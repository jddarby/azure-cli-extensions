# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
import re
import shutil
import subprocess
import os
from typing import List, Tuple, Dict
import requests
from requests.auth import HTTPBasicAuth
from knack.log import get_logger
from knack.util import CLIError
import base64
from azure.cli.core.azclierror import UnauthorizedError

from azext_aosm.common.utils import (
    call_subprocess_raise_output,
    clean_registry_name,
)

# TODO: check linting

logger = get_logger(__name__)
ACR_REGISTRY_NAME_PATTERN = r"^([a-zA-Z0-9]+\.azurecr\.io)"


class Registry:
    """
    A class to represent a registry and handle all Registry operations.
    """

    def __init__(self, registry_name: str, registry_namespace: str):
        """
        Initialise the Registry object.

        :param registry_name: The name of the registry
        :param registry_namespace: The namespace of the registry
        """
        self.registry_name = registry_name
        self.registry_namespaces = [registry_namespace]

    def add_namespace(self, namespace: str) -> None:
        """
        Add a namespace to the registry.

        :param namespace: The namespace to add to the registry
        """
        self.registry_namespaces.append(namespace)

    # TODO: Test
    def pull_image_to_local_registry(self, source_image: str) -> None:
        """
        Pull image to local registry using docker pull. Requires docker.

        Uses the CLI user's context to log in to the source registry.

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
            call_subprocess_raise_output(pull_source_image_cmd)
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
            # TODO: If we do this before the get_images thing, we will lose the credentials from the config.json file
            docker_logout_cmd = [
                str(shutil.which("docker")),
                "logout",
                self.registry_name,
            ]
            call_subprocess_raise_output(docker_logout_cmd)

    def get_access_credentials(self) -> Tuple[str, str]:
        """
        Get the access credentials for the registry from the default docker config file.

        :return: A tuple of the username and password for the registry
        """

        try:
            docker_config_path = os.path.expanduser("~/.docker/config.json")
            # TODO: specify the encoding
            with open(docker_config_path) as credentials_file:
                credentials = json.load(credentials_file)
                auth_token = credentials["auths"][self.registry_name.lower()]["auth"]
                decoded_auth_token = base64.b64decode(auth_token).decode()
                username, password = decoded_auth_token.split(":")
                return username, password
        except (FileNotFoundError, KeyError) as error:
            # TODO: Should we allow the user to input credentials manually?
            logger.debug(error, exc_info=True)
            raise UnauthorizedError(
                f"Access credentials for registry {self.registry_name} do no exist in the {docker_config_path}"
            ) from error

    # def get_images(self) -> Dict[str, Tuple["Registry", str]]:
    #     """
    #     Query the images in the registry in all available namespaces.

    #     :return: A dictionary of images with the image name as the key
    #     and the registry and namespace as the value.
    #     """

    #     # We need to pass in username and password instead of logging into the registry because
    #     # docker does not have a command to list images. Instead we need to use a get request
    #     username, password = self.get_access_credentials()
    #     images = {}

    #     for namespace in self.registry_namespaces:
    #         # TODO: make sure you are not logging out passwords
    #         url = f"https://{self.registry_name}/v2/{namespace}/tags/list"
    #         response = requests.get(
    #             url,
    #             auth=HTTPBasicAuth(
    #                 username,
    #                 password,
    #             ),
    #         )
    #         try:
    #             tags = response.json()["tags"]
    #             for tag in tags:
    #                 # TODO: if the tag appears in multiple namespaces, it will be overwritten, is that ok?
    #                 images[tag] = (self, namespace)
    #         except KeyError:
    #             logger.debug(
    #                 "Could not obtain tags from %s", self.registry_name, exc_info=True
    #             )
    #             continue
    #     return images

    def find_image(self, image: str, version: str) -> Tuple["Registry", str]:
        """
        Find whether the given image exists in this registry.

        :param image: The image to find in the registry
        :return: The registry and namespace for the image
        """

        for namespace in self.registry_namespaces:
            image_path = f"{self.registry_name}/{namespace}/{image}:{version}"

            try:
                manifest_inspect_cmd = [
                    str(shutil.which("docker")),
                    "manifest inspect",
                    image_path,
                ]

                return_code = call_subprocess_raise_output(manifest_inspect_cmd)

                if return_code == 0:
                    return self, namespace
            except CLIError as error:
                logger.warning(
                    (
                        "Failed to contact source registry %s."
                        "Make sure you run docker login on this registry "
                        "before running the aosm command."
                    ),
                    self.registry_name,
                )
                logger.debug(error, exc_info=True)
                raise error
        return None, None


class ACRRegistry(Registry):
    """
    A class to represent an Azure Container Registry and handle all ACR operations.
    """

    # TODO: there is a comment in the artifact.py file about the login to ACRs only working intermittently. We should check if this is the case here
    def _login(self):
        """
        Log in to the source registry using the Azure CLI.
        """

        message = f"Logging into source registry {self.registry_name}"
        print(message)  # TODO: Should this be a print?
        logger.info(message)
        try:
            acr_source_login_cmd = [
                str(shutil.which("az")),
                "acr",
                "login",
                "--name",
                self.registry_name,
            ]
            call_subprocess_raise_output(acr_source_login_cmd)
        # TODO: better error
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
    ) -> None:
        """
        Copy an image from this registry to a target ACR.

        :param source_image: The image to copy
        :param target_acr: The target ACR
        :param artifact_name: The name of the artifact
        :param artifact_version: The version of the artifact
        """

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
            # Dont use call_subprocess_raise_output here as we don't want to log the
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
            source = f"{clean_registry_name(self.registry_name)}/{source_image}"
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
            call_subprocess_raise_output(acr_import_image_cmd)
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

    def find_image(self, image, version) -> Tuple["ACRRegistry", str]:
        """
        Query the images in the registry in all available namespaces.

        :return: A dictionary of images with the image name as the key
        and the registry and namespace as the value.
        """

        for namespace in self.registry_namespaces:
            image_with_namespace = f"{namespace}/{image}:{version}"
            try:
                acr_source_get_images_cmd = [
                    str(shutil.which("az")),
                    "acr",
                    "repository",
                    "show",
                    "--name",
                    self.registry_name,
                    "--image",
                    image_with_namespace,
                ]

                return_code = call_subprocess_raise_output(acr_source_get_images_cmd)

                if return_code == 0:
                    return (self, namespace)

            except CLIError as error:
                logger.debug(
                    ("Image %s, version %s not found in %s registry."),
                    image,
                    version,
                    self.registry_name,
                )
                logger.debug(error, exc_info=True)

        return None, None


class RegistryHandler:
    """
    A class to handle all the registries and their images.
    """

    def __init__(self, image_sources):
        self.image_sources = image_sources
        self.registry_list = self._create_registry_list()

    def _create_registry_list(self) -> List[Registry]:
        """Create a list of registry objects from the registries provided by the user."""

        registries: Dict[str, Registry] = {}
        registry_list: List[Registry] = []

        for registry in self.image_sources:
            # if registry matches the pattern of myacr1.azurecr.io/**,
            # then create a an instance of the ACR registry class
            parts = registry.split("/", 1)
            registry_name = parts[0]
            registry_namespace = parts[1] if len(parts) > 1 else None

            # Remove a trailing slash from regisry_namespace
            if registry_namespace:
                registry_namespace = registry_namespace.rstrip("/")

            acr_match = re.match(ACR_REGISTRY_NAME_PATTERN, registry_name)

            if registry_name not in registries:
                if acr_match:
                    registries[registry_name] = ACRRegistry(
                        registry_name, registry_namespace
                    )
                else:
                    registries[registry_name] = Registry(
                        registry_name, registry_namespace
                    )
                registry_list.append(registries[registry_name])
            else:
                registries[registry_name].add_namespace(registry_namespace)

        return registry_list

    def get_registry_list(self) -> List[Registry]:
        """
        Get the list of registries.
        """
        return self.registry_list

    def find_registry_for_image(self, image, version) -> Tuple["Registry", str]:
        """
        Find the registry and namespace for a given image.

        :param image: The image to find the registry for
        :return: The registry and namespace for the image
        """

        for registry in self.registry_list:
            registry_for_image, namespace = registry.find_image(image, version)
            if registry_for_image:
                return registry_for_image, namespace
            continue
        logger.warning("Image %s not found in any of the provided registries", image)
        return None
