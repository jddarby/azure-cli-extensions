# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
from .onboarding_nfd_base_handler import OnboardingBaseCLIHandler
from azext_aosm.configuration_models.onboarding_nsd_input_config import NetworkFunctionPropertiesConfig, OnboardingNSDInputConfig


class OnboardingNSDCLIHandler(OnboardingBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return "nsd-input.jsonc"

    def _get_config(self, input_config: dict = {}) -> OnboardingNSDInputConfig:
        """Get the configuration for the command."""
        return OnboardingNSDInputConfig(**input_config)


    def build_base_bicep(self):
        """Build the base bicep file."""
        # TODO: Implement
        pass

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
