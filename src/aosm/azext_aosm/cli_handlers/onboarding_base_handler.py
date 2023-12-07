# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
import json
from dataclasses import fields, is_dataclass
from azext_aosm.configuration_models.onboarding_base_input_config import OnboardingBaseInputConfig
from azure.cli.core.azclierror import UnclassifiedUserFault
from knack.log import get_logger
logger = get_logger(__name__)

class OnboardingBaseCLIHandler(ABC):
    """Abstract base class for CLI handlers."""

    config: OnboardingBaseInputConfig
    
    @property
    @abstractmethod
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        raise NotImplementedError

    def __init__(self, input_json: str | None = None):
        # Config may be optional (to generate blank config file)
        input_json_path = Path(input_json) if input_json else None
        config_dict = (
            self._read_config_from_file(input_json_path) if input_json_path else {}
        )
        # Ensure config is of correct type
        try:
            self.config = self._get_config(config_dict)
        except Exception as e:
            raise UnclassifiedUserFault("Invalid configuration file") from e
       
    def _read_config_from_file(self, input_json_path: Path) -> dict:
        """Reads the input JSONC file, removes comments + returns config as dictionary."""
        lines = input_json_path.read_text().splitlines()
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
        self, output_path: Path
    ):
        """Write the configuration to a file."""
        # Serialize the top-level dataclass instance and wrap it in curly braces to form a valid JSONC string.
        jsonc_str = "{\n" + self._serialize(self.config) + "\n}"
        output_path.write_text(jsonc_str)

        print(f"Empty configuration has been written to {output_path.name}")
        logger.info("Empty  configuration has been written to %s", output_path.name)

    def _check_for_overwrite(self, output_path: Path):
        """Check that the input file exists."""
        if output_path.exists():
            carry_on = input(
                f"The file {output_path.name} already exists in this location - do you want to overwrite it?"
                " (y/n)"
            )
            if carry_on != "y":
                raise UnclassifiedUserFault("User aborted!")

    def generate_config(self, output_file: str | None = None):
        """Generate the configuration file for the command."""
        if not output_file:
            output_file = self.default_config_file_name

        # Make Path object and ensure it has .jsonc extension
        output_path = Path(output_file).with_suffix(".jsonc")

        self._check_for_overwrite(output_path)
        self._write_config_to_file(output_path)

    def build(self):
        """Build the definition."""
        self.config.validate()
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