# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# TODO: Move these somewhere more appropriate and probably expand into actual artifact
# definition element component classes.

from abc import ABC, abstractmethod
from pathlib import Path

from vendored_sdks.models import ManifestArtifactFormat

class BaseArtifact(ABC):
    """Abstract base class for artifacts."""
    artifact_manifest: ManifestArtifactFormat

    def __init__(self, artifact_manifest: ManifestArtifactFormat):
        self.artifact_manifest = artifact_manifest

    @abstractmethod
    def upload(self):
        """Upload the artifact."""
        # TODO: Implement all of these I guess
        raise NotImplementedError

class BaseACRArtifact(BaseArtifact):
    """Abstract base class for ACR artifacts."""
    # TODO: Implement
    pass

class LocalFileACRArtifact(BaseACRArtifact):
    """Class for ACR artifacts from a local file."""
    file_path: Path

    # TODO: Implement
    pass

class LocalDockerACRArtifact(BaseACRArtifact):
    """Class for ACR artifacts from a local Docker image."""
    docker_image_name: str

    # TODO: Implement
    pass

class RemoteACRArtifact(BaseACRArtifact):
    """Class for ACR artifacts from a remote ACR image."""
    acr_name: str
    namespace: str

    # TODO: Implement
    pass

class BaseStorageAccountArtifact(BaseArtifact):
    """Abstract base class for storage account artifacts."""
    # TODO: Implement
    pass

class LocalFileStorageAccountArtifact(BaseStorageAccountArtifact):
    """Class for storage account artifacts from a local file."""
    file_path: Path

    # TODO: Implement
    pass

class BlobStorageAccountArtifact(BaseStorageAccountArtifact):
    """Class for storage account artifacts from a remote blob."""
    blob_sas_uri: str

    # TODO: Implement
    pass
