# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
from jinja2 import Template

import json
from pathlib import Path

from azure.cli.core.azclierror import ValidationError, UnclassifiedUserFault
from knack.log import get_logger

from azext_aosm.build_processors.helm_chart_processor import HelmChartProcessor
from azext_aosm.inputs.helm_chart_input import HelmChartInput
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.configuration_models.onboarding_cnf_input_config import (
    OnboardingCNFInputConfig,
)
from azext_aosm.configuration_models.common_parameters_config import (
    CNFCommonParametersConfig,
)
from azext_aosm.definition_folder.builder.artifact_builder import (
    ArtifactDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.json_builder import (
    JSONDefinitionElementBuilder,
)
from azext_aosm.common.constants import (
    ARTIFACT_LIST_FILENAME,
    BASE_FOLDER_NAME,
    CNF_BASE_TEMPLATE_FILENAME,
    CNF_TEMPLATE_FOLDER_NAME,
    CNF_DEFINITION_TEMPLATE_FILENAME,
    CNF_HELM_VALIDATION_ERRORS_TEMPLATE_FILENAME,
    CNF_HELM_VALIDATION_ERRORS_FILENAME,
    CNF_INPUT_FILENAME,
    CNF_MANIFEST_TEMPLATE_FILENAME,
    CNF_OUTPUT_FOLDER_FILENAME,
    HELM_TEMPLATE,
    MANIFEST_FOLDER_NAME,
    NF_DEFINITION_FOLDER_NAME,
    DEPLOYMENT_PARAMETERS_FILENAME,
)

from .onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler

logger = get_logger(__name__)


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

    def _get_input_config(self, input_config: dict = None) -> OnboardingCNFInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingCNFInputConfig(**input_config)

    def _get_params_config(
        self, params_config: dict = None
    ) -> CNFCommonParametersConfig:
        """Get the configuration for the command."""
        if params_config is None:
            params_config = {}
        return CNFCommonParametersConfig(**params_config)

    def _get_processor_list(self) -> [HelmChartProcessor]:
        processor_list = []
        # for each helm package, instantiate helm processor
        for helm_package in self.config.helm_packages:
            if helm_package.path_to_mappings:
                if Path(helm_package.path_to_mappings).exists():
                    provided_config = json.load(open(helm_package.path_to_mappings))
                else:
                    raise UnclassifiedUserFault(
                        "There is no file at the path provided for the mappings file."
                    )
            else:
                provided_config = None

            helm_input = HelmChartInput.from_chart_path(
                Path(helm_package.path_to_chart), default_config=provided_config
            )
            helm_processor = HelmChartProcessor(
                helm_package.name,
                helm_input,
                self.config.images.source_registry,
                self.config.images.source_registry_namespace,
            )
            processor_list.append(helm_processor)
        return processor_list

    def _validate_helm_template(self):
        """Validate the helm packages."""
        helm_chart_processors = self._get_processor_list()

        validation_errors = {}

        for helm_processor in helm_chart_processors:
            validation_output = helm_processor.input_artifact.validate_template()

            if validation_output:
                validation_errors[
                    helm_processor.input_artifact.artifact_name
                ] = validation_output

        if validation_errors:
            # Create an error file using a j2 template
            error_file_template_path = self._get_template_path(
                CNF_TEMPLATE_FOLDER_NAME, CNF_HELM_VALIDATION_ERRORS_TEMPLATE_FILENAME
            )

            with open(
                error_file_template_path,
                "r",
                encoding="utf-8",
            ) as file:
                error_file_template = Template(file.read())

            rendered_error_file_template = error_file_template.render(
                errors=validation_errors
            )

            logger.info(rendered_error_file_template)

            with open(
                CNF_HELM_VALIDATION_ERRORS_FILENAME,
                "w",
                encoding="utf-8",
            ) as error_file:
                error_file.write(rendered_error_file_template)

            raise ValidationError(
                f"Could not validate all the provided Helm charts. Please refer to the {CNF_HELM_VALIDATION_ERRORS_FILENAME} file for more information."
            )

    def pre_validate_build(self):
        """Run all validation functions required before building the cnf."""
        logger.debug("Pre-validating build")
        if self.skip != HELM_TEMPLATE:
            self._validate_helm_template()

    def build_base_bicep(self):
        """Build the base bicep file."""
        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(
            CNF_TEMPLATE_FOLDER_NAME, CNF_BASE_TEMPLATE_FILENAME
        )
        bicep_contents = self._render_base_bicep_contents(template_path)
        # Create Bicep element with base contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, BASE_FOLDER_NAME), bicep_contents
        )
        return bicep_file

    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        artifact_list = []
        logger.info("Creating artifact manifest bicep")
        for processor in self.processors:
            artifacts = processor.get_artifact_manifest_list()

            # Add artifacts to a list of unique artifacts
            if artifacts not in artifact_list:
                artifact_list.extend(artifacts)
        logger.debug(
            "Created list of artifacts from %s helm package(s) provided: %s",
            len(self.config.helm_packages),
            artifact_list,
        )
        # Build manifest bicep contents, with j2 template
        template_path = self._get_template_path(
            CNF_TEMPLATE_FOLDER_NAME, CNF_MANIFEST_TEMPLATE_FILENAME
        )
        bicep_contents = self._render_manifest_bicep_contents(
            template_path, artifact_list
        )
        # Create Bicep element with manifest contents
        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, MANIFEST_FOLDER_NAME), bicep_contents
        )

        return bicep_file

    def build_artifact_list(self):
        """Build the artifact list."""
        artifact_list = []
        # For each helm package, get list of artifacts and combine
        # For each arm template, get list of artifacts and combine
        for processor in self.processors:
            (artifacts, _) = processor.get_artifact_details()
            if artifacts not in artifact_list:
                artifact_list.extend(artifacts)
        logger.debug(
            "Created list of artifact details from %s helm packages(s) and the vhd image provided: %s",
            len(self.config.helm_packages),
            artifact_list,
        )
        # Generate Artifact Element with artifact list
        return ArtifactDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME), artifact_list
        )

    def build_resource_bicep(self):
        """Build the resource bicep file."""
        logger.info("Creating artifacts list for artifacts.json")
        nf_application_list = []
        mappings_files = []
        schema_properties = {}
        # For each helm package, generate nf application, generate mappings profile
        for processor in self.processors:
            # Generate nf application
            nf_application = processor.generate_nf_application()
            nf_application_list.append(nf_application)

            # Generate deploymentParameters schema properties
            params_schema = processor.generate_params_schema()
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
                json.dumps(json.loads(deploy_values), indent=4),
            )
            mappings_files.append(mapping_file)

        # Create bicep contents using cnf defintion j2 template
        template_path = self._get_template_path(
            CNF_TEMPLATE_FOLDER_NAME, CNF_DEFINITION_TEMPLATE_FILENAME
        )

        params = {
            "acr_nf_applications": nf_application_list,
            "deployment_parameters_file": DEPLOYMENT_PARAMETERS_FILENAME,
        }
        bicep_contents = self._render_definition_bicep_contents(template_path, params)

        # Create a bicep element + add its supporting mapping files
        bicep_file = BicepDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME), bicep_contents
        )
        for mappings_file in mappings_files:
            bicep_file.add_supporting_file(mappings_file)

        # Add the deploymentParameters schema file
        bicep_file.add_supporting_file(
            self._render_deployment_params_schema(
                schema_properties, CNF_OUTPUT_FOLDER_FILENAME, NF_DEFINITION_FOLDER_NAME
            )
        )
        return bicep_file

    def build_common_parameters_json(self):
        params_content = {
            "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "location": {"value": self.config.location},
                "publisherName": {"value": self.config.publisher_name},
                "publisherResourceGroupName": {
                    "value": self.config.publisher_resource_group_name
                },
                "acrArtifactStoreName": {"value": self.config.acr_artifact_store_name},
                "acrManifestName": {
                    "value": self.config.acr_artifact_store_name + "-manifest"
                },
                "nfDefinitionGroup": {"value": self.config.nf_name},
                "nfDefinitionVersion": {"value": self.config.version},
            },
        }

        base_file = JSONDefinitionElementBuilder(
            Path(CNF_OUTPUT_FOLDER_FILENAME), json.dumps(params_content, indent=4)
        )
        return base_file
