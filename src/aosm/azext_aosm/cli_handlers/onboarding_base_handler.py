# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
from abc import ABC, abstractmethod
from azext_aosm.configuration_models.onboarding_base_input_config import OnboardingBaseInputConfig
from dataclasses import asdict, dataclass,fields, is_dataclass
import json

class OnboardingBaseCLIHandler(ABC):
    """Abstract base class for CLI handlers."""

    config: OnboardingBaseInputConfig

    def __init__(self, input_json_path: str | None = None):
        # Config may be optional (to generate blank config file)

        config_dict = (
            self._read_config_from_file(input_json_path) if input_json_path else {}
        )
        self.config = self._get_config(config_dict)

    def _read_config_from_file(self, input_json_path: str) -> dict:
        """Reads the input JSONC file, removes comments + returns config as dictionary."""
        with open(input_json_path, "r") as f:
            lines = f.readlines()
        lines = [line for line in lines if not line.strip().startswith("//")]
        config_dict = json.loads("".join(lines))

        return config_dict

    @abstractmethod
    def _get_config(self, input_config: dict = {}) -> OnboardingBaseInputConfig:
        """Get the configuration for the command."""
        raise NotImplementedError

    def _serialize(self, dataclass, indent_count = 1):
        """
        Convert a dataclass instance to a JSONC string.
        This function recursively iterates over the fields of the dataclass and serializes them.
        
        We expect the dataclass to contain values of type string, list or another dataclass.
        Lists may only contain dataclasses. 
        For example,
        {
            "param1": "value1",
            "param2": [
                { ... },
                { ... }
            ],
            "param3": { ... }
        }
        """
        indent = "    " * indent_count
        double_indent = indent * 2
        jsonc_string = []

        for field_info in fields(dataclass):
            # Get the value of the current field.
            field_value = getattr(dataclass, field_info.name)

            # Get comment, if it exists + add it to the result
            comment = field_info.metadata.get('comment', '')
            if comment:
                for line in comment.split('\n'):
                    jsonc_string.append(f'{indent}// {line}')

            if is_dataclass(field_value):
                # Serialize the nested dataclass and add it as a nested JSON object.
                # Checks if it is last field to omit trailing comma
                if field_info == fields(dataclass)[-1]:
                    nested_json = "{\n" + self._serialize(field_value, indent_count+1) + "\n" + indent + "}"
                else:
                    nested_json = "{\n" + self._serialize(field_value, indent_count+1) + "\n" +  indent + "},"
                jsonc_string.append(f'{indent}"{field_info.name}": {nested_json}')
            elif isinstance(field_value, list):
                # If the value is a list, iterate over the items.
                jsonc_string.append(f'{indent}"{field_info.name}": [')
                for item in field_value:
                    # Check if the item is a dataclass and serialize it.
                    if is_dataclass(item):
                        inner_dataclass = self._serialize(item, indent_count+2)
                        if item == field_value[-1]:
                            jsonc_string.append(double_indent + '{\n' + inner_dataclass + '\n' + double_indent +'}')
                        else:
                            jsonc_string.append(double_indent +'{\n' + inner_dataclass + '\n' + double_indent +'},')
                    else:
                        jsonc_string.append(json.dumps(item, indent=4) + ',')
                # If the field is the last field, omit the trailing comma.
                if field_info == fields(dataclass)[-1]:
                    jsonc_string.append(indent +']')
                else:
                    jsonc_string.append(indent +'],')
            else:
                # If the value is a string, serialize it directly.
                if field_info == fields(dataclass)[-1]:
                    jsonc_string.append(f'{indent}"{field_info.name}": {json.dumps(field_value,indent=4)}')
                else:
                    jsonc_string.append(f'{indent}"{field_info.name}": {json.dumps(field_value,indent=4)},')
        return '\n'.join(jsonc_string)

    def _write_config_to_file(
        self, output_file: str
    ):
        """Write the configuration to a file."""
        # Serialize the top-level dataclass instance and wrap it in curly braces to form a valid JSONC string.
        jsonc_str = "{\n" + self._serialize(self.config) + "\n}"
        with open(output_file, "w") as f:
            f.write(jsonc_str)


    def generate_config(self, output_file: str):
        """Generate the configuration file for the command."""
        # TODO: Make file name depend on class via property
        self._write_config_to_file(output_file)

    def build(self):
        """Build the definition."""
        self.build_base_bicep()
        self.build_manifest_bicep()
        self.build_artifact_list()
        self.build_resource_bicep()

    def publish(self, input_json_path: str):
        """Publish the definition."""
        # Takes folder, deploys to Azure
        #  - Read folder/ create folder object
        #  - For each step (element):
        #    - Do element.deploy()
        # TODO: Implement

    def delete(self, input_json_path: str):
        """Delete the definition."""
        # Takes folder, deletes to Azure
        #  - Read folder/ create folder object
        #  - For each element (reversed):
        #    - Do element.delete()
        # TODO: Implement

    @abstractmethod
    def build_base_bicep(self):
        """Build the base bicep file."""
        raise NotImplementedError

    @abstractmethod
    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        raise NotImplementedError

    @abstractmethod
    def build_artifact_list(self):
        """Build the artifact list."""
        raise NotImplementedError

    @abstractmethod
    def build_resource_bicep(self):
        """Build the resource bicep file."""
        raise NotImplementedError
