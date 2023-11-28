# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod

from build_processors.artifact_details import BaseArtifact
from vendored_sdks.models import ManifestArtifactFormat, NetworkFunctionApplication, ResourceElementTemplate


class BaseBuildProcessor(ABC):
    """Base class for build processors."""

    @staticmethod
    @abstractmethod
    def get_artifact_manifest_list() -> list[ManifestArtifactFormat]:
        """Get the artifact list."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_artifact_details() -> list[BaseArtifact]:
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
