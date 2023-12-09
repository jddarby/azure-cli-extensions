# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from azext_aosm.configuration_models.onboarding_vnf_input_config import OnboardingVNFInputConfig
from ..build_processors.arm_processor import BaseArmBuildProcessor
from .. input_artifacts.arm_template_input_artifact import ArmTemplateInputArtifact


class OnboardingVNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    config: OnboardingVNFInputConfig

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return "vnf-input.jsonc"

    def _get_config(self, input_config: dict = {}) -> OnboardingVNFInputConfig:
        """Get the configuration for the command."""
        return OnboardingVNFInputConfig(**input_config)

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        # Work in progress. TODO: Finish
        for arm_template in self.config.arm_templates:
            arm_input = ArmTemplateInputArtifact(
                artifact_name=arm_template.name,
                artifact_version=arm_template.version,
                artifact_path=arm_template.file_path)
            # We use the aritfact name
            processor = BaseArmBuildProcessor()
            processor.get_artifact_manifest_list()
        pass

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement
        pass

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        pass
