# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod

from configuration_models.onboarding_base_input_config import OnboardingBaseInputConfig


class OnboardingBaseCLIHandler(ABC):
    """Abstract base class for CLI handlers."""
    config: OnboardingBaseInputConfig

    def __init__(self, input_json_path: str | None = None):
        # Config may be optional (to generate blank config file)

        config_dict = self._read_config_from_file(input_json_path) if input_json_path else {}
        self.config = self._get_config(config_dict)

    def _read_config_from_file(self, input_json_path: str) -> dict:
        """Read the input JSONC file."""
        # TODO: Implement
        pass

    @abstractmethod
    def _get_config(self, input_config: dict = {}) -> OnboardingBaseInputConfig:
        """Get the configuration for the command."""
        raise NotImplementedError

    def _write_config_to_file(self, config: OnboardingBaseInputConfig, output_file: str):
        """Write the configuration to a file."""
        # TODO: Implement by converting config to JSONC
        pass

    def generate_config(self, output_file: str = "input.jsonc"):
        """Generate the configuration file for the command."""
        # TODO: Make file name depend on class via property
        self._write_config_to_file(self.config, output_file)

    def build(self, input_json_path: str):
        """Build the definition."""
        self.build_base_bicep()
        self.build_manifest_bicep()
        self.build_artifact_list()
        self.build_resource_bicep()

    def publish(self, input_json_path: str):
        """Publish the definition."""
        # TODO: Implement
        pass

    def delete(self, input_json_path: str):
        """Delete the definition."""
        # TODO: Implement
        pass

    @abstractmethod
    def build_base_bicep(self):
        """Build the base bicep file."""
        raise NotImplementedError

    @abstractmethod
    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        raise NotImplementedError

    @abstractmethod
    def build_artifact_list(self):
        """Build the artifact list."""
        raise NotImplementedError

    @abstractmethod
    def build_resource_bicep(self):
        """Build the resource bicep file."""
        raise NotImplementedError
