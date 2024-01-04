# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from pathlib import Path
import json
from .onboarding_base_handler import OnboardingBaseCLIHandler
from azext_aosm.common.local_file_builder import LocalFileBuilder

class OnboardingNFDBaseCLIHandler(OnboardingBaseCLIHandler):
    """Abstract base class for NFD CLI handlers."""

    @property
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        raise NotImplementedError

    def build_base_bicep(self):
        # TODO: Implement
        raise NotImplementedError

    def _render_deployment_params_schema(self, complete_params_schema, output_folder_name, definition_folder_name):
        return LocalFileBuilder(
            Path(
                output_folder_name,
                definition_folder_name,
                "deploymentParameters.json",
            ),
            json.dumps(
                self._build_deploy_params_schema(complete_params_schema), indent=4
            ),
        )

    def _build_deploy_params_schema(self, schema_properties):
        """
        Build the schema for deployParameters.json
        """
        schema_contents = {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "title": "DeployParametersSchema",
            "type": "object",
            "properties": {},
        }
        schema_contents["properties"] = schema_properties
        return schema_contents
