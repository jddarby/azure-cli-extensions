# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from pathlib import Path
from azext_aosm.common.constants import (
    VNF_DEFINITION_TEMPLATE_FILENAME,
    VNF_MANIFEST_TEMPLATE_FILENAME,
    VNF_OUTPUT_FOLDER_FILENAME,
    ARTIFACT_LIST_FILENAME,
    MANIFEST_FOLDER_NAME,
    NF_DEFINITION_FOLDER_NAME,
)
from azext_aosm.configuration_models.onboarding_vnf_input_config import (
    OnboardingVNFInputConfig,
)
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.common.artifact import LocalFileACRArtifact
from src.aosm.azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)

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

from ..build_processors.arm_processor import BaseArmBuildProcessor
from ..input_artifacts.arm_template_input_artifact import ArmTemplateInputArtifact


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
            # arm_input = ArmTemplateInputArtifact(
            #     artifact_name=arm_template.artifact_name,
            #     artifact_version=arm_template.version,
            #     artifact_path=arm_template.file_path)
            # # We use the aritfact name
            # processor = BaseArmBuildProcessor(arm_input.artifact_name, arm_input)
            # test = processor.get_artifact_manifest_list()
            # print("test", test)
            acr_artifact_list.append(
                ManifestArtifactFormat(
                    artifact_name=arm_template.artifact_name,
                    artifact_type="ArmTemplate",
                    artifact_version=arm_template.version,
                )
            )

        for vhd in self.config.vhd:
            #     if not vhd.artifact_name:
            #         vhd.artifact_name = self.config.nf_name + "-vhd"
            #     # Mocked for testing bicep
            sa_artifact_list.append(
                ManifestArtifactFormat(
                    artifact_name=vhd.artifact_name,
                    artifact_type="VHDImage",
                    artifact_version="2",
                )
            )

        template_path = self._get_template_path("vnf", VNF_MANIFEST_TEMPLATE_FILENAME)
        bicep_contents = self._write_manifest_bicep_contents(
            template_path, acr_artifact_list, sa_artifact_list
        )
        print(bicep_contents)
        return BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME),
            bicep_contents,
        )

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement

        artifact_list = []
        # TODO: Implement
        # for arm_template in self.config.arm_templates:
        #     processed_arm = BaseArmBuildProcessor()
        #     processed_arm.get_artifact_details()
        #     (artifacts, files) = processed_helm.get_artifact_details()
        #     if artifacts not in artifact_list:
        #         artifact_list.append(artifacts)

        # # For testing artifact builder works
        test_base_artifact = LocalFileACRArtifact(
            artifact_manifest=ManifestArtifactFormat(
                artifact_name="test",
                artifact_type="ArmTemplate",
                artifact_version="1.0.0",
            ),
            file_path=Path("test"),
        )
        artifact_list.append(test_base_artifact)
        # print(artifact_list)
        return ArtifactDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        # TODO: Remove testing code
        acr_nf_application_list = []
        sa_nf_application_list = []
        # # Mocking return of processor.generate_nf_application()
        # # We need: type, name, dependson, profile : {{ name, version}}

        for arm_template in self.config.arm_templates:
            #     processed_arm = BaseArmBuildProcessor()
            #     nf_application_list.append(processed_arm.generate_nf_application())
            nf_application = AzureCoreNetworkFunctionArmTemplateApplication(
                name="test",
                depends_on_profile=None,
                artifact_profile=AzureCoreArmTemplateArtifactProfile(
                    artifact_store=self.config.acr_artifact_store_name,
                    template_artifact_profile=ArmTemplateArtifactProfile(
                        template_name=arm_template.artifact_name,
                        template_version=arm_template.version,
                    ),
                ),
            )

            acr_nf_application_list.append(nf_application)
        # JORDAN: For testing (probably is the actual solution)
        for vhd in self.config.vhd:
            sa_nf_application_list.append(
                AzureCoreVhdImageArtifactProfile(
                    artifact_store=self.config.blob_artifact_store_name,
                    vhd_artifact_profile=VhdImageArtifactProfile(
                        vhd_name=vhd.artifact_name, vhd_version=vhd.version
                    ),
                )
            )

        template_path = self._get_template_path("vnf", VNF_DEFINITION_TEMPLATE_FILENAME)
        bicep_contents = self._write_definition_bicep_file(
            template_path, acr_nf_application_list, sa_nf_application_list
        )

        print(bicep_contents)
        return BicepDefinitionElementBuilder(
            Path(VNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME),
            bicep_contents,
        )
