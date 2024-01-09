# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from azext_aosm.common.artifact import BaseArtifact
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.inputs.base_input import BaseInput
from azext_aosm.vendored_sdks.models import (ManifestArtifactFormat,
                                             NetworkFunctionApplication,
                                             ResourceElementTemplate)


@dataclass
class BaseBuildProcessor(ABC):
    """Base class for build processors."""

    name: str
    input_artifact: BaseInput

    @abstractmethod
    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        raise NotImplementedError

    @abstractmethod
    def get_artifact_details(self) -> Tuple[List[BaseArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        raise NotImplementedError

    @abstractmethod
    def generate_nf_application(self) -> NetworkFunctionApplication:
        """Generate the NF application."""
        raise NotImplementedError

    @abstractmethod
    def generate_resource_element_template(self) -> ResourceElementTemplate:
        """Generate the resource element template."""
        raise NotImplementedError

    def generate_params_schema(self) -> Dict[str, Any]:
        """Generate the parameter schema"""
        base_params_schema = """
        {
            "%s": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
        """ % (
            self.name
        )

        params_schema = json.loads(base_params_schema)
        # print(json.dumps(self.input_artifact.get_schema(), indent=4))
        # print(json.dumps(self.input_artifact.get_defaults(), indent=4))
        self._generate_schema(
            params_schema[self.name],
            self.input_artifact.get_schema(),
            self.input_artifact.get_defaults(),
        )

        # If there are no properties, return an empty dict as we don't need
        # a schema for this input artifact.
        if not bool(params_schema[self.name]["properties"]):
            return {}

        return params_schema

    def _generate_schema(
        self,
        schema: Dict[str, Any],
        source_schema: Dict[str, Any],
        values: Dict[str, Any],
    ) -> None:
        """Generate the parameter schema"""
        if "properties" not in source_schema.keys():
            return

        # Loop through each property in the schema.
        for k, v in source_schema["properties"].items():
            # If the property is not in the values, and is required, add it to the values.
            if (
                "required" in source_schema
                and k not in values
                and k in source_schema["required"]
            ):
                if v["type"] == "object":
                    print(f"Resolving object {k} for schema")
                    self._generate_schema(schema, v, {})
                else:
                    schema["required"].append(k)
                    schema["properties"][k] = v
            # If the property is in the values, and is an object, generate the values mappings
            # for the subschema.
            if k in values and v["type"] == "object" and values[k]:
                self._generate_schema(schema, v, values[k])

    def generate_values_mappings(
        self,
        schema: Dict[str, Any],
        values: Dict[str, Any],
        is_nsd: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate values mappings for a Helm chart.
        Args:
            schema (Dict[str, Any]): The schema of the Helm chart.
            values (Dict[str, Any]): The values of the Helm chart.
        Returns:
            Dict[str, Any]: The value mappings for the Helm chart.
        """
        # If there are no properties in the schema for the object, return the values.
        if "properties" not in schema.keys():
            return values

        # Loop through each property in the schema.
        for k, v in schema["properties"].items():
            # If the property is not in the values, and is required, add it to the values.
            if "required" in schema and k not in values and k in schema["required"]:
                print(f"Adding {k} to values")
                if v["type"] == "object":
                    values[k] = self.generate_values_mappings(v, {}, is_nsd)
                else:
                    values[k] = (
                        f"{{configurationparameters('{self.name}').{k}}}"
                        if is_nsd
                        else f"{{deployParameters.{self.name}.{k}}}"
                    )
            # If the property is in the values, and is an object, generate the values mappings
            # for the subschema.
            if k in values and v["type"] == "object" and values[k]:
                values[k] = self.generate_values_mappings(v, values[k], is_nsd)

        return values
