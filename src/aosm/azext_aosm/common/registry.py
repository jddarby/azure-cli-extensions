# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
import re
import shutil
import subprocess
import os
from time import sleep
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


class ContainerRegistry:
    """
    A class to represent a registry and handle all Registry operations.
    """

    def __init__(self, registry_name: str):
        """
        Initialise the Registry object.

        :param registry_name: The name of the registry
        :param registry_namespace: The namespace of the registry
        """
        self.registry_name = registry_name

    def to_dict(self) -> dict:
        """Convert an instance to a dict."""
        output_dict = {"type": REGISTRY_CLASS_TO_TYPE[type(self)]}
        output_dict.update({k: vars(self)[k] for k in vars(self)})
        return output_dict

    @classmethod
    def from_dict(cls, registry_dict: Dict) -> "ContainerRegistry":
        try:
            registry_name = registry_dict["registry_name"]
            registry_class = REGISTRY_TYPE_TO_CLASS[registry_dict["type"]]
            return registry_class(registry_name)
        except KeyError as error:
            raise ValueError(
                f"Registry is missing required field {error}.\n"
                f"Registry is: {registry_dict}.\n"
                "This is unexpected and most likely comes from manual editing "
                "of the definition folder."
            )

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
                    " source registry %s and that you have run docker login on this registry."
                ),
                source_image,
                self.registry_name,
            )
            logger.debug(error, exc_info=True)
            raise error

    def push_image_from_local_registry(
        self,
        target_acr: str,
        target_image: str,
        target_username: str,
        target_password: str,
        local_docker_image: str,
    ) -> None:
        """
        Push image to target registry using docker push. Requires docker.

        :param local_docker_image: name and tag of the source image on local registry
            e.g. uploadacr.azurecr.io/samples/nginx:stable
        :type local_docker_image: str
        :param target_password: The password to use for the az acr login attempt
        :type target_password: str
        """

        target = f"{target_acr}/{target_image}"
        logger.debug("Target ACR: %s", target)

        print("Tagging source image")
        tag_image_cmd = [
            str(shutil.which("docker")),
            "tag",
            local_docker_image,
            target,
        ]
        call_subprocess_raise_output(tag_image_cmd)

        logger.info("Logging into artifact store registry %s", target_acr)
        # ACR login seems to work intermittently, so we retry on failure
        retries = 0
        while True:
            try:
                target_acr_login_cmd = [
                    str(shutil.which("az")),
                    "acr",
                    "login",
                    "--name",
                    target_acr,
                    "--username",
                    target_username,
                    "--password",
                    target_password,
                ]
                call_subprocess_raise_output(target_acr_login_cmd)
                logger.debug("Logged in to %s", target_acr)
                break
            except CLIError as error:
                if retries < 20:
                    logger.info("Retrying ACR login. Retries so far: %s", retries)
                    retries += 1
                    sleep(3)
                    continue
                logger.error(
                    ("Failed to login to %s as %s."), target_acr, target_username
                )
                logger.debug(error, exc_info=True)
                raise error

        try:
            print("Pushing target image using docker push")
            push_target_image_cmd = [
                str(shutil.which("docker")),
                "push",
                target,
            ]
            call_subprocess_raise_output(push_target_image_cmd)
        except CLIError as error:
            logger.error(
                ("Failed to push %s to %s."),
                local_docker_image,
                target_acr,
            )
            logger.debug(error, exc_info=True)
            raise error
        finally:
            docker_logout_cmd = [
                str(shutil.which("docker")),
                "logout",
                target_acr,
            ]
            call_subprocess_raise_output(docker_logout_cmd)


class UniversalRegistry(ContainerRegistry):

    def find_image(self, image: str, version: str) -> ContainerRegistry:
        """
        Find whether the given image exists in this registry.

        :param image: The image to find in the registry
        :return: The registry and namespace for the image
        """

        image_path = f"{self.registry_name}/{image}:{version}"

        logger.debug("Checking if image %s exists in %s", image, self.registry_name)

        try:
            manifest_inspect_cmd = [
                str(shutil.which("docker")),
                "manifest",
                "inspect",
                image_path,
            ]

            output = call_subprocess_raise_output(manifest_inspect_cmd)

            if output is None:
                return None
            else:
                return self
        except CLIError as error:
            if "manifest unknown" in str(error):
                return None
            logger.warning(
                (
                    "Failed to contact source registry %s. "
                    "Make sure you run docker login on this registry "
                    "before running the aosm command."
                ),
                self.registry_name,
            )
            logger.debug(error, exc_info=True)
            raise error


class AzureContainerRegistry(ContainerRegistry):
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
        try:
            super().pull_image_to_local_registry(source_image)
        except CLIError as error:
            raise error
        finally:
            docker_logout_cmd = [
                str(shutil.which("docker")),
                "logout",
                self.registry_name,
            ]
            call_subprocess_raise_output(docker_logout_cmd)

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

    def get_repositories(self) -> Dict[str, Tuple["AzureContainerRegistry", str]]:
        """
        Query the images in the registry in all available namespaces.

        :return: A dictionary of images with the image name as the key
        and the registry and namespace as the value.
        """
        repositories = {}

        acr_get_repositories_cmd = [
            str(shutil.which("az")),
            "acr",
            "repository",
            "list",
            "--name",
            self.registry_name,
        ]

        logger.info("Looking for images in %s registry", self.registry_name)

        repository_list: List[str] = json.loads(
            call_subprocess_raise_output(acr_get_repositories_cmd)
        )

        logger.debug(
            "Repositories found in %s: %s", self.registry_name, repository_list
        )

        for repository in repository_list:
            acr_get_versions_for_repository_cmd = [
                str(shutil.which("az")),
                "acr",
                "repository",
                "show-tags",
                "--name",
                self.registry_name,
                "--repository",
                f"{repository}",
            ]

            version_list: List[str] = json.loads(
                call_subprocess_raise_output(acr_get_versions_for_repository_cmd)
            )

            for version in version_list:
                repositories[(repository, version)] = self

        return repositories


class ContainerRegistryHandler:
    """
    A class to handle all the registries and their images.
    """

    def __init__(self, image_sources):
        self.image_sources = image_sources
        self.registry_list = self._create_registry_list()
        self.registry_for_image = self._get_repositories()

    def _create_registry_list(self) -> List[ContainerRegistry]:
        """Create a list of registry objects from the registries provided by the user."""

        registries: Dict[str, ContainerRegistry] = {}
        registry_list: List[ContainerRegistry] = []

        for registry in self.image_sources:
            # if registry matches the pattern of myacr1.azurecr.io/**,
            # then create a an instance of the ACR registry class
            parts = registry.split("/", 1)
            registry_name = parts[0]

            acr_match = re.match(ACR_REGISTRY_NAME_PATTERN, registry_name)

            # TODO pk5: is this how we should be handling this? We are now effectively ignoring namespace completely and just using the registry name. Can we use the namespace somehow?
            registry = registry.rstrip("/")

            if registry_name not in registries:
                if acr_match:
                    registries[registry] = AzureContainerRegistry(registry_name)
                else:
                    registries[registry] = UniversalRegistry(registry)
                registry_list.append(registries[registry])

        return registry_list

    def get_registry_list(self) -> List[ContainerRegistry]:
        """
        Get the list of registries.
        """
        return self.registry_list

    def _get_repositories(self) -> Dict[str, Tuple["ContainerRegistry", str]]:
        """
        Cycle through all available registries and get the images that they have.

        :return: A dictionary of images with the image name as the key and the registry and namespace as the value.
        """
        registry_for_image = {}

        for registry in self.registry_list:

            if isinstance(registry, AzureContainerRegistry):
                registry_for_image.update(registry.get_repositories())

        logger.debug("Images found in the ACR registires: %s", registry_for_image)
        return registry_for_image

    def find_registry_for_image(
        self, image, version
    ) -> Tuple["ContainerRegistry", str]:
        """
        Find the registry and namespace for a given image.

        :param image: The image to find the registry for
        :return: The registry and namespace for the image
        """
        # TODO: this function should not be running in build

        if (image, version) in self.registry_for_image:
            return self.registry_for_image[(image, version)]

        for registry in self.registry_list:
            if isinstance(registry, UniversalRegistry):
                image_registry = registry.find_image(image, version)
                if image_registry:
                    return image_registry
                continue
        logger.warning(
            "Image: %s, version: %s was not found in any of the provided registries",
            image,
            version,
        )
        return None


# Mapping of registry type names to their classes.
REGISTRY_CLASS_TO_TYPE = {
    UniversalRegistry: "UniversalRegistry",
    AzureContainerRegistry: "AzureContainerRegistry",
}

REGISTRY_TYPE_TO_CLASS = {value: key for key, value in REGISTRY_CLASS_TO_TYPE.items()}
