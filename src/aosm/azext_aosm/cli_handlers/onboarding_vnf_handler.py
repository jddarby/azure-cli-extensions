# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from pathlib import Path
import json
from azext_aosm.common.constants import (
    VNF_DEFINITION_TEMPLATE_FILENAME,
    VNF_MANIFEST_TEMPLATE_FILENAME,
    VNF_OUTPUT_FOLDER_FILENAME,
    ARTIFACT_LIST_FILENAME,
    MANIFEST_FOLDER_NAME,
    NF_DEFINITION_FOLDER_NAME,
)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.configuration_models.onboarding_vnf_input_config import (
    OnboardingVNFInputConfig,
)
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.common.artifact import LocalFileACRArtifact
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from src.aosm.azext_aosm.input_artifacts.vhd_file import VHDFile
from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler

from azext_aosm.vendored_sdks.models import (
    ManifestArtifactFormat,
    NetworkFunctionApplication,
    AzureCoreVhdImageArtifactProfile,
    VhdImageArtifactProfile,
    AzureCoreNetworkFunctionArmTemplateApplication,
    AzureCoreArmTemplateArtifactProfile,
    ArmTemplateArtifactProfile,
)

from azext_aosm.build_processors.arm_processor import BaseArmBuildProcessor, AzureCoreArmBuildProcessor
from azext_aosm.build_processors.vhd_processor import VHDProcessor
from azext_aosm.input_artifacts.arm_template_input_artifact import (
    ArmTemplateInputArtifact,
)


class OnboardingVNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    config: OnboardingVNFInputConfig

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return "vnf-input.jsonc"

    @property
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        return VNF_OUTPUT_FOLDER_FILENAME

    def _get_config(self, input_config: dict = {}) -> OnboardingVNFInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingVNFInputConfig(**input_config)

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        # Work in progress. TODO: Finish
        acr_artifact_list = []
        sa_artifact_list = []

        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInputArtifact(
                artifact_name=arm_template.artifact_name,
                artifact_version=arm_template.version,
                artifact_path=arm_template.file_path)
            # TODO: generalise for nexus in nexus ready stories
            arm_processor = AzureCoreArmBuildProcessor(arm_input.artifact_name, arm_input)
            acr_artifact_list.extend(arm_processor.get_artifact_manifest_list())
            # acr_artifact_list.append(
            #     ManifestArtifactFormat(
            #         artifact_name=arm_template.artifact_name,
            #         artifact_type="ArmTemplate",
            #         artifact_version=arm_template.version,
            #     )
            # )

        for vhd in self.config.vhd:
            if not vhd.artifact_name:
                vhd.artifact_name = self.config.nf_name + "-vhd"
            vhd_processor = VHDProcessor(
                name=vhd.artifact_name,
                artifact_store=self.config.blob_artifact_store_name,
                input_artifact=VHDFile(
                    artifact_name=vhd.artifact_name, artifact_version=vhd.version
                )
            )
            sa_artifact_list.extend(vhd_processor.get_artifact_manifest_list())
            print("SA", sa_artifact_list)
            #     # Mocked for testing bicep
            # sa_artifact_list.append(
            #     ManifestArtifactFormat(
            #         artifact_name=vhd.artifact_name,
            #         artifact_type="VHDImage",
            #         artifact_version="2",
            #     )
            # )

        template_path = self._get_template_path("vnf", VNF_MANIFEST_TEMPLATE_FILENAME)
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, acr_artifact_list, sa_artifact_list
        )

        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME),
            bicep_contents,
        )

        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_manifest_parameters_contents())

        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement

        artifact_list = []
        # TODO: Implement
        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInputArtifact(
                artifact_name=arm_template.artifact_name,
                artifact_version=arm_template.version,
                artifact_path=arm_template.file_path)
            # TODO: generalise for nexus in nexus ready stories
            arm_processor = AzureCoreArmBuildProcessor(arm_input.artifact_name, arm_input)
            (artifacts, files) = arm_processor.get_artifact_details()
            if artifacts not in artifact_list:
                artifact_list.append(artifacts)

        # # For testing artifact builder works
        # test_base_artifact = LocalFileACRArtifact(
        #     artifact_manifest=ManifestArtifactFormat(
        #         artifact_name="test",
        #         artifact_type="ArmTemplate",
        #         artifact_version="1.0.0",
        #     ),
        #     file_path=Path("test"),
        # )
        # artifact_list.append(test_base_artifact)

        # for vhd in self.config.vhd:
        #     if not vhd.artifact_name:
        #         vhd.artifact_name = self.config.nf_name + "-vhd"
        #     vhd_processor = VHDProcessor(
        #         name=vhd.artifact_name,
        #         artifact_store=self.config.blob_artifact_store_name,
        #         input_artifact=VHDFile(
        #             artifact_name=vhd.artifact_name, artifact_version=vhd.version
        #         )
        #     )
        #     (artifact,files) = vhd_processor.get_artifact_details()
        #     if artifacts not in artifact_list:
        #         artifact_list.append(artifacts)
            
        # print(artifact_list)
        return ArtifactDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Remove testing code
        acr_nf_application_list = []
        sa_nf_application_list = []

        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInputArtifact(
                artifact_name=arm_template.artifact_name,
                artifact_version=arm_template.version,
                artifact_path=arm_template.file_path)
            # TODO: generalise for nexus in nexus ready stories
            arm_processor = AzureCoreArmBuildProcessor(arm_input.artifact_name, arm_input)
            acr_nf_application_list.append(arm_processor.generate_nf_application())
            
            # nf_application = AzureCoreNetworkFunctionArmTemplateApplication(
            #     name="test",
            #     depends_on_profile=None,
            #     artifact_profile=AzureCoreArmTemplateArtifactProfile(
            #         artifact_store=self.config.acr_artifact_store_name,
            #         template_artifact_profile=ArmTemplateArtifactProfile(
            #             template_name=arm_template.artifact_name,
            #             template_version=arm_template.version,
            #         ),
            #     ),
            # )

            # acr_nf_application_list.append(nf_application)

        for vhd in self.config.vhd:
            if not vhd.artifact_name:
                vhd.artifact_name = self.config.nf_name + "-vhd"
            vhd_processor = VHDProcessor(
                name=vhd.artifact_name,
                artifact_store=self.config.blob_artifact_store_name,
                input_artifact=VHDFile(
                    artifact_name=vhd.artifact_name, artifact_version=vhd.version
                )
            )
            sa_nf_application_list.append(vhd_processor.generate_nf_application())
        # JORDAN: For testing (add get nf application for workingprobably is the actual solution)
        # for vhd in self.config.vhd:
        #     sa_nf_application_list.append(
        #         AzureCoreVhdImageArtifactProfile(
        #             artifact_store=self.config.blob_artifact_store_name,
        #             vhd_artifact_profile=VhdImageArtifactProfile(
        #                 vhd_name=vhd.artifact_name, vhd_version=vhd.version
        #             ),
        #         )
        #     )

        template_path = self._get_template_path("vnf", VNF_DEFINITION_TEMPLATE_FILENAME)
        bicep_contents = self._write_definition_bicep_file(
            template_path, acr_nf_application_list, sa_nf_application_list
        )

        bicep_file = BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME),
            bicep_contents,
        )
        
        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_definition_parameters_contents())

        return bicep_file

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
