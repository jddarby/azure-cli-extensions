# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations

import json
from pathlib import Path
from azure.cli.core.azclierror import UnclassifiedUserFault
from azext_aosm.build_processors.helm_chart_processor import HelmChartProcessor
from azext_aosm.inputs.helm_chart_input import HelmChartInput
from azext_aosm.common.constants import (ARTIFACT_LIST_FILENAME,
                                         CNF_DEFINITION_TEMPLATE_FILENAME,
                                         CNF_MANIFEST_TEMPLATE_FILENAME,
                                         CNF_BASE_TEMPLATE_FILENAME,
                                         CNF_DEFINITION_FOLDER_NAME,
                                         CNF_OUTPUT_FOLDER_FILENAME,
                                         CNF_INPUT_FILENAME,
                                         MANIFEST_FOLDER_NAME,
                                         NF_DEFINITION_FOLDER_NAME,
                                         BASE_FOLDER_NAME)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.configuration_models.onboarding_cnf_input_config import \
    OnboardingCNFInputConfig
from azext_aosm.definition_folder.builder.artifact_builder import \
    ArtifactDefinitionElementBuilder
from azext_aosm.definition_folder.builder.bicep_builder import \
    BicepDefinitionElementBuilder
from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler


class OnboardingCNFCLIHandler(OnboardingNFDBaseCLIHandler):
    """CLI handler for publishing NFDs."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return CNF_INPUT_FILENAME

    @property
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        return CNF_OUTPUT_FOLDER_FILENAME

    def _get_config(self, input_config: dict = None) -> OnboardingCNFInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingCNFInputConfig(**input_config)

    def build_base_bicep(self):
        """ Build the base bicep file."""

        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(CNF_DEFINITION_FOLDER_NAME, CNF_BASE_TEMPLATE_FILENAME)
        bicep_contents = self._render_base_bicep_contents(
            template_path
        )
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, BASE_FOLDER_NAME), bicep_contents
        )
        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_base_parameters_contents())
        return bicep_file

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        artifact_list = []

        # For each helm package, get list of artifacts
        for helm_package in self.config.helm_packages:
            # TODO: check if we can just default to None in build manifest (does it matter?)
            # Check if any default config has been provided in the input file
            if helm_package.path_to_mappings:
                if Path.exists(Path(helm_package.path_to_mappings)):
                    provided_config = json.load(open(helm_package.path_to_mappings))
                else:
                    raise UnclassifiedUserFault("There is no file at the path provided for the mappings file.")
            else:
                provided_config = None

            helm_input = HelmChartInput.from_chart_path(Path(helm_package.path_to_chart), default_config=provided_config)
            processed_helm = HelmChartProcessor(
                helm_package.name,
                helm_input,
                self.config.acr_artifact_store_name
            )
            artifacts = processed_helm.get_artifact_manifest_list()
        # TODO: future work: make artifact_list a set, then convert back to list
        # TODO: future work: add to util, compare properly the artifacts
        # Add artifacts to a list of unique artifacts
            if artifacts not in artifact_list:
                artifact_list.extend(artifacts)

        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(CNF_DEFINITION_FOLDER_NAME, CNF_MANIFEST_TEMPLATE_FILENAME)
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, artifact_list
        )
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME), bicep_contents
        )
        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_manifest_parameters_contents())

        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        artifact_list = []
        # For each helm package, get list of artifacts and combine
        for helm_package in self.config.helm_packages:
            helm_input = HelmChartInput.from_chart_path(Path(helm_package.path_to_chart), default_config=None)
            # TODO: add comment why this is needed
            if self.config.images.source_registry_namespace:
                remote_image_source = f"{self.config.acr_artifact_store_name}/{self.config.images.source_registry_namespace}"
            else:
                remote_image_source = self.config.acr_artifact_store_name
            processed_helm = HelmChartProcessor(
                helm_package.name,
                helm_input,
                remote_image_source
            )
            (artifacts, files) = processed_helm.get_artifact_details()
            if artifacts not in artifact_list:
                artifact_list.extend(artifacts)

        # Generate Artifact Element with artifact list
        return ArtifactDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        nf_application_list = []
        mappings_files = []
        schema_properties = {}
        # For each helm package, generate nf application, generate mappings profile
        for helm_package in self.config.helm_packages:
            # Check if any default config has been provided in the input file
            if helm_package.path_to_mappings:
                if Path.exists(Path(helm_package.path_to_mappings)):
                    provided_config = json.load(open(helm_package.path_to_mappings))
                else:
                    raise UnclassifiedUserFault("There is no file at the path provided for the mappings file.")
            else:
                provided_config = None

            # Create HelmChartInput object from chart path provided in input file
            helm_input = HelmChartInput.from_chart_path(Path(helm_package.path_to_chart), default_config=provided_config)
            if self.config.images.source_registry_namespace:
                remote_image_source = f"{self.config.acr_artifact_store_name}/{self.config.images.source_registry_namespace}"
            else:
                remote_image_source = self.config.acr_artifact_store_name

            # Create HelmChartProcessor object from HelmChartInput object
            processed_helm = HelmChartProcessor(
                helm_package.name,
                helm_input,
                remote_image_source
            )

            # Generate nf application
            nf_application = processed_helm.generate_nf_application()
            nf_application_list.append(nf_application)

            # Generate deploymentParameters schema properties
            params_schema = processed_helm.generate_params_schema()
            schema_properties.update(params_schema)

            # Adding supporting file: config mappings
            deploy_values = (
                nf_application.deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile.values
            )
            mapping_file = LocalFileBuilder(
                Path(
                    CNF_OUTPUT_FOLDER_FILENAME,
                    NF_DEFINITION_FOLDER_NAME,
                    nf_application.name + "-mappings.json",
                ),
                deploy_values,
            )
            mappings_files.append(mapping_file)

        template_path = self._get_template_path(CNF_DEFINITION_FOLDER_NAME, CNF_DEFINITION_TEMPLATE_FILENAME)
        bicep_contents = self._render_definition_bicep_contents(
            template_path, nf_application_list
        )

        # Create a bicep element + add its supporting mapping files
        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME), bicep_contents
        )
        for mappings_file in mappings_files:
            bicep_file.add_supporting_file(mappings_file)

        # Add the accompanying parameters.json
        bicep_file.add_supporting_file(self._render_definition_parameters_contents())

        # Add the deploymentParameters schema file
        bicep_file.add_supporting_file(
            self._render_deployment_params_schema(schema_properties, CNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME)
        )
        return bicep_file

    def _render_base_parameters_contents(self):
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "nfDefinitionGroup": {"value": self.config.nf_name}
            },
        }

        return LocalFileBuilder(
            Path(
                CNF_OUTPUT_FOLDER_FILENAME,
                BASE_FOLDER_NAME,
                "deploy.parameters.json",
            ),
            json.dumps(params_content, indent=4),
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
