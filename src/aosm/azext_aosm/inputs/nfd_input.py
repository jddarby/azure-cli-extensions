# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from dataclasses import dataclass
from typing import Any, Dict
from azext_aosm.inputs.base_input import BaseInput
from azext_aosm.vendored_sdks.models import NetworkFunctionDefinitionVersion


@dataclass
class NFDInput(BaseInput):
    """
    A utility class for working with VHD files.
    """

    network_function_definition: NetworkFunctionDefinitionVersion

    def get_defaults(self) -> Dict[str, Any]:
        """
        Abstract method to get the default values for configuring the artifact.
        Returns:
            A dictionary containing the default values.
        """
        return self.default_config

    def get_schema(self) -> Dict[str, Any]:
        """
        Abstract method to get the schema for configuring the artifact.
        Returns:
            A dictionary containing the schema.
        """
        return json.loads(self.network_function_definition.properties.deploy_parameters)
