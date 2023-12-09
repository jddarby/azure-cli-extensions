# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
from pathlib import Path
from azext_aosm.configuration_models.onboarding_cnf_input_config import (
    OnboardingCNFInputConfig,
)
from azext_aosm.build_processors.helm_chart_processor import HelmChartProcessor
from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from azext_aosm.vendored_sdks.models import (
    ManifestArtifactFormat, AzureArcKubernetesHelmApplication, 
    AzureArcKubernetesArtifactProfile, HelmArtifactProfile,
    AzureArcKubernetesDeployMappingRuleProfile, HelmMappingRuleProfile, HelmMappingRuleProfileOptions)
# from azext_aosm.vendored_sdks.models import ArtifactStore

class OnboardingCNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return "cnf-input.jsonc"

    def _get_config(self, input_config: dict = None) -> OnboardingCNFInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingCNFInputConfig(**input_config)

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        # TODO: Implement
        # print("config", self.config)
        artifact_list = []
        # Jordan: Logic when HelmChartProcessor is implemented
        # for helm_package in self.config.helm_packages:
        #     processed_helm = HelmChartProcessor(
        #         helm_package.name,
        #         self.config.acr_artifact_store_name,
        #         helm_package,
        #     )
        #     artifacts = processed_helm.get_artifact_manifest_list()

        # # Add artifacts to a list of unique artifacts
        #     if artifacts not in artifact_list:
        #         artifact_list.append(artifacts)

        # Jordan: For testing write manifest bicep
        artifact_list.append(ManifestArtifactFormat(artifact_name="test", artifact_type="OCIArtifact", artifact_version="4.1.0-12-rel-4-1-0"))

        template_path = self._get_template_path("cnfartifactmanifest.bicep.j2")
        bicep_contents = self._write_manifest_bicep_file(template_path, artifact_list)
        print("JORDAN MANIFEST", bicep_contents)

        return bicep_contents

    def build_artifact_list(self):
        """Build the artifact list."""
        # TODO: Implement
        raise NotImplementedError

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        nf_application_list = []
        # for helm_package in self.config.helm_packages:
        #     processed_helm = HelmChartProcessor(
        #         helm_package.name,
        #         self.config.acr_artifact_store_name,
        #         helm_package,
        #     )
        #     nf_application_list.append(processed_helm.generate_nf_application())
        
        # Jordan: mocked nf applicaton
        test_nf_application = AzureArcKubernetesHelmApplication(
            name="testNFApplication",
            depends_on_profile=[],
            artifact_profile=AzureArcKubernetesArtifactProfile(artifact_store="testArtifactStore", 
                                                               helm_artifact_profile=HelmArtifactProfile(
                                                                   helm_package_name="testHelmPackage",
                                                                   helm_package_version_range="1.0.0",
                                                                   registry_values_paths=["testPath1", "testPath2"],
                                                                   image_pull_secrets_values_paths=["testPath3", "testPath4"])),
            deploy_parameters_mapping_rule_profile=AzureArcKubernetesDeployMappingRuleProfile(application_enablement="testApplicationEnablement",
                                                                                              helm_mapping_rule_profile=HelmMappingRuleProfile(
                                                                                                  release_namespace="testReleaseNamespace",
                                                                                                  release_name="testReleaseName",
                                                                                                  helm_package_version="1.0.0",
                                                                                                  values="testValues",
                                                                                                  options=None
                                                                                              )))
        nf_application_list.append(test_nf_application)
        template_path = self._get_template_path("cnfdefinition.bicep.j2")
        
        #   values: string(loadJsonContent('configMappings/{{ configuration.valueMappingsFile }}'))
           
        bicep_contents = self._write_definition_bicep_file(template_path, nf_application_list)
        print("JORDAN NF", bicep_contents)

        return bicep_contents
