# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, final, List, Tuple


from base_processor import BaseBuildProcessor
from artifact_details import BaseArtifact
from ..input_artifacts.arm_template_input_artifact import ArmTemplateInputArtifact
from ..common.local_file_builder import LocalFileBuilder

from ..vendored_sdks.models import (
    ArtifactStore,
    DependsOnProfile,
    ResourceElementTemplate,
    ManifestArtifactFormat,
    NetworkFunctionApplication,
    ArmResourceDefinitionResourceElementTemplateDetails,
    AzureCoreNetworkFunctionArmTemplateApplication,
    AzureCoreArtifactType,
    AzureCoreArmTemplateArtifactProfile,
    ArmTemplateArtifactProfile,
)


@dataclass
class BaseArmBuildProcessor(BaseBuildProcessor):
    """
    Base class for ARM template processors.

    This class loosely implements the Template Method pattern to define the steps required
    to generate NF applications and RETs from a given ARM template.

    The steps are as follows:
     - generate_schema
     - generate_mappings
     - generate_artifact_profile
     - generate_nfvi_specific_nf_application

    """

    name: str
    artifact_store: ArtifactStore
    input_artifact: ArmTemplateInputArtifact

    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        return [
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=AzureCoreArtifactType.ARM_TEMPLATE,
                artifact_version=self.input_artifact.artifact_version,
            )
        ]

    @abstractmethod
    def get_artifact_details(self) -> Tuple[List[BaseArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        raise NotImplementedError

    @final
    def generate_nf_application(self) -> NetworkFunctionApplication:
        return self.generate_nfvi_specific_nf_application()

    # TODO: Should this actually be a cached property?
    def generate_schema(self) -> Dict[str, Any]:
        return self.input_artifact.get_schema()

    def generate_mappings(self) -> Dict[str, str]:
        template_parameters = {}
        vm_parameters = self.generate_schema()

        # TODO: Document that this no longer appends "Image" to the image name supplied by user in input.jsonc
        # TODO: Document that the parameters are no longer ordered, and create story to reimplement ordering
        for key in vm_parameters:
            template_parameters[key] = f"{{deployParameters.{key}}}"

        return template_parameters

    # @abstractmethod?
    def generate_artifact_profile(self) -> AzureCoreArmTemplateArtifactProfile:
        artifact_profile = ArmTemplateArtifactProfile(
            template_name=self.input_artifact.artifact_name,
            template_version=self.input_artifact.artifact_version,
        )
        return AzureCoreArmTemplateArtifactProfile(
            artifact_store=self.artifact_store,
            template_artifact_profile=artifact_profile,
        )

    @abstractmethod
    def generate_nfvi_specific_nf_application(self):
        pass

    def generate_resource_element_template(self) -> ResourceElementTemplate:
        return ArmResourceDefinitionResourceElementTemplateDetails()


class AzureCoreArmBuildProcessor(BaseArmBuildProcessor):
    """
    This class represents an ARM template processor for Azure Core.
    """

    def generate_nfvi_specific_nf_application(
        self,
    ) -> AzureCoreNetworkFunctionArmTemplateApplication:
        return AzureCoreNetworkFunctionArmTemplateApplication(
            name=self.name,
            depends_on_profile=DependsOnProfile(),
            artifact_type=AzureCoreArtifactType.ARM_TEMPLATE,
            artifact_profile=self.generate_artifact_profile(),
            deploy_parameters_mapping_rule_profile=self.generate_mappings(),
        )


class NexusArmBuildProcessor(BaseArmBuildProcessor):
    """
    This class represents a processor for generating ARM templates specific to Nexus.
    """

    def generate_nfvi_specific_nf_application(self):
        pass