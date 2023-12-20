# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from azext_aosm.inputs.base_input import BaseInput
from azext_aosm.vendored_sdks.models import NetworkFunctionDefinitionVersion


@dataclass
class NFDInput(BaseInput):
    """
    A utility class for working with VHD files.
    """

    network_function_definition: NetworkFunctionDefinitionVersion
    arm_template_output_path: Path

    def get_defaults(self) -> Dict[str, Any]:
        """
        Abstract method to get the default values for configuring the artifact.
        Returns:
            A dictionary containing the default values.
        """
        if self.default_config:
            return self.default_config
        return {}

    def get_schema(self) -> Dict[str, Any]:
        """
        Abstract method to get the schema for configuring the artifact.
        Returns:
            A dictionary containing the schema.
        """

        nfdv_properties = self.network_function_definition.properties
        if nfdv_properties and nfdv_properties.deploy_parameters:
            return json.loads(nfdv_properties.deploy_parameters)
        raise ValueError("No properties found in the network function definition.")
