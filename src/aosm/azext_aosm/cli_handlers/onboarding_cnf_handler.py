# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from azext_aosm.configuration_models.onboarding_cnf_input_config import OnboardingCNFInputConfig


class OnboardingCNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    def _get_config(self, input_json_path: str | None = None) -> OnboardingCNFInputConfig:
        """Get the configuration for the command."""
        return OnboardingCNFInputConfig(**self._read_config_from_file(input_json_path))

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        # TODO: Implement
        pass

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement
        pass

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        pass
