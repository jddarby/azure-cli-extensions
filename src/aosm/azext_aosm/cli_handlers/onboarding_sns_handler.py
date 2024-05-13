# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from knack.log import get_logger

from azext_aosm.cli_handlers.onboarding_nfd_base_handler import OnboardingBaseCLIHandler
from azext_aosm.common.command_context import CommandContext
from azext_aosm.common.constants import (
    SNS_OUTPUT_FOLDER_FILENAME,
    SNS_INPUT_FILENAME,
    SNS_DEFINITION_FOLDER_NAME,
    SNS_TEMPLATE_FOLDER_NAME,
    SNS_DEFINITION_TEMPLATE_FILENAME,
)
from azext_aosm.common.utils import render_bicep_contents_from_j2, get_template_path
from azext_aosm.configuration_models.onboarding_sns_input_config import (
    OnboardingSNSInputConfig,
)
from azext_aosm.configuration_models.sns_parameters_config import SNSCommonParametersConfig
from azext_aosm.definition_folder.builder.bicep_builder import BicepDefinitionElementBuilder
from azext_aosm.definition_folder.builder.deploy_input_builder import DeploymentInputDefinitionElementBuilder
from azext_aosm.definition_folder.builder.json_builder import (
    JSONDefinitionElementBuilder,
)
from azext_aosm.definition_folder.reader.definition_folder import DefinitionFolder
from azext_aosm.vendored_sdks import HybridNetworkManagementClient
from azext_aosm.vendored_sdks.models import (
    NetworkServiceDesignVersion,
)


class OnboardingSNSCLIHandler(OnboardingBaseCLIHandler):
    """CLI handler for deploying SNSs."""

    config: OnboardingSNSInputConfig | SNSCommonParametersConfig
    logger = get_logger(__name__)

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        return SNS_INPUT_FILENAME

    @property
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        return SNS_OUTPUT_FOLDER_FILENAME

    def build(self):
        """Build the definition."""
        self.definition_folder_builder.add_element(self.build_resource_bicep())
        self.definition_folder_builder.add_element(self.build_deploy_input())
        self.definition_folder_builder.add_element(self.build_all_parameters_json())
        self.definition_folder_builder.write()

    def _get_processor_list(self) -> list:
        return []

    def _get_input_config(self, input_config: Optional[dict] = None) -> OnboardingSNSInputConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return OnboardingSNSInputConfig(**input_config)

    def _get_params_config(self, config_file: Path) -> SNSCommonParametersConfig:
        """Get the configuration for the command."""
        with open(config_file, "r", encoding="utf-8") as _file:
            params_dict = json.load(_file)
        if params_dict is None:
            params_dict = {}
        return SNSCommonParametersConfig(**params_dict)

    def build_deploy_input(self) -> DeploymentInputDefinitionElementBuilder:
        """Pre-validate the build."""
        nsdv = self._get_nsdv()
        deployment_input_file = DeploymentInputDefinitionElementBuilder(
            Path(SNS_OUTPUT_FOLDER_FILENAME), nsdv.properties.nfvis_from_site
        )
        return deployment_input_file

    def _get_nsdv(self) -> NetworkServiceDesignVersion:
        """Get the existing NSDV resource object."""
        print(
            f"Reading existing NSDV resource object "
            f"{self.config.nsd_reference.nsd_version} from group "
            f"{self.config.nsd_reference.nsd_name}"
        )
        assert isinstance(self.aosm_client, HybridNetworkManagementClient)
        nsdv_object = self.aosm_client.network_service_design_versions.get(
            resource_group_name=self.config.nsd_reference.publisher_resource_group_name,
            publisher_name=self.config.nsd_reference.publisher_name,
            network_service_design_group_name=self.config.nsd_reference.nsd_name,
            network_service_design_version_name=self.config.nsd_reference.nsd_version,
        )
        return nsdv_object

    def build_resource_bicep(self) -> BicepDefinitionElementBuilder:
        """Build the resource bicep file."""
        template_path = get_template_path(
            SNS_TEMPLATE_FOLDER_NAME, SNS_DEFINITION_TEMPLATE_FILENAME
        )
        params = {}

        bicep_contents = render_bicep_contents_from_j2(
            template_path, params
        )
        # Generate the nsd bicep file
        bicep_file = BicepDefinitionElementBuilder(
            Path(SNS_OUTPUT_FOLDER_FILENAME, SNS_DEFINITION_FOLDER_NAME), bicep_contents
        )

        return bicep_file

    def deploy(self, command_context: CommandContext):
        """Publish the definition contained in the specified definition folder."""
        definition_folder = DefinitionFolder(
            command_context.cli_options["definition_folder"]
        )
        assert isinstance(self.config, SNSCommonParametersConfig)
        definition_folder.deploy(config=self.config, command_context=command_context)

    def build_all_parameters_json(self) -> JSONDefinitionElementBuilder:
        """Build all parameters json."""
        params_content = {
            "location": self.config.location,
            "operatorResourceGroupName": self.config.operator_resource_group_name,
            "siteName": self.config.site_name
        }
        base_file = JSONDefinitionElementBuilder(
            Path(SNS_OUTPUT_FOLDER_FILENAME), json.dumps(params_content, indent=4)
        )
        return base_file

    def build_base_bicep(self):
        # TODO: Implement
        raise NotImplementedError

    def build_artifact_list(self):
        # TODO: Implement this method
        raise NotImplementedError

    def build_manifest_bicep(self) -> BicepDefinitionElementBuilder:
        # TODO: Implement this method
        raise NotImplementedError
