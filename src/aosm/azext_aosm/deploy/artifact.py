# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material

# pylint: disable=unidiomatic-typecheck
"""A module to handle interacting with artifacts."""
from typing import Union
from dataclasses import dataclass
from knack.log import get_logger

from azure.storage.blob import BlobClient, BlobType
from azext_aosm._configuration import ArtifactConfig, HelmPackageConfig
from oras.client import OrasClient


logger = get_logger(__name__)


@dataclass
class Artifact:
    """Artifact class."""

    artifact_name: str
    artifact_type: str
    artifact_version: str
    artifact_client: Union[BlobClient, OrasClient]

    def upload(self, artifact_config: ArtifactConfig or HelmPackageConfig) -> None:
        """
        Upload aritfact.

        :param artifact_config: configuration for the artifact being uploaded
        """
        if type(self.artifact_client) == OrasClient:
            self._upload_helm_to_acr(artifact_config)

            ## TODO: pk5 fix this

            # if type(artifact_config) == HelmPackageConfig:
            #     self._upload_helm_to_acr(artifact_config)
            # elif type(artifact_config) == ArtifactConfig:
            #     self._upload_arm_to_acr(artifact_config)
        else:
            self._upload_to_storage_account(artifact_config)

    def _upload_arm_to_acr(self, artifact_config: ArtifactConfig) -> None:
        """
        Upload ARM artifact to ACR.

        :param artifact_config: configuration for the artifact being uploaded
        """
        assert type(self.artifact_client) == OrasClient

        # If not included in config, the file path value will be the description of
        # the field.

        if artifact_config.file_path:
            target = f"{self.artifact_client.remote.hostname.replace('https://', '')}\
                /{self.artifact_name}:{self.artifact_version}"
            logger.debug("Uploading %s to %s", artifact_config.file_path, target)
            self.artifact_client.push(
                files=[artifact_config.file_path],
                target=target,
            )
        else:
            raise NotImplementedError(
                "Copying artifacts is not implemented for ACR artifacts stores."
            )

    def _upload_helm_to_acr(self, artifact_config: HelmPackageConfig) -> None:
        """
        Upload artifact to ACR.

        :param artifact_config: configuration for the artifact being uploaded
        """
        assert type(self.artifact_client) == OrasClient

        # If not included in config, the file path value will be the description of
        # the field.

        if artifact_config["path_to_chart"]:
            target = f"{self.artifact_client.remote.hostname.replace('https://', '')}/{self.artifact_name}:{self.artifact_version}"
            logger.debug(f"Uploading {artifact_config['path_to_chart']} to {target}")
            self.artifact_client.push(
                files=[artifact_config["path_to_chart"]],
                target=target,
            )

        else:
            raise NotImplementedError(
                "Copying artifacts is not implemented for ACR artifacts stores."
            )

    def _upload_to_storage_account(self, artifact_config: ArtifactConfig) -> None:
        """
        Upload artifact to storage account.

        :param artifact_config: configuration for the artifact being uploaded
        """
        assert type(self.artifact_client) == BlobClient
        assert type(artifact_config) == ArtifactConfig

        # If the file path is given, upload the artifact, else, copy it from an existing blob.
        if artifact_config.file_path:
            logger.info("Upload to blob store")
            with open(artifact_config.file_path, "rb") as artifact:
                self.artifact_client.upload_blob(
                    artifact, overwrite=True, blob_type=BlobType.PAGEBLOB
                )
            logger.info(
                "Successfully uploaded %s to %s",
                artifact_config.file_path,
                self.artifact_client.account_name,
            )
        else:
            logger.info("Copy from SAS URL to blob store")
            source_blob = BlobClient.from_blob_url(artifact_config.blob_sas_url)

            if source_blob.exists():
                logger.debug(source_blob.url)
                self.artifact_client.start_copy_from_url(source_blob.url)
                logger.info(
                    "Successfully copied %s from %s to %s",
                    source_blob.blob_name,
                    source_blob.account_name,
                    self.artifact_client.account_name,
                )
            else:
                raise RuntimeError(
                    f"{source_blob.blob_name} does not exist in {source_blob.account_name}."
                )

    def copy_image(
        self,
        cli_ctx,
        management_client,
        source_registry_id,
        source_image,
        target_registry_resource_group_name,
        target_registry_name,
        mode="NoForce",
    ):
        from azure.mgmt.containerregistry.models import (
            ImportImageParameters,
            ImportSource,
        )

        from azure.cli.core.commands import LongRunningOperation

        ## TODO: pk5 Check if the registry exists

        ## TODO: pk5 figure out the tags

        ## TODO: pk5 figure out what happens if the artifact is not in the registry

        target_tags = [source_image]

        source = ImportSource(resource_id=source_registry_id, source_image=source_image)

        import_parameters = ImportImageParameters(
            source=source,
            target_tags=target_tags,
            untagged_target_repositories=[],
            mode=mode,
        )

        result_poller = management_client.begin_import_image(
            resource_group_name=target_registry_resource_group_name,
            registry_name=target_registry_name,
            parameters=import_parameters,
        )

        return LongRunningOperation(cli_ctx, "Importing image...")(result_poller)
