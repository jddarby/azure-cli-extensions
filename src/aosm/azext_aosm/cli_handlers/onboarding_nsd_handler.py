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

from azext_aosm.cli_handlers.onboarding_nfd_base_handler import OnboardingBaseCLIHandler
from azext_aosm.common.constants import (
    ARTIFACT_LIST_FILENAME,
    MANIFEST_FOLDER_NAME,
    NSD_MANIFEST_TEMPLATE_FILENAME,
    NSD_DEFINITION_FOLDER_NAME,
    NSD_OUTPUT_FOLDER_FILENAME,
    # NSD_DEFINITION_TEMPLATE_FILENAME,
    NSD_INPUT_FILENAME,
    BASE_FOLDER_NAME,
    NSD_BASE_TEMPLATE_FILENAME,
)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.json_builder import JSONDefinitionElementBuilder
from azext_aosm.inputs.arm_template_input import ArmTemplateInput
from azext_aosm.inputs.nfd_input import NFDInput
from azext_aosm.configuration_models.common_parameters_config import NSDCommonParametersConfig


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

    def _get_input_config(self, input_config: dict = None) -> OnboardingNSDInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingNSDInputConfig(**input_config)

    def _get_params_config(self, params_config: dict = None) -> NSDCommonParametersConfig:
        """Get the configuration for the command."""
        if params_config is None:
            params_config = {}
        return NSDCommonParametersConfig(**params_config)

    def build_base_bicep(self):
        """Build the base bicep file."""

        # Build base bicep contents, with bicep template
        template_path = self._get_template_path(
            NSD_DEFINITION_FOLDER_NAME, NSD_BASE_TEMPLATE_FILENAME
        )
        bicep_contents = self._render_base_bicep_contents(template_path)
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(NSD_OUTPUT_FOLDER_FILENAME, BASE_FOLDER_NAME), bicep_contents
        )
        # Add the accompanying parameters.json
        # bicep_file.add_supporting_file(self._render_base_parameters_contents())
        return bicep_file

    def build_manifest_bicep(self):
        """Build the manifest bicep file.

        Create ARM Template manifest as expected, but behaves differently for NFs:
        For each NF, we create one manifest per artifact
        and do not populate these manifests until publish, based on the params file

        """
        # Build artifact list for ArmTemplates
        artifact_list = []
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
                # TODO: change artifact name and version to the nfd name and version or justify why it was this in the first place
                nfd_input = NFDInput(
                    artifact_name=self.config.nsd_name,
                    artifact_version=self.config.nsd_version,
                    default_config=None,
                    network_function_definition=NetworkFunctionDefinitionVersion(
                        location="test",
                        tags=None,
                        properties=NetworkFunctionDefinitionVersionPropertiesFormat(
                            description="test", deploy_parameters=None
                        ),
                    ),
                    arm_template_output_path=Path("test"),
                )
                nfd_processor = NFDProcessor(
                    name=self.config.nsd_name, input_artifact=nfd_input
                )
                artifact_list.extend(nfd_processor.get_artifact_manifest_list())
        template_path = self._get_template_path(
            NSD_DEFINITION_FOLDER_NAME, NSD_MANIFEST_TEMPLATE_FILENAME
        )
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, artifact_list
        )

        bicep_file = BicepDefinitionElementBuilder(
            Path(NSD_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME), bicep_contents
        )
        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        # Build artifact list for ArmTemplates
        artifact_list = []
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
                (artifacts, files) = arm_processor.get_artifact_details()
                if artifacts not in artifact_list:
                    artifact_list.extend(artifacts)
            if resource_element.resource_element_type == "NF":
                # TODO: change artifact name and version to the nfd name and version or justify why it was this in the first place
                nfd_input = NFDInput(
                    artifact_name=self.config.nsd_name,
                    artifact_version=self.config.nsd_version,
                    default_config=None,
                    network_function_definition=NetworkFunctionDefinitionVersion(
                        # TODO: is location the location of the nf (if this how do we get it?) or nsd?
                        location="test",
                        tags=None,
                        properties=NetworkFunctionDefinitionVersionPropertiesFormat(
                            description="test", deploy_parameters=None
                        ),
                    ),
                    arm_template_output_path=Path("test"),
                )
                nfd_processor = NFDProcessor(
                    name=self.config.nsd_name, input_artifact=nfd_input
                )
                (artifacts, files) = nfd_processor.get_artifact_details()

                if artifacts not in artifact_list:
                    artifact_list.extend(artifacts)
        # Generate Artifact Element with artifact list (of arm template and vhd images)
        return ArtifactDefinitionElementBuilder(
            Path(NSD_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self, aosm_client):
        """Build the resource bicep file."""
        # TODO: Implement

        bicep_contents = {}
        schema_properties = {}
        nf_names = []
        print(bicep_contents)

        for resource_element in self.config.resource_element_templates:
            if resource_element.resource_element_type == "NF":
                # TODO: change artifact name and version to the nfd name and version or justify why it was this in the first place

                # Get nfdv information from azure using config from input file
                nfdv_object = self._get_nfdv(aosm_client, resource_element.properties)
                print("nfdv", nfdv_object)
                nfd_input = NFDInput(
                    artifact_name=self.config.nsd_name,
                    artifact_version=self.config.nsd_version,
                    default_config=None,
                    network_function_definition=NetworkFunctionDefinitionVersion(
                        # TODO: is location the location of the nf (if this how do we get it?) or nsd?
                        location="test",
                        tags=None,
                        properties=NetworkFunctionDefinitionVersionPropertiesFormat(
                            description="test", deploy_parameters=None
                        ),
                    ),
                    arm_template_output_path=Path("test"),
                )
                nfd_processor = NFDProcessor(
                    name=resource_element.properties.name, input_artifact=nfd_input
                )

                # Generate RET
                nf_ret = nfd_processor.generate_resource_element_template()
                # nf_ret.configuration.

                # Generate deploymentParameters schema properties
                # JORDAN TODO: check this includes the name of the deploymentParams too?
                # TODO: test this
                params_schema = nfd_processor.generate_params_schema()
                schema_properties.update(params_schema)

                # List of NF RET names, for adding to required part of CGS
                nf_names.append(resource_element.properties.name)


        # Generate the nsd bicep file
        bicep_file = BicepDefinitionElementBuilder(
            Path(NSD_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME), bicep_contents
        )
        # Add the accompanying cgs
        bicep_file.add_supporting_file(self._render_config_group_schema_contents(schema_properties, nf_names))

        # Add the accomanying NF biceps
        # for files in nf_files:
        #    bicep_file.add_supporting_file()
        return bicep_file

        # 1.Add config group schema logic (from nsd_generator) as supporting file
        # mappings like elsewhere? nsd has single schema for each RET deploys,
        # 2.Write config mappings for each NF (processor.generateRET)
        # 3.write the nf bicep file (nf template j2) - not ready, need to discuss w Jacob
        # 4.write nsd bicep (contain cgs, nsdv)

    def build_common_parameters_json(self):
        # TODO: add common params for build resource bicep
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "publisherResourceGroupName": {
                    "value": self.config.publisher_resource_group_name
                },
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "acrManifestName": {
                    "value": self.config.acr_artifact_store_name + "-manifest"
                },
                "nsDesignGroup": {"value": self.config.nsd_name},
            },
        }
        print(params_content)
        base_file = JSONDefinitionElementBuilder(
            Path(NSD_OUTPUT_FOLDER_FILENAME), json.dumps(params_content, indent=4)
        )
        return base_file

    def _render_config_group_schema_contents(self, complete_schema, nf_names):
        params_content = {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "title": "ubuntu_ConfigGroupSchema",
            "type": "object",
            "properties": complete_schema,
            "managedIdentity": {
                "type": "string",
                "description": "The managed identity to use to deploy NFs within this SNS.  \
                    This should be of the form '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}. \
                    If you wish to use a system assigned identity, set this to a blank string.",
            },
            # TODO: add names of the schemas ie ubuntu-vm-nfdg
            "required": [nf_names, "managedIdentity"],
        }
        print(params_content)
        return LocalFileBuilder(
            Path(
                NSD_OUTPUT_FOLDER_FILENAME,
            NSD_DEFINITION_FOLDER_NAME,
                "test-cgs.json",
            ),
            json.dumps(params_content, indent=4),
        )

    # def _render_manifest_parameters_contents(self):
    #     arm_template_names = []
    #     artifact_manifest_names = []
    #     # TODO: change manifest name
    #     # For each NF, create an arm template name and manifest name
    #     for resource_element in self.config.resource_element_templates:
    #         if resource_element.resource_element_type == "NF":
    #             arm_template_names.append(
    #                 f"{resource_element.properties.name}_nf_artifact"
    #             )
    #             sanitised_nf_name = (
    #                 f"{resource_element.properties.name.lower().replace('_','-')}"
    #             )
    #             sanitised_nsd_version = f"{self.config.nsd_version.replace('.', '-')}"
    #             artifact_manifest_names.append(
    #                 f"{sanitised_nf_name}-nf-acr-manifest-{sanitised_nsd_version}"
    #             )

    #     # Set the artifact version to be the same as the NSD version, so that they
    #     # don't get over written when a new NSD is published.
    #     params_content = {
    #         "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
    #         "contentVersion": "1.0.0.0",
    #         "parameters": {
    #             "location": {"value": self.config.location},
    #             "publisherName": {"value": self.config.publisher_name},
    #             "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
    #             "acrManifestName": {
    #                 "value": self.config.acr_artifact_store_name + "-manifest"
    #             },
    #             "armTemplateVersion": {"value": self.config.nsd_version},
    #         },
    #     }

    #     # print(params_content)
    #     return LocalFileBuilder(
    #         Path(
    #             NSD_OUTPUT_FOLDER_FILENAME,
    #             MANIFEST_FOLDER_NAME,
    #             "deploy.parameters.json",
    #         ),
    #         json.dumps(params_content, indent=4),
    #     )
    def _render_config_schema_contents(self):
        cgs_contents = {
            "$schema": "https://json-schema.org/draft-07/schema#",
            # "title": self.config.cg_schema_name,
            # "type": "object",
            # "properties": properties,
            # "required": required,
        }
        return cgs_contents

    def _get_nfdv(self, aosm_client, nf_properties) -> NetworkFunctionDefinitionVersion:
        """Get the existing NFDV resource object."""
        print(
            f"Reading existing NFDV resource object {nf_properties.version} from group {nf_properties.name}"
        )
        nfdv_object = aosm_client.network_function_definition_versions.get(
            resource_group_name=nf_properties.publisher_resource_group,
            publisher_name=nf_properties.publisher,
            network_function_definition_group_name=nf_properties.name,
            network_function_definition_version_name=nf_properties.version,
        )
        return nfdv_object
