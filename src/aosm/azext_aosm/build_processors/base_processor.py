# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

from ..common.artifact import BaseArtifact
from ..input_artifacts.base_input_artifact import BaseInputArtifact
from ..common.local_file_builder import LocalFileBuilder
from ..vendored_sdks.models import ManifestArtifactFormat, NetworkFunctionApplication, ResourceElementTemplate, ArtifactStore

@dataclass
class BaseBuildProcessor(ABC):
    """Base class for build processors."""

    name: str
    artifact_store: ArtifactStore
    input_artifact: BaseInputArtifact

    @abstractmethod
    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        raise NotImplementedError

    @abstractmethod
    def get_artifact_details(self) -> Tuple[List[BaseArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        raise NotImplementedError

    @abstractmethod
    def generate_nf_application(self) -> NetworkFunctionApplication:
        """Generate the NF application."""
        raise NotImplementedError

    @abstractmethod
    def generate_resource_element_template(self) -> ResourceElementTemplate:
        """Generate the resource element template."""
        raise NotImplementedError