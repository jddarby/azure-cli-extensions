# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
import re
import shutil
import subprocess
import requests
from requests.auth import HTTPBasicAuth
from knack.log import get_logger
from knack.util import CLIError
from azure.cli.command_modules.acr._docker_utils import (
    request_data_from_registry,
    get_access_credentials,
    RegistryAccessTokenPermission,
)

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

logger = get_logger(__name__)


def _clean_name(registry_name: str) -> str:
    """Remove https:// from the registry name."""
    return registry_name.replace("https://", "")


# TODO: This is taken from the Artifact class. This should just be a utility function
def _call_subprocess_raise_output(cmd: list) -> None:
    """
    Call a subprocess and raise a CLIError with the output if it fails.

    :param cmd: command to run, in list format
    :raise CLIError: if the subprocess fails
    """
    log_cmd = cmd.copy()
    if "--password" in log_cmd:
        # Do not log out passwords.
        log_cmd[log_cmd.index("--password") + 1] = "[REDACTED]"

    try:
        called_process = subprocess.run(
            cmd, encoding="utf-8", capture_output=True, text=True, check=True
        )
        logger.debug(
            "Output from %s: %s. Error: %s",
            log_cmd,
            called_process.stdout,
            called_process.stderr,
        )
        return called_process.stdout
    except subprocess.CalledProcessError as error:
        all_output: str = (
            f"Command: {' '.join(log_cmd)}\n"
            f"stdout: {error.stdout}\n"
            f"stderr: {error.stderr}\n"
            f"Return code: {error.returncode}"
        )
        logger.debug("The following command failed to run:\n%s", all_output)
        # Raise the error without the original exception, which may contain secrets.
        raise CLIError(all_output) from None


class Registry:
    def __init__(self, registry_name: str, registry_namespace: str):
        self.registry_name = registry_name
        self.registry_namespaces = [registry_namespace]

    def add_namespace(self, namespace: str):
        self.registry_namespaces.append(namespace)

    # TODO: this has not been tested at all but it is pretty much the same as what was in the RemoteACRArtifact class
    def pull_image_to_local_registry(self, source_image: str):
        """
        Pull image to local registry using docker pull. Requires docker.

        Uses the CLI user's context to log in to the source registry.

        :param: source_registry_login_server: e.g. uploadacr.azurecr.io
        :param: source_image: source docker image name e.g.
            uploadacr.azurecr.io/samples/nginx:stable
        """
        try:
            message = f"Pulling source image {source_image}"
            print(message)
            logger.info(message)
            pull_source_image_cmd = [
                str(shutil.which("docker")),
                "pull",
                source_image,
            ]
            _call_subprocess_raise_output(pull_source_image_cmd)
        except CLIError as error:
            logger.error(
                (
                    "Failed to pull %s. Check if this image exists in the"
                    " source registry %s."
                ),
                source_image,
                self.registry_name,
            )
            logger.debug(error, exc_info=True)
            raise error
        finally:
            docker_logout_cmd = [
                str(shutil.which("docker")),
                "logout",
                self.registry_name,
            ]
            _call_subprocess_raise_output(docker_logout_cmd)

    def get_images(self):

        images = {}
        for namespace in self.registry_namespaces:
            # TODO: should this have a try and except block?
            # TODO: this should use real username and password
            url = f"https://{self.registry_name}/v2/{namespace}/tags/list"
            response = requests.get(url, auth=HTTPBasicAuth("admin", "adminpass!"))

            for image in response["tags"]:
                images[image] = (self, namespace)

        return images


class ACRRegistry(Registry):

    # TODO: there is a comment in the artifact.py file about the login to ACRs only working intermittently. We should check if this is the case here
    def _login(self):
        message = f"Logging into source registry {self.registry_name}"
        print(message)  # Should this be a print?
        logger.info(message)
        try:
            acr_source_login_cmd = [
                str(shutil.which("az")),
                "acr",
                "login",
                "--name",
                self.registry_name,
            ]
            _call_subprocess_raise_output(acr_source_login_cmd)
        except CLIError as error:
            logger.error(("Failed to log into registry %s."), self.registry_name)
            logger.debug(error, exc_info=True)
            raise error

    def pull_image_to_local_registry(self, source_image: str):

        self._login()
        super().pull_image_to_local_registry(source_image)

    # TODO: test this - ported from the artifact.py
    def copy_image(
        self,
        source_image: str,
        target_acr: str,
        artifact_name: str,
        artifact_version: str,
    ):
        try:
            print("Copying artifact from source registry")
            # In order to use az acr import cross subscription, we need to use a token
            # to authenticate to the source registry. This is documented as the way to
            # us az acr import cross-tenant, not cross-sub, but it also works
            # cross-subscription, and meant we didn't have to make a breaking change to
            # the format of input.json. Our usage here won't work cross-tenant since
            # we're attempting to get the token (source) with the same context as that
            # in which we are creating the ACR (i.e. the target tenant)
            get_token_cmd = [str(shutil.which("az")), "account", "get-access-token"]
            # Dont use _call_subprocess_raise_output here as we don't want to log the
            # output
            called_process = subprocess.run(  # noqa: S603
                get_token_cmd,
                encoding="utf-8",
                capture_output=True,
                text=True,
                check=True,
            )
            access_token_json = json.loads(called_process.stdout)
            access_token = access_token_json["accessToken"]
        except subprocess.CalledProcessError as get_token_err:
            # This error is thrown from the az account get-access-token command
            # If it errored we can log the output as it doesn't contain the token
            logger.debug(get_token_err, exc_info=True)
            raise CLIError(  # pylint: disable=raise-missing-from
                "Failed to import image: could not get an access token from your"
                " Azure account. Try logging in again with `az login` and then re-run"
                " the command. If it fails again, please raise an issue and try"
                " repeating the command using the --no-subscription-permissions"
                " flag to pull the image to your local machine and then"
                " push it to the Artifact Store using manifest credentials scoped"
                " only to the store. This requires Docker to be installed"
                " locally."
            )

        try:
            # TODO: we need to add namespace here
            source = f"{_clean_name(self.registry_name)}/{source_image}"
            acr_import_image_cmd = [
                str(shutil.which("az")),
                "acr",
                "import",
                "--name",
                target_acr,
                "--source",
                source,
                "--image",
                f"{artifact_name}:{artifact_version}",
                "--password",
                access_token,
            ]
            _call_subprocess_raise_output(acr_import_image_cmd)
        except CLIError as error:
            logger.debug(error, exc_info=True)
            if (" 401" in str(error)) or ("Unauthorized" in str(error)):
                # As we shell out the the subprocess, I think checking for these strings
                # is the best check we can do for permission failures.
                raise CLIError(
                    "Failed to import image.\nThe problem may be one or more of:\n"
                    " - the source_registry in your config file does not exist;\n"
                    " - the image doesn't exist;\n"
                    " - you do not have permissions to import images.\n"
                    f"You need to have Reader/AcrPull from {self.registry_name}, "
                    "and Contributor role + AcrPush role, or a custom "
                    "role that allows the importImage action and AcrPush over the "
                    "whole subscription in order to be able to import to the new "
                    "Artifact store. More information is available at "
                    "https://aka.ms/acr/authorization\n\n"
                    "If you do not have the latter then you can re-run the command using "
                    "the --no-subscription-permissions flag to pull the image to your "
                    "local machine and then push it to the Artifact Store using manifest "
                    "credentials scoped only to the store. This requires Docker to be "
                    "installed locally."
                ) from error

            # Otherwise, the most likely failure is that the image already exists in the artifact
            # store, so don't fail at this stage, log the error.
            logger.warning(
                (
                    "Failed to import %s to %s. If this failure is because it already exists in "
                    "the target registry we can continue. If the failure was for another reason, "
                    " for example it does not exist in the source registry, this is likely "
                    "fatal. Attempting to continue.\n"
                    "%s"
                ),
                source_image,
                target_acr,
                error,
            )

    def get_images(self):
        images = {}
        self._login()
        for namespace in self.registry_namespaces:
            acr_source_get_images_cmd = [
                str(shutil.which("az")),
                "acr",
                "repository",
                "show-tags",
                "--name",
                self.registry_name,
                "--repository",
                namespace,
            ]

            output = _call_subprocess_raise_output(acr_source_get_images_cmd)

            # This should give me a dictionary where I can search for an image and I will get a registry object (but I also want a namespace with it as well)
            for image in output:
                images[image] = (self, namespace)

        return images


class GenericRegistry(Registry):
    pass


class RegistryHandler:
    def __init__(self, image_sources):
        self.image_sources = image_sources
        self.registry_list = self._create_registry_list()
        self.registry_for_image = self._get_images()

    def _create_registry_list(self) -> [Registry]:
        """Get the list of registries."""

        registries = {}
        registry_list = []

        for registry in self.image_sources:
            # if registry matches the pattern of myacr1.azurecr.io/**, then create a an instance of the ACR registry class
            parts = registry.split("/", 1)
            registry_name = parts[0]
            registry_namespace = parts[1] if len(parts) > 1 else None
            # Remove a trailing slash from regisry_namespace
            registry_namespace = registry_namespace.rstrip("/")

            # TODO: this should be moved to top of the file
            acr_pattern = r"^([a-zA-Z0-9]+\.azurecr\.io)"
            match = re.match(acr_pattern, registry_name)

            if registry_name not in registries:
                if match:
                    registries[registry_name] = ACRRegistry(
                        registry_name, registry_namespace
                    )
                else:
                    registries[registry_name] = GenericRegistry(
                        registry_name, registry_namespace
                    )
                registry_list.append(registries[registry_name])
            else:
                registries[registry_name].add_namespace(registry_namespace)

        return registry_list

    def get_registry_list(self):
        return self.registry_list

    def _get_images(self):
        # go through all registries and find the images that they have.
        # Then have some function that can search for registry based on the image.
        # For example find_registry_for_image
        registry_for_image = {}

        for registry in self.registry_list:

            registry_for_image.update(registry.get_images())

        return registry_for_image

    def find_registry_for_image(self, image):

        if image in self.registry_for_image:
            return self.registry_for_image[image]
        logger.warning("Image %s not found in any of the provided registries", image)
        return None
