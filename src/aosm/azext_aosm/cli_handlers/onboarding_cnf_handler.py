# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
import json
from pathlib import Path
from azext_aosm.configuration_models.onboarding_cnf_input_config import (
    OnboardingCNFInputConfig,
)
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.common.artifact import (
    BaseArtifact,
    LocalFileACRArtifact,
    BaseACRArtifact,
)
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from azext_aosm.build_processors.helm_chart_processor import HelmChartProcessor
from azext_aosm.common.constants import (
    CNF_DEFINITION_TEMPLATE_FILENAME,
    CNF_MANIFEST_TEMPLATE_FILENAME,
    CNF_OUTPUT_FOLDER_FILENAME,
    ARTIFACT_LIST_FILENAME,
    MANIFEST_FOLDER_NAME,
    NF_DEFINITION_FOLDER_NAME,
)
from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from azext_aosm.vendored_sdks.models import (
    ManifestArtifactFormat,
    AzureArcKubernetesHelmApplication,
    AzureArcKubernetesArtifactProfile,
    HelmArtifactProfile,
    AzureArcKubernetesDeployMappingRuleProfile,
    HelmMappingRuleProfile,
    HelmMappingRuleProfileOptions,
)


class OnboardingCNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return "cnf-input.jsonc"

    @property
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        return CNF_OUTPUT_FOLDER_FILENAME

    def _get_config(self, input_config: dict = {}) -> OnboardingCNFInputConfig:
        """Get the configuration for the command."""
        return OnboardingCNFInputConfig(**input_config)

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        # TODO: Implement
        artifact_list = []
        # Jordan: Logic when HelmChartProcessor is implemented
        # for helm_package in self.config.helm_packages:
        #     processed_helm = HelmChartProcessor(
        #         helm_package.name,
        #         self.config.acr_artifact_store_name,
        #         helm_package,
        #     )
        #     artifacts = processed_helm.get_artifact_manifest_list()
        ## TODO: make artifact_list a set, then convert back to list
        ## TODO: add to util, compare properly the artifacts
        # # Add artifacts to a list of unique artifacts
        #     if artifacts not in artifact_list:
        #         artifact_list.append(artifacts)

        # Jordan: For testing write manifest bicep. THIS IS THE RIGHT TEST
        test_base_artifact = ManifestArtifactFormat(
            artifact_name="test",
            artifact_type="OCIArtifact",
            artifact_version="4.1.0-12-rel-4-1-0",
        )
        artifact_list.append(test_base_artifact)

        template_path = self._get_template_path("cnf", CNF_MANIFEST_TEMPLATE_FILENAME)
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, artifact_list
        )
        # print(bicep_contents)

        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME), bicep_contents
        )
        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_manifest_parameters_contents())
        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        artifact_list = []
        # TODO: Test with processor

        # for helm_package in self.config.helm_packages:
        #     processed_helm = HelmChartProcessor(
        #         helm_package.name,
        #         self.config.acr_artifact_store_name,
        #         helm_package,
        #     )
        #     (artifacts, files) = processed_helm.get_artifact_details()
        #     if artifacts not in artifact_list:
        #         artifact_list.append(artifacts)

        # # For testing artifact builder works
        test_base_artifact = LocalFileACRArtifact(
            artifact_manifest=ManifestArtifactFormat(
                artifact_name="test",
                artifact_type="OCIArtifact",
                artifact_version="4.1.0-12-rel-4-1-0",
            ),
            file_path=Path("test"),
        )
        artifact_list.append(test_base_artifact)
        # print(artifact_list)
        return ArtifactDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        # TODO: Implement
        nf_application_list = []
        supporting_files = []
        complete_params_schema = {}
        # For each helm package, generate nf application, generate mappings profile
        # for helm_package in self.config.helm_packages:
        #     processed_helm = HelmChartProcessor(
        #         helm_package.name,
        #         self.config.acr_artifact_store_name,
        #         helm_package,
        #     )
        #     nf_application = processed_helm.generate_nf_application()
        #     nf_application_list.append(nf_application)

        #     # # params_schema = processed_helm.generate_params_schema()
        #     # complete_params_schema.update(params_schema)
        #     # example params_schema "nf_app_name": <SCHEMA>

        #     # Adding supporting file: config mappings
        # deploy_values = (
        #     nf_application.deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile.values
        # )
        # mapping_file = LocalFileBuilder(
        #     Path(
        #         CNF_OUTPUT_FOLDER_FILENAME,
        #         NF_DEFINITION_FOLDER_NAME,
        #         nf_application.name + "-mappings.json",
        #     ),
        #     deploy_values,
        # )
        # supporting_files.append(mapping_file)

        # Jordan: mocked nf applicaton
        test_nf_application = AzureArcKubernetesHelmApplication(
            name="testNFApplication",
            depends_on_profile=[],
            artifact_profile=AzureArcKubernetesArtifactProfile(
                artifact_store="testArtifactStore",
                helm_artifact_profile=HelmArtifactProfile(
                    helm_package_name="testHelmPackage",
                    helm_package_version_range="1.0.0",
                    registry_values_paths=["testPath1", "testPath2"],
                    image_pull_secrets_values_paths=["testPath3", "testPath4"],
                ),
            ),
            deploy_parameters_mapping_rule_profile=AzureArcKubernetesDeployMappingRuleProfile(
                application_enablement="testApplicationEnablement",
                helm_mapping_rule_profile=HelmMappingRuleProfile(
                    release_namespace="testReleaseNamespace",
                    release_name="testReleaseName",
                    helm_package_version="1.0.0",
                    values="testValues",
                    options=None,
                ),
            ),
        )
        deploy_values = (
            test_nf_application.deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile.values
        )
        supporting_files.append(
            LocalFileBuilder(
                Path(
                    CNF_OUTPUT_FOLDER_FILENAME,
                    NF_DEFINITION_FOLDER_NAME,
                    test_nf_application.name + "-mappings.json",
                ),
                deploy_values,
            )
        )
        nf_application_list.append(test_nf_application)
        complete_params_schema.update(
            {
                test_nf_application.name: {
                    "type": "object",
                    "properties": {"test1": {"type": "string"}, "test2" : {"type": "string"}},
                }
            }
        )
        # End testing

        template_path = self._get_template_path("cnf", CNF_DEFINITION_TEMPLATE_FILENAME)
        bicep_contents = self._write_definition_bicep_file(
            template_path, nf_application_list
        )

        # Create a bicep element + add its supporting files (mappings + schema)
        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME), bicep_contents
        )
        for mappings_file in supporting_files:
            bicep_file.add_supporting_file(mappings_file)

        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_definition_parameters_contents())

        # Add the deployParameters schema
        bicep_file.add_supporting_file(self._render_deploy_params_schema(complete_params_schema))
        return bicep_file

    def _render_deploy_params_schema(self, complete_params_schema):
        return LocalFileBuilder(
            Path(
                CNF_OUTPUT_FOLDER_FILENAME,
                NF_DEFINITION_FOLDER_NAME,
                "deploymentParameters.json",
            ),
            json.dumps(self._build_deploy_params_schema(complete_params_schema), indent=4),
        )
    def _render_manifest_parameters_contents(self):
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "acrManifestName": {
                    "value": self.config.acr_artifact_store_name + "-manifest"
                },
            },
        }

        return LocalFileBuilder(
            Path(
                CNF_OUTPUT_FOLDER_FILENAME,
                MANIFEST_FOLDER_NAME,
                "deploy.parameters.json",
            ),
            json.dumps(params_content, indent=4),
        )

    def _render_definition_parameters_contents(self):
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "nfDefinitionGroup": {"value": self.config.nf_name},
                "nfDefinitionVersion": {"value": self.config.version},
            },
        }

        return LocalFileBuilder(
            Path(
                CNF_OUTPUT_FOLDER_FILENAME,
                NF_DEFINITION_FOLDER_NAME,
                "deploy.parameters.json",
            ),
            json.dumps(params_content, indent=4),
        )
