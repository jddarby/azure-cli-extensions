# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import genson
import json
from dataclasses import dataclass
from jinja2 import StrictUndefined, Template
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
        split_id = self.network_function_definition.id.split("/")
        publisher_name = split_id[8]
        nfdg_name = split_id[10]
        publisher_resource_group = split_id[4]

        base_defaults = {
            "configObject": {
                "publisherName": publisher_name,
                "nfdgName": nfdg_name,
                "nfdvName": self.network_function_definition.name,
                "publisherResourceGroup": publisher_resource_group
            }
        }

        if self.network_function_definition.properties.network_function_type == "VirtualNetworkFunction":
            base_defaults["configObject"]["customLocationId"] = ""

        return base_defaults

    def get_schema(self) -> Dict[str, Any]:
        """
        Abstract method to get the schema for configuring the artifact.
        Returns:
            A dictionary containing the schema.
        """
        base_schema = """
        {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "title": "nfDeploySchema",
            "type": "object",
            "properties": {
                "configObject": {
                    "type": "object",
                    "properties": {
                        "publisherName": {
                            "type": "string"
                        },
                        "nfdgName": {
                            "type": "string"
                        },
                        "nfdvName": {
                            "type": "string"
                        },
                        "publisherResourceGroup": {
                            "type": "string"
                        },
                        "location": {
                            "type": "string"
                        },
                        "deploymentParameters": {
                            "type": "array",
                            "items": {
                                "type": "object"
                            }
                        },
                        "customLocationId": {
                            "type": "string"
                        },
                        "managedIdentityId": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "publisherName",
                        "nfdgName",
                        "nfdvName",
                        "publisherResourceGroup",
                        "location",
                        "deploymentParameters",
                        "customLocationId",
                        "managedIdentityId"
                    ]
                }
            },
            "required": [
                "configObject"
            ]
        }
        """

        schema = json.loads(base_schema)
        nfdv_properties = self.network_function_definition.properties

        if nfdv_properties and nfdv_properties.deploy_parameters:

            schema["properties"]["configObject"]["properties"]["deploymentParameters"]["items"] = json.loads(nfdv_properties.deploy_parameters)
            builder = genson.SchemaBuilder()
            builder.add_schema(schema)
            return builder.to_schema()
        raise ValueError("No properties found in the network function definition.")
