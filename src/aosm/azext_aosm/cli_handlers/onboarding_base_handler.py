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
        """Read the input JSONC file."""
        # TODO: Implement

    @abstractmethod
    def _get_config(self, input_config: dict = {}) -> OnboardingBaseInputConfig:
        """Get the configuration for the command."""
        raise NotImplementedError

    def serialize(self,instance, indent_count = 1):
        """
        Convert a dataclass instance to a JSONC string.
        This function takes 
        """
        indent = "\t" * indent_count
        double_indent = indent * 2
        # Initialize an empty list to hold the lines of the JSONC string.
        result = []
        # Iterate over the fields of the dataclass.
        for field_info in fields(instance):
            # Get the value of the current field.
            value = getattr(instance, field_info.name)
            
            # Get comment, if it exists + add it to the result
            comment = field_info.metadata.get('comment', '')
            if comment:
                for line in comment.split('\n'):
                    result.append(f'{indent}// {line}')

            if is_dataclass(value):
                # Serialize the nested dataclass and add it as a nested JSON object.
                if field_info == fields(instance)[-1]:
                    nested_json = "{\n" + self.serialize(value, indent_count+1) + "\n" + indent + "}"
                else:
                    nested_json = "{\n" + self.serialize(value, indent_count+1) + "\n" +  indent + "},"
                result.append(f'{indent}"{field_info.name}": {nested_json}')
            elif isinstance(value, list):
                # If the value is a list, iterate over the items.
                result.append(f'{indent}"{field_info.name}": [')
                for item in value:
                    # Check if the item is a dataclass and serialize it.
                    if is_dataclass(item):
                        inner_dataclass = self.serialize(item, indent_count+2)
                        if item == value[-1]:
                            result.append(double_indent + '{\n' + inner_dataclass + '\n' + double_indent +'}')
                        else:
                            result.append(double_indent +'{\n' + inner_dataclass + '\n' + double_indent +'},')
                    else:
                        result.append(json.dumps(item, indent=4) + ',')

                if field_info == fields(instance)[-1]:
                    result.append(indent +']')
                else:
                    result.append(indent +'],')
            else:
                # If the value is neither a dataclass nor a list, serialize it directly.
                if field_info == fields(instance)[-1]:
                    result.append(f'{indent}"{field_info.name}": {json.dumps(value,indent=4)}')
                else:
                    result.append(f'{indent}"{field_info.name}": {json.dumps(value,indent=4)},')
        return '\n'.join(result)

    def _write_config_to_file(
        self, config: OnboardingBaseInputConfig, output_file: str
    ):
        """Write the configuration to a file."""
        # TODO: Implement by converting config to JSONC
        # print(config.__dataclass_fields__['location'].metadata["comment"])
        # Serialize the top-level dataclass instance and wrap it in curly braces to form a valid JSONC string.
        jsonc_str = "{\n" + self.serialize(self.config) + "\n}"
        with open(output_file, "w") as f:
            f.write(jsonc_str)


    def generate_config(self, output_file: str):
        """Generate the configuration file for the command."""
        # TODO: Make file name depend on class via property
        self._write_config_to_file(self.config, output_file)

    def build(self, input_json_path: str):
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
