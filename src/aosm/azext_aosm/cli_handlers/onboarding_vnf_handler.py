# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
from pathlib import Path
from knack.log import get_logger
from azext_aosm.build_processors.arm_processor import AzureCoreArmBuildProcessor, BaseArmBuildProcessor
from azext_aosm.build_processors.vhd_processor import VHDProcessor
from azext_aosm.common.constants import (
    ARTIFACT_LIST_FILENAME,
    MANIFEST_FOLDER_NAME,
    NF_DEFINITION_FOLDER_NAME,
    VNF_DEFINITION_TEMPLATE_FILENAME,
    VNF_MANIFEST_TEMPLATE_FILENAME,
    VNF_OUTPUT_FOLDER_FILENAME,
    VNF_INPUT_FILENAME,
    VNF_DEFINITION_FOLDER_NAME,
    VNF_BASE_TEMPLATE_FILENAME,
    BASE_FOLDER_NAME,
)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.configuration_models.onboarding_vnf_input_config import (
    OnboardingVNFInputConfig,
)
from azext_aosm.configuration_models.common_parameters_config import VNFCommonParametersConfig
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.json_builder import (
    JSONDefinitionElementBuilder,
)
from azext_aosm.inputs.arm_template_input import ArmTemplateInput
from azext_aosm.inputs.vhd_file_input import VHDFileInput

from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler

logger = get_logger(__name__)


class OnboardingVNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    # config: OnboardingVNFInputConfig

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return VNF_INPUT_FILENAME

    @property
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        return VNF_OUTPUT_FOLDER_FILENAME

    def _get_input_config(self, input_config: dict = None) -> OnboardingVNFInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingVNFInputConfig(**input_config)

    def _get_params_config(self, params_config: dict = None) -> VNFCommonParametersConfig:
        """Get the configuration for the command."""
        if params_config is None:
            params_config = {}
        return VNFCommonParametersConfig(**params_config)

    def _get_processor_list(self):
        processor_list = []
        # for each arm template, instantiate arm processor
        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInput(
                artifact_name=arm_template.artifact_name,
                artifact_version=arm_template.version,
                default_config=None,
                template_path=Path(arm_template.file_path),
            )
            # TODO: generalise for nexus in nexus ready stories
            processor_list.append(AzureCoreArmBuildProcessor(
                arm_input.artifact_name, arm_input
            ))
    
        # Instantiate vhd processor
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
        processor_list.append(vhd_processor)
        return processor_list

    def build_base_bicep(self):
        """Build the base bicep file."""

        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(
            VNF_DEFINITION_FOLDER_NAME, VNF_BASE_TEMPLATE_FILENAME
        )
        bicep_contents = self._render_base_bicep_contents(template_path)
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, BASE_FOLDER_NAME), bicep_contents
        )
        return bicep_file

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        acr_artifact_list = []

        logger.info("Creating artifact manifest bicep")

        for processor in self.processors:
            if isinstance(processor, BaseArmBuildProcessor):
                acr_artifact_list.extend(processor.get_artifact_manifest_list())
                logger.debug(
                    "Created list of artifacts from %s arm template(s) provided: %s",
                    len(self.config.arm_templates),
                    acr_artifact_list,
                )
            elif isinstance(processor, VHDProcessor):
                sa_artifact_list = processor.get_artifact_manifest_list()
                logger.debug(
                    "Created list of artifacts from vhd image provided: %s", sa_artifact_list
                )

        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(
            VNF_DEFINITION_FOLDER_NAME, VNF_MANIFEST_TEMPLATE_FILENAME
        )
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, acr_artifact_list, sa_artifact_list
        )
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME),
            bicep_contents,
        )

        logger.info("Created artifact manifest bicep element")
        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        logger.info("Creating artifacts list for artifacts.json")
        artifact_list = []
        # For each arm template, get list of artifacts and combine
        for processor in self.processors:
            (artifacts, files) = processor.get_artifact_details()
            if artifacts not in artifact_list:
                artifact_list.extend(artifacts)
        logger.debug(
            "Created list of artifact details from %s arm template(s) and the vhd image provided: %s",
            len(self.config.arm_templates),
            artifact_list,
        )

        # Generate Artifact Element with artifact list (of arm template and vhd images)
        return ArtifactDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        logger.info("Creating artifacts list for artifacts.json")
        acr_nf_application_list = []
        supporting_files = []
        schema_properties = {}

        # For each arm template, generate nf application
        for processor in self.processors:
            if isinstance(processor, BaseArmBuildProcessor):
                nf_application = processor.generate_nf_application()
                acr_nf_application_list.append(nf_application)
                logger.debug("Created nf application %s", nf_application.name)

                # Generate deploymentParameters schema properties
                params_schema = processor.generate_params_schema()
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
                logger.info(
                    "Created templatateParameters as supporting file for nfDefinition bicep"
                )
            elif isinstance(processor, VHDProcessor):
                # Generate NF Application
                nf_application = processor.generate_nf_application()

                # Generate local file for vhd_parameters
                vhd_params = (
                    nf_application.deploy_parameters_mapping_rule_profile.vhd_image_mapping_rule_profile.user_configuration
                )
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
        template_path = self._get_template_path(
            VNF_DEFINITION_FOLDER_NAME, VNF_DEFINITION_TEMPLATE_FILENAME
        )
        bicep_contents = self._render_definition_bicep_contents(
            template_path, acr_nf_application_list, nf_application
        )

        # Create a bicep element
        # + add its supporting files (deploymentParameters, vhdParameters and templateParameters)
        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME),
            bicep_contents,
        )
        for supporting_file in supporting_files:
            bicep_file.add_supporting_file(supporting_file)

        # Add the deploymentParameters schema file
        bicep_file.add_supporting_file(
            self._render_deployment_params_schema(
                schema_properties, VNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME
            )
        )
        return bicep_file

    def build_common_parameters_json(self):
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
                "saArtifactStoreName": {"value": self.config.blob_artifact_store_name},
                "acrManifestName": {
                    "value": self.config.acr_artifact_store_name + "-manifest"
                },
                "saManifestName": {
                    "value": self.config.blob_artifact_store_name + "-manifest"
                },
                "nfDefinitionGroup": {"value": self.config.nf_name},
                "nfDefinitionVersion": {"value": self.config.version},
            },
        }
        base_file = JSONDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME), json.dumps(params_content, indent=4)
        )
        return base_file

    def _get_default_config(self, vhd):
        default_config = {}
        if vhd.image_disk_size_GB:
            default_config.update({"image_disk_size_GB": vhd.image_disk_size_GB})
        else:
            # Default to V1 if not specified
            default_config.update({"image_disk_size_GB": "V1"})
        if vhd.image_hyper_v_generation:
            default_config.update(
                {"image_hyper_v_generation": vhd.image_hyper_v_generation}
            )
        if vhd.image_api_version:
            default_config.update({"image_api_version": vhd.image_api_version})
        return default_config
