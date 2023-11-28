# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod


class OnboardingBaseCLIHandler(ABC):
    """Abstract base class for CLI handlers."""

    def __init__(self, config):
        # Config may be optional (to generate blank config file)
        # TODO: Implement
        pass

    def generate_config(self):
        """Generate the configuration file for the command."""
        # TODO: Implement
        pass

    def build(self):
        """Build the definition."""
        self.build_base_bicep()
        self.build_manifest_bicep()
        self.build_artifact_list()
        self.build_resource_bicep()

    def publish(self):
        """Publish the definition."""
        # TODO: Implement
        pass

    def delete(self):
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
