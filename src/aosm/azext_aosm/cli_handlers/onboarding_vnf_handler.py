# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from azext_aosm.configuration_models.onboarding_vnf_input_config import (
    OnboardingVNFInputConfig,
)
from azext_aosm.vendored_sdks.models import (
    ManifestArtifactFormat,
    NetworkFunctionApplication,
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

        # for arm_template in self.config.arm_templates:
        #     # arm_input = ArmTemplateInputArtifact(
        #     #     artifact_name=arm_template.artifact_name,
        #     #     artifact_version=arm_template.version,
        #     #     artifact_path=arm_template.file_path)
        #     # We use the aritfact name
        #     # processor = BaseArmBuildProcessor(arm_input.artifact_name, arm_input)
        #     # processor.get_artifact_manifest_list()
        #     acr_artifact_list.append(
        #         ManifestArtifactFormat(
        #             artifact_name="testarm",
        #             artifact_type="ArmTemplate",
        #             artifact_version="1",
        #         )
        #     )

        # for vhd in self.config.vhd:
        #     if not vhd.artifact_name:
        #         vhd.artifact_name = self.config.nf_name + "-vhd"
        #     # Mocked for testing bicep
        #     sa_artifact_list.append(
        #         ManifestArtifactFormat(
        #             artifact_name=vhd.artifact_name,
        #             artifact_type="VHDImage",
        #             artifact_version="2",
        #         )
        #     )

        template_path = self._get_template_path("vnfartifactmanifest.bicep.j2")
        bicep_contents = self._write_manifest_bicep_file(
            template_path, acr_artifact_list, sa_artifact_list
        )
        print(bicep_contents)
        return bicep_contents

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement
        raise NotImplementedError

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        # TODO: Remove testing code
        acr_nf_application_list = []
        sa_nf_application_list = []
        # # Mocking return of processor.generate_nf_application()
        # # We need: type, name, dependson, profile : {{ name, version}}

        # for arm_template in self.config.arm_templates:
            # test_nf_application = (
            #     # arm_template.artifact_name,
            #     # arm_template.version,
            #     NetworkFunctionApplication(name="testname", depends_on_profile=None)
            # )
            # print(test_nf_application.name)
            # acr_nf_application_list.append({'name':'test', test_nf_application})
        # for vhd in self.config.vhd:
            # nf_application_list.append(processor.get_artifact_manifest_list())
            # sa_nf_application_list.append(
                # {
                #     vhd.artifact_name,
                #     vhd.version,
                # NetworkFunctionApplication(name="", depends_on_profile=None),
                # }
            # )

        template_path = self._get_template_path("vnfdefinition.bicep.j2")
        bicep_contents = self._write_definition_bicep_file(
            template_path, acr_nf_application_list, sa_nf_application_list
        )

        print(bicep_contents)
        return bicep_contents

