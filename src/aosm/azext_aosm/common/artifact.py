# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# TODO: Move these somewhere more appropriate and probably expand into actual artifact
# definition element component classes.

from abc import ABC, abstractmethod
from pathlib import Path

from azext_aosm.vendored_sdks.models import ManifestArtifactFormat


class BaseArtifact(ABC):
    """Abstract base class for artifacts."""

    artifact_manifest: ManifestArtifactFormat

    def __init__(self, artifact_manifest: ManifestArtifactFormat):
        self.artifact_manifest = artifact_manifest

    def to_dict(self) -> dict:
        """Convert an instance to a dict."""
        # Flatten the artifact manifest into the dict and add type.
        output_dict = {
            "type": ARTIFACT_CLASS_TO_TYPE[type(self)],
            "artifact_name": self.artifact_manifest.artifact_name,
            "artifact_type": self.artifact_manifest.artifact_type,
            "artifact_version": self.artifact_manifest.artifact_version,
        }
        # Pull in all the fields from the class that aren't the artifact manifest
        output_dict.update(
            {
                k: vars(self)[k]
                for k in vars(self)
                if k != "artifact_manifest"
            }
        )
        return output_dict

    @abstractmethod
    def upload(self):
        """Upload the artifact."""
        # TODO: Implement all of these I guess
        raise NotImplementedError


class BaseACRArtifact(BaseArtifact):
    """Abstract base class for ACR artifacts."""

    @abstractmethod
    def upload(self):
        """Upload the artifact."""
        raise NotImplementedError


class LocalFileACRArtifact(BaseACRArtifact):
    """Class for ACR artifacts from a local file."""

    file_path: Path

    def __init__(self, artifact_manifest: ManifestArtifactFormat, file_path: Path):
        super().__init__(artifact_manifest)
        self.file_path = str(file_path)

    # TODO: Implement
    def upload(self):
        """Upload the artifact."""
        raise NotImplementedError


class LocalDockerACRArtifact(BaseACRArtifact):
    """Class for ACR artifacts from a local Docker image."""

    docker_image_name: str

    def __init__(
        self, artifact_manifest: ManifestArtifactFormat, docker_image_name: str
    ):
        super().__init__(artifact_manifest)
        self.docker_image_name = docker_image_name

    # TODO: Implement
    def upload(self):
        """Upload the artifact."""
        raise NotImplementedError


class RemoteACRArtifact(BaseACRArtifact):
    """Class for ACR artifacts from a remote ACR image."""

    source_registry: str
    source_registry_namespace: str

    def __init__(
        self, artifact_manifest: ManifestArtifactFormat,
        source_registry: str, source_registry_namespace: str
    ):
        super().__init__(artifact_manifest)
        self.source_registry = source_registry
        self.source_registry_namespace = source_registry_namespace

    # TODO: Implement
    def upload(self):
        """Upload the artifact."""
        raise NotImplementedError


class BaseStorageAccountArtifact(BaseArtifact):
    """Abstract base class for storage account artifacts."""

    # TODO: Implement
    def upload(self):
        """Upload the artifact."""
        raise NotImplementedError


class LocalFileStorageAccountArtifact(BaseStorageAccountArtifact):
    """Class for storage account artifacts from a local file."""

    file_path: Path

    def __init__(self, artifact_manifest: ManifestArtifactFormat, file_path: Path):
        super().__init__(artifact_manifest)
        self.file_path = str(file_path)

    # TODO: Implement
    def upload(self):
        """Upload the artifact."""
        raise NotImplementedError


class BlobStorageAccountArtifact(BaseStorageAccountArtifact):
    """Class for storage account artifacts from a remote blob."""

    blob_sas_uri: str

    def __init__(self, artifact_manifest: ManifestArtifactFormat, blob_sas_uri: str):
        super().__init__(artifact_manifest)
        self.blob_sas_uri = blob_sas_uri

    # TODO: Implement
    def upload(self):
        """Upload the artifact."""
        raise NotImplementedError


# Mapping of artifact type names to their classes.
ARTIFACT_TYPE_TO_CLASS = {
    "ACRFromLocalFile": LocalFileACRArtifact,
    "ACRFromLocalDocker": LocalDockerACRArtifact,
    "ACRFromRemote": RemoteACRArtifact,
    "StorageAccountFromLocalFile": LocalFileStorageAccountArtifact,
    "StorageAccountFromBlob": BlobStorageAccountArtifact,
}

# Generated mapping of artifact classes to type names.
ARTIFACT_CLASS_TO_TYPE = {v: k for k, v in ARTIFACT_TYPE_TO_CLASS.items()}
