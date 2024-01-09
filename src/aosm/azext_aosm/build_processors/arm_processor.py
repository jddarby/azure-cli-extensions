# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, final

from azext_aosm.build_processors.base_processor import BaseBuildProcessor
from azext_aosm.common.artifact import LocalFileACRArtifact
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.inputs.arm_template_input import ArmTemplateInput
from azext_aosm.vendored_sdks.models import (
    ApplicationEnablement, ArmResourceDefinitionResourceElementTemplate,
    ArmResourceDefinitionResourceElementTemplateDetails,
    ArmTemplateArtifactProfile, ArmTemplateMappingRuleProfile,
    AzureCoreArmTemplateArtifactProfile,
    AzureCoreArmTemplateDeployMappingRuleProfile, AzureCoreArtifactType,
    AzureCoreNetworkFunctionArmTemplateApplication, DependsOnProfile,
    ManifestArtifactFormat, NetworkFunctionApplication, NSDArtifactProfile,
    ReferencedResource, ResourceElementTemplate, TemplateType)


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

    input_artifact: ArmTemplateInput

    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        return [
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=AzureCoreArtifactType.ARM_TEMPLATE.value,
                artifact_version=self.input_artifact.artifact_version,
            )
        ]

    def get_artifact_details(
        self,
    ) -> Tuple[List[LocalFileACRArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        return (
            [
                LocalFileACRArtifact(
                    artifact_manifest=ManifestArtifactFormat(
                        artifact_name=self.input_artifact.artifact_name,
                        artifact_type=AzureCoreArtifactType.ARM_TEMPLATE.value,
                        artifact_version=self.input_artifact.artifact_version,
                    ),
                    file_path=self.input_artifact.template_path,
                )
            ],
            [],
        )

    @final
    def generate_nf_application(self) -> NetworkFunctionApplication:
        return self.generate_nfvi_specific_nf_application()

    def generate_artifact_profile(self) -> AzureCoreArmTemplateArtifactProfile:
        artifact_profile = ArmTemplateArtifactProfile(
            template_name=self.input_artifact.artifact_name,
            template_version=self.input_artifact.artifact_version,
        )
        return AzureCoreArmTemplateArtifactProfile(
            artifact_store=ReferencedResource(id=""),
            template_artifact_profile=artifact_profile,
        )

    @abstractmethod
    def generate_nfvi_specific_nf_application(self):
        pass

    def generate_resource_element_template(self) -> ResourceElementTemplate:
        """Generate the resource element template."""
        parameter_values = self.generate_values_mappings(
            self.input_artifact.get_schema(), self.input_artifact.get_defaults(), True
        )

        artifact_profile = NSDArtifactProfile(
            artifact_store_reference=ReferencedResource(id=""),
            artifact_name=self.input_artifact.artifact_name,
            artifact_version=self.input_artifact.artifact_version,
        )

        return ArmResourceDefinitionResourceElementTemplateDetails(
            name=self.name,
            depends_on_profile=DependsOnProfile(),
            configuration=ArmResourceDefinitionResourceElementTemplate(
                template_type=TemplateType.ARM_TEMPLATE.value,
                parameter_values=json.dumps(parameter_values),
                artifact_profile=artifact_profile,
            ),
        )


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
            deploy_parameters_mapping_rule_profile=self._generate_mapping_rule_profile(),
        )

    def _generate_mapping_rule_profile(
        self,
    ) -> AzureCoreArmTemplateDeployMappingRuleProfile:
        template_parameters = self.generate_values_mappings(
            self.input_artifact.get_schema(), self.input_artifact.get_defaults()
        )

        mapping_profile = ArmTemplateMappingRuleProfile(
            template_parameters=json.dumps(template_parameters)
        )

        return AzureCoreArmTemplateDeployMappingRuleProfile(
            application_enablement=ApplicationEnablement.ENABLED,
            template_mapping_rule_profile=mapping_profile,
        )


class NexusArmBuildProcessor(BaseArmBuildProcessor):
    """
    Not implemented yet. This class represents a processor for generating ARM templates specific to Nexus.
    """

    def generate_nfvi_specific_nf_application(self):
        return NotImplementedError
