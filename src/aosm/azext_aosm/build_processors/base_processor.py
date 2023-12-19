# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple
from azext_aosm.inputs.base_input import BaseInput
from azext_aosm.common.artifact import BaseArtifact
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.vendored_sdks.models import (
    ManifestArtifactFormat,
    NetworkFunctionApplication,
    ResourceElementTemplate,
)

from typing import Dict, Any


@dataclass
class BaseBuildProcessor(ABC):
    """Base class for build processors."""

    name: str
    input_artifact: BaseInput

    @abstractmethod
    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Returns list of artifacts in ManifestArtifactFormat"""
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

    def generate_params_schema(
        self, schema: Dict[str, Any], values: Dict[str, Any], is_nsd: bool = False
    ) -> Dict[str, Any]:
        """Generate the parameter schema"""

        # Loop through each property in the schema.
        for k, v in schema["properties"].items():
            # If the property is not in the values, and is required, add it to the values.
            if "required" in schema and k not in values and k in schema["required"]:
                print(f"Adding {k} to values")
                if v["type"] == "object":
                    values[k] = self.generate_params_schema()
                else:
                    values[k] = (
                        f"{{configurationparameters('{self.name}').{k}}}"
                        if is_nsd
                        else f"{{deployParameters.{self.name}.{k}}}"
                    )
            # If the property is in the values, and is an object, generate the values mappings
            # for the subschema.
            if k in values and v["type"] == "object" and values[k]:
                values[k] = self.generate_params_schema(self.name, v, {}, is_nsd)
        return values

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

        # Loop through each property in the schema.
        for k, v in schema["properties"].items():
            # If the property is not in the values, and is required, add it to the values.
            if "required" in schema and k not in values and k in schema["required"]:
                print(f"Adding {k} to values")
                if v["type"] == "object":
                    values[k] = self.generate_values_mappings(self.name, v, {}, is_nsd)
                else:
                    values[k] = (
                        f"{{configurationparameters('{self.name}').{k}}}"
                        if is_nsd
                        else f"{{deployParameters.{self.name}.{k}}}"
                    )
            # If the property is in the values, and is an object, generate the values mappings
            # for the subschema.
            if k in values and v["type"] == "object" and values[k]:
                values[k] = self.generate_values_mappings(self.name, v, {}, is_nsd)
        return values
