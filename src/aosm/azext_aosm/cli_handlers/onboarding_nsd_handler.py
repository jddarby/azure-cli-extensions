# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
from .onboarding_nfd_base_handler import OnboardingBaseCLIHandler
from azext_aosm.vendored_sdks.models import ManifestArtifactFormat
from azext_aosm.configuration_models.onboarding_nsd_input_config import (
    NetworkFunctionPropertiesConfig,
    OnboardingNSDInputConfig,
)


class OnboardingNSDCLIHandler(OnboardingBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return "nsd-input.jsonc"

    def _get_config(self, input_config: dict = None) -> OnboardingNSDInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingNSDInputConfig(**input_config)

    def build_base_bicep(self):
        """Build the base bicep file."""
        # TODO: Implement
        raise NotImplementedError

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        # TODO: Implement
        artifact_list = []
        for resource_element in self.config.resource_element_templates:
            if resource_element.resource_element_type == "ArmTemplate":
                # TODO: Check manifests are only for ArmTemplates
                # Call helm processor and then get manifest details
                # # Add artifacts to a list of unique artifacts
                # if artifacts not in artifact_list:
                #   artifact_list.append(artifacts)
                
                # Mocking NSD artifact for testing 
                artifact_list.append(
                    ManifestArtifactFormat(
                        artifact_name=resource_element.properties.artifact_name,
                        artifact_type="ArmTemplate",
                        artifact_version=resource_element.properties.version,
                    )
                )

        template_path = self._get_template_path("nsdartifactmanifest.bicep.j2")
        bicep_contents = self._write_manifest_bicep_file(template_path, artifact_list)
        print(bicep_contents)
        return bicep_contents

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement
        raise NotImplementedError

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        raise NotImplementedError
