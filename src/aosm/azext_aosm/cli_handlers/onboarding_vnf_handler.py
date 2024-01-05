# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
from pathlib import Path

from azext_aosm.build_processors.arm_processor import AzureCoreArmBuildProcessor
from azext_aosm.build_processors.vhd_processor import VHDProcessor
from azext_aosm.common.constants import (
    ARTIFACT_LIST_FILENAME,
    MANIFEST_FOLDER_NAME,
    NF_DEFINITION_FOLDER_NAME,
    VNF_DEFINITION_TEMPLATE_FILENAME,
    VNF_MANIFEST_TEMPLATE_FILENAME,
    VNF_OUTPUT_FOLDER_FILENAME,
    VNF_INPUT_FILENAME, VNF_DEFINITION_FOLDER_NAME, VNF_BASE_TEMPLATE_FILENAME,
    BASE_FOLDER_NAME
)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.configuration_models.onboarding_vnf_input_config import (
    OnboardingVNFInputConfig,
)
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from azext_aosm.inputs.arm_template_input import ArmTemplateInput
from azext_aosm.inputs.vhd_file_input import VHDFileInput

from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler


class OnboardingVNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    config: OnboardingVNFInputConfig

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return VNF_INPUT_FILENAME

    @property
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        return VNF_OUTPUT_FOLDER_FILENAME

    def _get_config(self, input_config: dict = None) -> OnboardingVNFInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingVNFInputConfig(**input_config)

    def build_base_bicep(self):
        """ Build the base bicep file."""

        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(VNF_DEFINITION_FOLDER_NAME, VNF_BASE_TEMPLATE_FILENAME)
        bicep_contents = self._render_base_bicep_contents(
            template_path
        )
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, BASE_FOLDER_NAME), bicep_contents
        )
        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_base_parameters_contents())
        return bicep_file

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        acr_artifact_list = []

        # For each arm template, get list of artifacts
        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInput(
                artifact_name=arm_template.artifact_name,
                artifact_version=arm_template.version,
                default_config=None,
                template_path=Path(arm_template.file_path),
            )
            # TODO: generalise for nexus in nexus ready stories
            arm_processor = AzureCoreArmBuildProcessor(
                arm_input.artifact_name, arm_input
            )
            acr_artifact_list.extend(arm_processor.get_artifact_manifest_list())

        # Get list of vhd artifacts
        if not self.config.vhd.artifact_name:
            self.config.vhd.artifact_name = self.config.nf_name + "-vhd"
        vhd_processor = VHDProcessor(
            name=self.config.vhd.artifact_name,
            input_artifact=VHDFileInput(
                artifact_name=self.config.vhd.artifact_name,
                artifact_version=self.config.vhd.version,
                default_config=self._get_default_config(self.config.vhd),
                file_path=self.config.vhd.file_path,
                blob_sas_uri=self.config.vhd.blob_sas_url,
            ),
        )
        sa_artifact_list = vhd_processor.get_artifact_manifest_list()

        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(VNF_DEFINITION_FOLDER_NAME, VNF_MANIFEST_TEMPLATE_FILENAME)
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, acr_artifact_list, sa_artifact_list
        )
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME),
            bicep_contents,
        )
        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_manifest_parameters_contents())

        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        artifact_list = []
        # For each arm template, get list of artifacts and combine
        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInput(
                artifact_name=arm_template.artifact_name,
                artifact_version=arm_template.version,
                default_config=None,
                template_path=arm_template.file_path,
            )
            # TODO: generalise for nexus in nexus ready stories
            arm_processor = AzureCoreArmBuildProcessor(
                arm_input.artifact_name, arm_input
            )
            (artifacts, files) = arm_processor.get_artifact_details()
            if artifacts not in artifact_list:
                artifact_list.extend(artifacts)

        # Get list of vhd artifacts and combine
        if not self.config.vhd.artifact_name:
            self.config.vhd.artifact_name = self.config.nf_name + "-vhd"

        vhd_processor = VHDProcessor(
            name=self.config.vhd.artifact_name,
            input_artifact=VHDFileInput(
                artifact_name=self.config.vhd.artifact_name,
                artifact_version=self.config.vhd.version,
                default_config=self._get_default_config(self.config.vhd),
                file_path=self.config.vhd.file_path,
                blob_sas_uri=self.config.vhd.blob_sas_url,
            ),
        )
        (artifacts, files) = vhd_processor.get_artifact_details()
        if artifacts not in artifact_list:
            artifact_list.extend(artifacts)

        # Generate Artifact Element with artifact list (of arm template and vhd images)
        return ArtifactDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        acr_nf_application_list = []
        supporting_files = []
        schema_properties = {}

        # For each arm template, generate nf application
        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInput(
                artifact_name=arm_template.artifact_name,
                artifact_version=arm_template.version,
                default_config=None,
                template_path=arm_template.file_path,
            )
            # TODO: generalise for nexus in nexus ready stories
            # Generate NF Application and append to list of nf applications
            arm_processor = AzureCoreArmBuildProcessor(
                arm_input.artifact_name, arm_input
            )
            nf_application = arm_processor.generate_nf_application()
            acr_nf_application_list.append(nf_application)

            # Generate deploymentParameters schema properties
            params_schema = arm_processor.generate_params_schema()
            schema_properties.update(params_schema)
            
            # Generate local file for template_parameters + add to supporting files list
            template_params = (
                nf_application.deploy_parameters_mapping_rule_profile.template_mapping_rule_profile.template_parameters
            )
            template_parameters_file = LocalFileBuilder(
                Path(
                    VNF_OUTPUT_FOLDER_FILENAME,
                    NF_DEFINITION_FOLDER_NAME,
                    "templateParameters.json",
                ),
                json.dumps(template_params, indent=4),
            )
            supporting_files.append(template_parameters_file)

        # For vhd image, generate nf application
        if not self.config.vhd.artifact_name:
            self.config.vhd.artifact_name = self.config.nf_name + "-vhd"
        vhd_processor = VHDProcessor(
            name=self.config.vhd.artifact_name,
            input_artifact=VHDFileInput(
                artifact_name=self.config.vhd.artifact_name,
                artifact_version=self.config.vhd.version,
                file_path=self.config.vhd.file_path,
                default_config=self._get_default_config(self.config.vhd),
                blob_sas_uri=self.config.vhd.blob_sas_url,
            ),
        )
        # Generate NF Application
        nf_application = vhd_processor.generate_nf_application()

        # Generate local file for vhd_parameters
        vhd_params = nf_application.deploy_parameters_mapping_rule_profile.vhd_image_mapping_rule_profile.user_configuration
        vhd_params_file = LocalFileBuilder(
            Path(
                VNF_OUTPUT_FOLDER_FILENAME,
                NF_DEFINITION_FOLDER_NAME,
                "vhdParameters.json",
            ),
            vhd_params,
        )
        supporting_files.append(vhd_params_file)

        # Create bicep contents using vnf defintion j2 template
        template_path = self._get_template_path(VNF_DEFINITION_FOLDER_NAME, VNF_DEFINITION_TEMPLATE_FILENAME)
        bicep_contents = self._render_definition_bicep_contents(
            template_path, acr_nf_application_list, nf_application
        )

        # Create a bicep element + add its supporting files (deploymentParameters, vhdParameters and templateParameters)
        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME),
            bicep_contents,
        )
        for supporting_file in supporting_files:
            bicep_file.add_supporting_file(supporting_file)

        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_definition_parameters_contents())

        # Add the deploymentParameters schema file
        bicep_file.add_supporting_file(
            self._render_deployment_params_schema(schema_properties, VNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME)
        )
        return bicep_file

    def _render_base_parameters_contents(self):
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "saArtifactStoreName": {"value": self.config.blob_artifact_store_name},
                "nfDefinitionGroup": {"value": self.config.nf_name}
            },
        }

        return LocalFileBuilder(
            Path(
                VNF_OUTPUT_FOLDER_FILENAME,
                BASE_FOLDER_NAME,
                "deploy.parameters.json",
            ),
            json.dumps(params_content, indent=4),
        )

    def _render_manifest_parameters_contents(self):
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "acrManifestName": {
                    "value": self.config.acr_artifact_store_name + "-manifest"
                },
                "saArtifactStoreName": {"value": self.config.blob_artifact_store_name},
                "saManifestName": {
                    "value": self.config.blob_artifact_store_name + "-manifest"
                },
            },
        }

        return LocalFileBuilder(
            Path(
                VNF_OUTPUT_FOLDER_FILENAME,
                MANIFEST_FOLDER_NAME,
                "deploy.parameters.json",
            ),
            json.dumps(params_content, indent=4),
        )

    def _render_definition_parameters_contents(self):
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "saArtifactStoreName": {"value": self.config.blob_artifact_store_name},
                "nfDefinitionGroup": {"value": self.config.nf_name},
                "nfDefinitionVersion": {"value": self.config.version},
            },
        }
        return LocalFileBuilder(
            Path(
                VNF_OUTPUT_FOLDER_FILENAME,
                NF_DEFINITION_FOLDER_NAME,
                "deploy.parameters.json",
            ),
            json.dumps(params_content, indent=4),
        )

    def _get_default_config(self, vhd):
        default_config = {}
        if vhd.image_disk_size_GB:
            default_config.update({'image_disk_size_GB': vhd.image_disk_size_GB})
        else:
            # Default to V1 if not specified
            default_config.update({'image_disk_size_GB': 'V1'})
        if vhd.image_hyper_v_generation:
            default_config.update(
                {'image_hyper_v_generation': vhd.image_hyper_v_generation}
            )
        if vhd.image_api_version:
            default_config.update({'image_api_version': vhd.image_api_version})
        return default_config
