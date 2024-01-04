# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
import json
from pathlib import Path

from azext_aosm.configuration_models.onboarding_nsd_input_config import (
    OnboardingNSDInputConfig,
)
from azext_aosm.vendored_sdks.models import (
    ManifestArtifactFormat,
    NetworkFunctionDefinitionVersion,
    NetworkFunctionDefinitionVersionPropertiesFormat,
)

from azext_aosm.build_processors.arm_processor import AzureCoreArmBuildProcessor
from azext_aosm.build_processors.nfd_processor import NFDProcessor

from .onboarding_nfd_base_handler import OnboardingBaseCLIHandler
from azext_aosm.common.constants import (
    ARTIFACT_LIST_FILENAME,
    MANIFEST_FOLDER_NAME,
    NSD_MANIFEST_TEMPLATE_FILENAME,
    NSD_DEFINITION_FOLDER_NAME,
    NSD_OUTPUT_FOLDER_FILENAME,
    # NSD_DEFINITION_TEMPLATE_FILENAME,
    NSD_MANIFEST_TEMPLATE_FILENAME,
    NSD_OUTPUT_FOLDER_FILENAME,
    NSD_MANIFEST_TEMPLATE_FILENAME,
    NSD_INPUT_FILENAME
)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.configuration_models.onboarding_nsd_input_config import (
    OnboardingNSDInputConfig,
)
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from azext_aosm.inputs.arm_template_input import ArmTemplateInput
from azext_aosm.inputs.nfd_input import NFDInput


class OnboardingNSDCLIHandler(OnboardingBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return NSD_INPUT_FILENAME

    @property
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        return NSD_OUTPUT_FOLDER_FILENAME

    def _get_config(self, input_config: dict = None) -> OnboardingNSDInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingNSDInputConfig(**input_config)

    def build_base_bicep(self):
        """Build the base bicep file."""
        # TODO: Implement
        raise NotImplementedError

    def build_manifest_bicep(self):
        """Build the manifest bicep file.

        Create ARM Template manifest as expected, but behaves differently for NFs:
        For each NF, we create one manifest per artifact
        and do not populate these manifests until publish, based on the params file

        """
        # Build artifact list for ArmTemplates
        artifact_list = []
        RET_artifact_list = []
        for resource_element in self.config.resource_element_templates:
            if resource_element.resource_element_type == "ArmTemplate":
                arm_input = ArmTemplateInput(
                    artifact_name=resource_element.properties.artifact_name,
                    artifact_version=resource_element.properties.version,
                    default_config=None,
                    template_path=Path(resource_element.properties.file_path),
                )
                # TODO: generalise for nexus in nexus ready stories
                arm_processor = AzureCoreArmBuildProcessor(
                    arm_input.artifact_name, arm_input
                )
                artifact_list.extend(arm_processor.get_artifact_manifest_list())
            # TODO: add this for artifact manifest and go to j2 template
            if resource_element.resource_element_type == "NF":
                # TODO: change artifact name and version to the nfd name and version
                nfd_input = NFDInput(
                    artifact_name=self.config.nsd_name,
                    artifact_version=self.config.nsd_version,
                    default_config=None,
                    network_function_definition=NetworkFunctionDefinitionVersion(
                        location="test",
                        tags=None,
                        properties=NetworkFunctionDefinitionVersionPropertiesFormat(description="test", deploy_parameters="wherefrom?"),
                    ),
                    arm_template_output_path=Path("test"),
                )
                nfd_processor = NFDProcessor(name=self.config.nsd_name, input_artifact=nfd_input)
                RET_artifact_list.extend(nfd_processor.get_artifact_manifest_list())
        # TODO: one artifact manifest
        template_path = self._get_template_path("nsd", NSD_MANIFEST_TEMPLATE_FILENAME)
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, artifact_list
        )
        print(bicep_contents)

        bicep_file = BicepDefinitionElementBuilder(
            Path(NSD_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME), bicep_contents
        )

        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_manifest_parameters_contents())
        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement
        # keep ordering, turn config into processor objects
        # same for arm templates as before
        # use nfd processor.get_Artifact_details
        
        raise NotImplementedError

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement

        # Add config group schema logic (from nsd_generator) as supporting file
        # mappings like elsewhere? nsd has single schema for each RET deploys, 
        # Write config mappings for each NF (processor.generateRET)
        # write the nf bicep file (nf template j2) - not ready, need to discuss w Jacob
        # write nsd bicep (contain cgs, nsdv)
        raise NotImplementedError

    def _render_manifest_parameters_contents(self):
        arm_template_names = []
        artifact_manifest_names = []

        # For each NF, create an arm template name and manifest name
        for resource_element in self.config.resource_element_templates:
            if resource_element.resource_element_type == "NF":
                arm_template_names.append(
                    f"{resource_element.properties.name}_nf_artifact"
                )
                print("arm", arm_template_names)
                sanitised_nf_name = (
                    f"{resource_element.properties.name.lower().replace('_','-')}"
                )
                sanitised_nsd_version = f"{self.config.nsd_version.replace('.', '-')}"
                artifact_manifest_names.append(
                    f"{sanitised_nf_name}-nf-acr-manifest-{sanitised_nsd_version}"
                )

        # Set the artifact version to be the same as the NSD version, so that they
        # don't get over written when a new NSD is published.
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "location": {"value": self.config.location},
            "publisherName": {"value": self.config.publisher_name},
            "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
            "acrManifestNames": {"value": artifact_manifest_names},
            "armTemplateNames": {"value": arm_template_names},
            "armTemplateVersion": {"value": self.config.nsd_version},
        }

        print(params_content)
        return LocalFileBuilder(
            Path(
                NSD_OUTPUT_FOLDER_FILENAME,
                MANIFEST_FOLDER_NAME,
                "deploy.parameters.json",
            ),
            json.dumps(params_content, indent=4),
        )

    def _render_config_schema_contents(self):

        cgs_contents = {
            "$schema": "https://json-schema.org/draft-07/schema#",
            # "title": self.config.cg_schema_name,
            # "type": "object",
            # "properties": properties,
            # "required": required,
            }
        return cgs_contents
