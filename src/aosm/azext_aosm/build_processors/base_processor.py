# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod

from azext_aosm.inputs.base_input import BaseInput
from azext_aosm.common.artifact import BaseArtifact
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.vendored_sdks.models import (
    ManifestArtifactFormat,
    NetworkFunctionApplication,
    ResourceElementTemplate,
    ArtifactStore,
)

from typing import List, Tuple


class BaseBuildProcessor(ABC):
    """Base class for build processors."""

    name: str
    artifact_store: ArtifactStore
    input_template: BaseInput

    @staticmethod
    @abstractmethod
    def get_artifact_manifest_list() -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_artifact_details() -> Tuple[List[BaseArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_nf_application() -> NetworkFunctionApplication:
        """Generate the NF application."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_resource_element_template() -> ResourceElementTemplate:
        """Generate the resource element template."""
        raise NotImplementedError
