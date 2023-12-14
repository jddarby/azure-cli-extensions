# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from azext_aosm.configuration_models.onboarding_vnf_input_config import (
    OnboardingVNFInputConfig,
)


class OnboardingVNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return "vnf-input.jsonc"

    def _get_config(self, input_config: dict = None) -> OnboardingVNFInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingVNFInputConfig(**input_config)

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        # TODO: Implement
        raise NotImplementedError

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement
        raise NotImplementedError

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        raise NotImplementedError
