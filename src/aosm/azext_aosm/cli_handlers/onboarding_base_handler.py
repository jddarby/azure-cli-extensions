# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import fields, is_dataclass
from pathlib import Path
from azure.cli.core.azclierror import UnclassifiedUserFault
from jinja2 import StrictUndefined, Template
from knack.log import get_logger

from azext_aosm.configuration_models.onboarding_base_input_config import (
    OnboardingBaseInputConfig,
)
from azext_aosm.definition_folder.builder.definition_folder_builder import (
    DefinitionFolderBuilder,
)
from azext_aosm.definition_folder.reader.definition_folder import DefinitionFolder
from azext_aosm.common.command_context import CommandContext
from azext_aosm.configuration_models.common_parameters_config import \
    BaseCommonParametersConfig
from azext_aosm.vendored_sdks.models import AzureCoreNetworkFunctionVhdApplication

logger = get_logger(__name__)


class OnboardingBaseCLIHandler(ABC):
    """Abstract base class for CLI handlers."""

    @property
    @abstractmethod
    def default_config_file_name(self) -> str:
        """Get the default configuration file name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def output_folder_file_name(self) -> str:
        """Get the output folder file name."""
        raise NotImplementedError

    def __init__(self, config_file: str | None = None):
        # If config file provided (for build, publish and delete)
        if config_file:
            config_file_path = Path(config_file)
            try:
                # If config file is the input.jsonc for build command
                if config_file_path.suffix == '.jsonc':
                    config_dict = (
                        self._read_input_config_from_file(config_file_path)
                    )
                    self.config = self._get_input_config(config_dict)
                # If config file is the all parameters json file for publish/delete
                elif config_file_path.suffix == '.json':
                    config_dict = self._read_params_config_from_file(config_file_path)
                    self.config = self._get_params_config(config_dict)
            except Exception as e:
                raise UnclassifiedUserFault("Invalid input") from e
        # If no config file provided (for generate-config)
        else:
            self.config = self._get_input_config()
        self.definition_folder_builder = DefinitionFolderBuilder(
            Path.cwd() / self.output_folder_file_name
        )

    def generate_config(self, output_file: str | None = None):
        """Generate the configuration file for the command."""
        if not output_file:
            output_file = self.default_config_file_name

        # Make Path object and ensure it has .jsonc extension
        output_path = Path(output_file).with_suffix(".jsonc")

        self._check_for_overwrite(output_path)
        self._write_config_to_file(output_path)

    def build(self, aosm_client=None):
        """Build the definition."""
        self.config.validate()
        self.definition_folder_builder.add_element(self.build_base_bicep())
        self.definition_folder_builder.add_element(self.build_manifest_bicep())
        self.definition_folder_builder.add_element(self.build_artifact_list())
        self.definition_folder_builder.add_element(self.build_resource_bicep(aosm_client))
        self.definition_folder_builder.add_element(self.build_common_parameters_json())
        self.definition_folder_builder.write()

    def publish(self, command_context: CommandContext):
        """Publish the definition contained in the specified definition folder."""
        definition_folder = DefinitionFolder(command_context.cli_options["definition_folder"])
        definition_folder.deploy(config=self.config, command_context=command_context)

    def delete(self, command_context: CommandContext):
        """Delete the definition."""
        # Takes folder, deletes to Azure
        #  - Read folder/ create folder object
        #  - For each element (reversed):
        #    - Do element.delete()
        # TODO: Implement

    @abstractmethod
    def build_base_bicep(self):
        """ Build bicep file for underlying resources"""
    @abstractmethod
    def build_manifest_bicep(self):
        """Build the manifest bicep file."""
        raise NotImplementedError

    @abstractmethod
    def build_artifact_list(self):
        """Build the artifact list."""
        raise NotImplementedError

    @abstractmethod
    def build_resource_bicep(self, aosm_client=None):
        """Build the resource bicep file."""
        raise NotImplementedError

    @abstractmethod
    def build_common_parameters_json(self):
        """ Build common parameters.json file """
        raise NotImplementedError

    @abstractmethod
    def _get_input_config(self, input_config: dict = None) -> OnboardingBaseInputConfig:
        """Get the configuration for the command."""
        raise NotImplementedError

    @abstractmethod
    def _get_params_config(self, params_config: dict = None) -> BaseCommonParametersConfig:
        """ Get the parameters config for publish/delete """
        raise NotImplementedError

    def _read_input_config_from_file(self, input_json_path: Path) -> dict:
        """Reads the input JSONC file, removes comments + returns config as dictionary."""
        lines = input_json_path.read_text().splitlines()
        lines = [line for line in lines if not line.strip().startswith("//")]
        config_dict = json.loads("".join(lines))

        return config_dict

    def _read_params_config_from_file(self, input_json_path) -> dict:
        """ Reads input file, takes only the {parameters:values} + returns config as dictionary

            For example,
            {'location': {'value': 'test'} is returned as
            {'location': 'test'}

        """
        with open(input_json_path, "r", encoding="utf-8") as _file:
            params_schema = json.load(_file)
        params = params_schema["parameters"]
        return {param: params[param]["value"] for param in params}

    def _render_base_bicep_contents(self, template_path):
        """Write the base bicep file from given template."""
        with open(template_path, "r", encoding="UTF-8") as f:
            template: Template = Template(
                f.read(),
                undefined=StrictUndefined,
            )

        bicep_contents: str = template.render()
        return bicep_contents

    def _render_definition_bicep_contents(
        self,
        template_path: Path,
        acr_nf_application: list,
        sa_nf_application: AzureCoreNetworkFunctionVhdApplication = None,
    ):
        """Write the definition bicep file from given template."""
        with open(template_path, "r", encoding="UTF-8") as f:
            template: Template = Template(
                f.read(),
                undefined=StrictUndefined,
            )

        bicep_contents: str = template.render(
            acr_nf_applications=acr_nf_application, sa_nf_application=sa_nf_application
        )
        return bicep_contents

    def _render_manifest_bicep_contents(
        self,
        template_path: Path,
        acr_artifact_list: list,
        sa_artifact_list: list = None,
    ):
        """Write the manifest bicep file from given template.

        Returns bicep content as string
        """
        with open(template_path, "r", encoding="UTF-8") as f:
            template: Template = Template(
                f.read(),
                undefined=StrictUndefined,
            )

        bicep_contents: str = template.render(
            acr_artifacts=acr_artifact_list, sa_artifacts=sa_artifact_list
        )
        return bicep_contents

    def _get_template_path(self, definition_type: str, template_name: str) -> Path:
        """Get the path to a template."""
        return (
            Path(__file__).parent.parent
            / "common"
            / "templates"
            / definition_type
            / template_name
        )

    def _serialize(self, dataclass, indent_count=1):
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
            comment = field_info.metadata.get("comment", "")
            if comment:
                for line in comment.split("\n"):
                    jsonc_string.append(f"{indent}// {line}")

            if is_dataclass(field_value):
                # Serialize the nested dataclass and add it as a nested JSON object.
                # Checks if it is last field to omit trailing comma
                if field_info == fields(dataclass)[-1]:
                    nested_json = (
                        "{\n"
                        + self._serialize(field_value, indent_count + 1)
                        + "\n"
                        + indent
                        + "}"
                    )
                else:
                    nested_json = (
                        "{\n"
                        + self._serialize(field_value, indent_count + 1)
                        + "\n"
                        + indent
                        + "},"
                    )
                jsonc_string.append(f'{indent}"{field_info.name}": {nested_json}')
            elif isinstance(field_value, list):
                # If the value is a list, iterate over the items.
                jsonc_string.append(f'{indent}"{field_info.name}": [')
                for item in field_value:
                    # Check if the item is a dataclass and serialize it.
                    if is_dataclass(item):
                        inner_dataclass = self._serialize(item, indent_count + 2)
                        if item == field_value[-1]:
                            jsonc_string.append(
                                double_indent
                                + "{\n"
                                + inner_dataclass
                                + "\n"
                                + double_indent
                                + "}"
                            )
                        else:
                            jsonc_string.append(
                                double_indent
                                + "{\n"
                                + inner_dataclass
                                + "\n"
                                + double_indent
                                + "},"
                            )
                    else:
                        jsonc_string.append(json.dumps(item, indent=4) + ",")
                # If the field is the last field, omit the trailing comma.
                if field_info == fields(dataclass)[-1]:
                    jsonc_string.append(indent + "]")
                else:
                    jsonc_string.append(indent + "],")
            else:
                # If the value is a string, serialize it directly.
                if field_info == fields(dataclass)[-1]:
                    jsonc_string.append(
                        f'{indent}"{field_info.name}": {json.dumps(field_value,indent=4)}'
                    )
                else:
                    jsonc_string.append(
                        f'{indent}"{field_info.name}": {json.dumps(field_value,indent=4)},'
                    )
        return "\n".join(jsonc_string)

    def _write_config_to_file(self, output_path: Path):
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
