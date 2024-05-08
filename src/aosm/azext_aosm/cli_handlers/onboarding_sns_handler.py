# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional
from typing import Dict

from knack.log import get_logger
from azext_aosm.cli_handlers.onboarding_nfd_base_handler import OnboardingBaseCLIHandler
from azext_aosm.common.constants import (
    SNS_OUTPUT_FOLDER_FILENAME,
    SNS_INPUT_FILENAME
)
from azext_aosm.configuration_models.common_parameters_config import (
    SNSCommonParametersConfig,
)
from azext_aosm.definition_folder.builder.bicep_builder import (
    BicepDefinitionElementBuilder,
)
from azext_aosm.definition_folder.builder.json_builder import (
    JSONDefinitionElementBuilder,
)
from azext_aosm.configuration_models.onboarding_sns_input_config import SiteNetworkServicePropertiesConfig

logger = get_logger(__name__)


class SNSCLIHandler(OnboardingBaseCLIHandler):
    """CLI handler for SNS."""

    config: SiteNetworkServicePropertiesConfig

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
        self.definition_folder_builder.add_element(self.build_all_parameters_json())
        self.definition_folder_builder.write()

    def _get_input_config(self, input_config: Optional[dict] = None) -> SiteNetworkServicePropertiesConfig:
        """Get the configuration for the command."""
        if input_config is None:
            input_config = {}
        return SiteNetworkServicePropertiesConfig(**input_config)

    def _get_params_config(self, config_file: Path) -> SNSCommonParametersConfig:
        """Get the configuration for the command."""
        with open(config_file, "r", encoding="utf-8") as _file:
            params_dict = json.load(_file)
        if params_dict is None:
            params_dict = {}
        return SNSCommonParametersConfig(**params_dict)

    def build_base_bicep(self) -> BicepDefinitionElementBuilder:
        pass

    def build_all_parameters_json(self) -> JSONDefinitionElementBuilder:
        """Build all parameters json."""
        params_content: Dict[str, str] = {}
        for property_name, value in vars(self.config).items():
            params_content[property_name] = value
        base_file = JSONDefinitionElementBuilder(
            Path(SNS_OUTPUT_FOLDER_FILENAME), json.dumps(params_content, indent=4)
        )

        return base_file

    def _get_processor_list(self):
        # Provide an implementation for this method
        pass

    def build_artifact_list(self):
        # Provide an implementation for this method
        pass

    def build_manifest_bicep(self):
        # Provide an implementation for this method
        pass

    def build_resource_bicep(self) -> BicepDefinitionElementBuilder:
        # Provide an implementation for this method
        pass
