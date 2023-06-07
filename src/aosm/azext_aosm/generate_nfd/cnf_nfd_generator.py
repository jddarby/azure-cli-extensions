# --------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT
# License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------
"""Contains a class for generating CNF NFDs and associated resources."""
import json
import os
import re
import shutil
import tarfile
import tempfile
from typing import Any, Dict, Iterator, List, Optional, Tuple

import yaml
from azure.cli.core.azclierror import FileOperationError, InvalidTemplateError
from jinja2 import StrictUndefined, Template
from knack.log import get_logger

from azext_aosm._configuration import CNFConfiguration, HelmPackageConfig
from azext_aosm.generate_nfd.nfd_generator_base import NFDGenerator
from azext_aosm.util.constants import (
    CNF_DEFINITION_BICEP_TEMPLATE,
    CNF_DEFINITION_JINJA2_SOURCE_TEMPLATE,
    CNF_MANIFEST_BICEP_TEMPLATE,
    CNF_MANIFEST_JINJA2_SOURCE_TEMPLATE,
    CONFIG_MAPPINGS,
    DEPLOYMENT_PARAMETER_MAPPING_REGEX,
    DEPLOYMENT_PARAMETERS,
    GENERATED_VALUES_MAPPINGS,
    IMAGE_LINE_REGEX,
    IMAGE_PULL_SECRET_LINE_REGEX,
    SCHEMA_PREFIX,
    SCHEMAS,
)
from azext_aosm.util.utils import input_ack

logger = get_logger(__name__)


class CnfNfdGenerator(NFDGenerator):  # pylint: disable=too-many-instance-attributes
    """
    CNF NFD Generator.

    This takes a config file, and outputs:
    - A bicep file for the NFDV
    - Parameters files that are used by the NFDV bicep file, these are the
      deployParameters and the mapping profiles of those deploy parameters
    - A bicep file for the Artifact manifests
    """

    def __init__(self, config: CNFConfiguration, interactive: bool = False):
        """
        Create a new CNF NFD Generator.

        Interactive parameter is only used if the user wants to generate the values
        mapping file from the values.yaml in the helm package, and also requires the
        mapping file in config to be blank.
        """
        super(NFDGenerator, self).__init__()
        self.config = config
        self.nfd_jinja2_template_path = os.path.join(
            os.path.dirname(__file__),
            "templates",
            CNF_DEFINITION_JINJA2_SOURCE_TEMPLATE,
        )
        self.manifest_jinja2_template_path = os.path.join(
            os.path.dirname(__file__),
            "templates",
            CNF_MANIFEST_JINJA2_SOURCE_TEMPLATE,
        )
        self.output_folder_name = self.config.build_output_folder_name

        self.artifacts = []
        self.nf_application_configurations = []
        self.deployment_parameter_schema = SCHEMA_PREFIX

        self._bicep_path = os.path.join(
            self.output_folder_name, CNF_DEFINITION_BICEP_TEMPLATE
        )
        self.interactive = interactive
        self._tmp_folder_name = ""

    def generate_nfd(self) -> None:
        """Generate a CNF NFD which comprises a group, an Artifact Manifest and an NFDV."""

        # Create temporary folder.
        with tempfile.TemporaryDirectory() as tmpdirname:
            self._tmp_folder_name = tmpdirname
            try:
                for helm_package in self.config.helm_packages:
                    # Turn Any type into HelmPackageConfig, to access properties on the object
                    helm_package = HelmPackageConfig(**helm_package)

                    # Unpack the chart into the tmp folder
                    self._extract_chart(helm_package.path_to_chart)

                    # TODO: Validate charts

                    # Create a chart mapping schema if none has been passed in.
                    if (
                        not helm_package.path_to_mappings
                        or helm_package.path_to_mappings == ""
                    ):
                        self._generate_chart_value_mappings(helm_package)

                    # Get schema for each chart
                    # (extract mappings and take the schema bits we need from values.schema.json)
                    # + Add that schema to the big schema.
                    self.deployment_parameter_schema["properties"].update(
                        self.get_chart_mapping_schema(helm_package)
                    )

                    # Get all image line matches for files in the chart.
                    # Do this here so we don't have to do it multiple times.
                    image_line_matches = self.find_pattern_matches_in_chart(
                        helm_package, IMAGE_LINE_REGEX
                    )

                    # Generate the NF application configuration for the chart
                    # passed to jinja2 renderer to render bicep template
                    self.nf_application_configurations.append(
                        self.generate_nf_application_config(
                            helm_package,
                            image_line_matches,
                            self.find_pattern_matches_in_chart(
                                helm_package, IMAGE_PULL_SECRET_LINE_REGEX
                            ),
                        )
                    )
                    # Workout the list of artifacts for the chart and
                    # update the list for the NFD with any unique artifacts.
                    chart_artifacts = self.get_artifact_list(
                        helm_package, set(image_line_matches)
                    )
                    self.artifacts += [
                        a for a in chart_artifacts if a not in self.artifacts
                    ]
                self.write_nfd_bicep_file()
                self.write_schema_to_file()
                self.write_manifest_bicep_file()
                self.copy_to_output_folder()
                print(
                    f"Generated NFD bicep template created in {self.output_folder_name}"
                )
                print(
                    "Please review these templates."
                    "If you are happy with them, you should manually deploy your bicep "
                    "templates and upload your charts and images to your "
                    "artifact store."
                )
            except InvalidTemplateError as e:
                raise e

    @property
    def bicep_path(self) -> Optional[str]:
        """Returns the path to the bicep file for the NFD if it has been created."""
        if os.path.exists(self._bicep_path):
            return self._bicep_path

        return None

    def _extract_chart(self, path: str) -> None:
        """
        Extract the chart into the tmp folder.

        :param path: The path to helm package
        """

        logger.debug("Extracting helm package %s", path)

        (_, ext) = os.path.splitext(path)
        if ext in (".gz", ".tgz"):
            with tarfile.open(path, "r:gz") as tar:
                tar.extractall(path=self._tmp_folder_name)

        elif ext == ".tar":
            with tarfile.open(path, "r:") as tar:
                tar.extractall(path=self._tmp_folder_name)

        else:
            raise InvalidTemplateError(
                f"ERROR: The helm package '{path}' is not a .tgz, .tar or .tar.gz file.\
                Please fix this and run the command again."
            )

    def _generate_chart_value_mappings(self, helm_package: HelmPackageConfig) -> None:
        """
        Optional function to create a chart value mappings file with every value being a deployParameter.

        Expected use when a helm chart is very simple and user wants every value to be a
        deployment parameter.
        """
        logger.debug(
            "Creating chart value mappings file for %s", helm_package.path_to_chart
        )
        print("Creating chart value mappings file for %s", helm_package.path_to_chart)

        # Get all the values files in the chart
        top_level_values_yaml = self._read_top_level_values_yaml(helm_package)

        mapping_to_write = self._replace_values_with_deploy_params(
            top_level_values_yaml, {}
        )

        # Write the mapping to a file
        folder_name = os.path.join(self._tmp_folder_name, GENERATED_VALUES_MAPPINGS)
        os.makedirs(folder_name, exist_ok=True)
        mapping_filepath = os.path.join(
            self._tmp_folder_name,
            GENERATED_VALUES_MAPPINGS,
            f"{helm_package.name}_generated-mapping.yaml",
        )
        with open(mapping_filepath, "w", encoding="UTF-8") as mapping_file:
            yaml.dump(mapping_to_write, mapping_file)

        # Update the config that points to the mapping file
        helm_package.path_to_mappings = mapping_filepath

    def _read_top_level_values_yaml(
        self, helm_package: HelmPackageConfig
    ) -> Dict[str, Any]:
        for file in os.listdir(os.path.join(self._tmp_folder_name, helm_package.name)):
            if file in ("values.yaml", "values.yml"):
                with open(
                    os.path.join(self._tmp_folder_name, helm_package.name, file),
                    "r",
                    encoding="UTF-8",
                ) as values_file:
                    values_yaml = yaml.safe_load(values_file)
                return values_yaml

        raise FileOperationError(
            "Cannot find top level values.yaml/.yml file in Helm package."
        )

    def write_manifest_bicep_file(self) -> None:
        """Write the bicep file for the Artifact Manifest."""
        with open(self.manifest_jinja2_template_path, "r", encoding="UTF-8") as f:
            template: Template = Template(
                f.read(),
                undefined=StrictUndefined,
            )

        bicep_contents: str = template.render(
            artifacts=self.artifacts,
        )

        path = os.path.join(self._tmp_folder_name, CNF_MANIFEST_BICEP_TEMPLATE)
        with open(path, "w", encoding="utf-8") as f:
            f.write(bicep_contents)

        logger.info("Created artifact manifest bicep template: %s", path)

    def write_nfd_bicep_file(self) -> None:
        """Write the bicep file for the NFD."""
        with open(self.nfd_jinja2_template_path, "r", encoding="UTF-8") as f:
            template: Template = Template(
                f.read(),
                undefined=StrictUndefined,
            )

        bicep_contents: str = template.render(
            deployParametersPath=os.path.join(SCHEMAS, DEPLOYMENT_PARAMETERS),
            nf_application_configurations=self.nf_application_configurations,
        )

        path = os.path.join(self._tmp_folder_name, CNF_DEFINITION_BICEP_TEMPLATE)
        with open(path, "w", encoding="utf-8") as f:
            f.write(bicep_contents)

        logger.info("Created NFD bicep template: %s", path)

    def write_schema_to_file(self) -> None:
        """Write the schema to file deploymentParameters.json."""

        logger.debug("Create deploymentParameters.json")

        full_schema = os.path.join(self._tmp_folder_name, DEPLOYMENT_PARAMETERS)
        with open(full_schema, "w", encoding="UTF-8") as f:
            json.dump(self.deployment_parameter_schema, f, indent=4)

        logger.debug("%s created", full_schema)

    def copy_to_output_folder(self) -> None:
        """Copy the config mappings, schema and bicep templates (artifact manifest and NFDV) to the output folder."""

        logger.info("Create NFD bicep %s", self.output_folder_name)

        os.mkdir(self.output_folder_name)
        os.mkdir(os.path.join(self.output_folder_name, SCHEMAS))

        tmp_nfd_bicep_path = os.path.join(
            self._tmp_folder_name, CNF_DEFINITION_BICEP_TEMPLATE
        )
        shutil.copy(tmp_nfd_bicep_path, self.output_folder_name)

        tmp_manifest_bicep_path = os.path.join(
            self._tmp_folder_name, CNF_MANIFEST_BICEP_TEMPLATE
        )
        shutil.copy(tmp_manifest_bicep_path, self.output_folder_name)
        if os.path.exists(
            os.path.join(self._tmp_folder_name, GENERATED_VALUES_MAPPINGS)
        ):
            generated_mappings_path = os.path.join(
                self.output_folder_name, GENERATED_VALUES_MAPPINGS
            )
            shutil.copytree(
                os.path.join(self._tmp_folder_name, GENERATED_VALUES_MAPPINGS),
                generated_mappings_path,
            )

        tmp_config_mappings_path = os.path.join(self._tmp_folder_name, CONFIG_MAPPINGS)
        output_config_mappings_path = os.path.join(
            self.output_folder_name, CONFIG_MAPPINGS
        )
        shutil.copytree(
            tmp_config_mappings_path,
            output_config_mappings_path,
            dirs_exist_ok=True,
        )

        tmp_schema_path = os.path.join(self._tmp_folder_name, DEPLOYMENT_PARAMETERS)
        output_schema_path = os.path.join(
            self.output_folder_name, SCHEMAS, DEPLOYMENT_PARAMETERS
        )
        shutil.copy(
            tmp_schema_path,
            output_schema_path,
        )

        logger.info("Copied files to %s", self.output_folder_name)

    def generate_nf_application_config(
        self,
        helm_package: HelmPackageConfig,
        image_line_matches: List[Tuple[str, ...]],
        image_pull_secret_line_matches: List[Tuple[str, ...]],
    ) -> Dict[str, Any]:
        """Generate NF application config."""
        (name, version) = self.get_chart_name_and_version(helm_package)
        registryValuesPaths = set({m[0] for m in image_line_matches})
        imagePullSecretsValuesPaths = set(image_pull_secret_line_matches)

        return {
            "name": helm_package.name,
            "chartName": name,
            "chartVersion": version,
            "dependsOnProfile": helm_package.depends_on,
            "registryValuesPaths": list(registryValuesPaths),
            "imagePullSecretsValuesPaths": list(imagePullSecretsValuesPaths),
            "valueMappingsPath": self.generate_parameter_mappings(helm_package),
        }

    def _find_yaml_files(self, directory) -> Iterator[str]:
        """
        Find all yaml files in given directory.

        :param directory: The directory to search.
        """
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".yaml") or file.endswith(".yml"):
                    yield os.path.join(root, file)

    def find_pattern_matches_in_chart(
        self, helm_package: HelmPackageConfig, pattern: str
    ) -> List[Tuple[str, ...]]:
        """
        Find pattern matches in Helm chart, using provided REGEX pattern.

        param helm_package: The helm package config. param pattern: The regex pattern to
        match.
        """
        chart_dir = os.path.join(self._tmp_folder_name, helm_package.name)
        matches = []

        for file in self._find_yaml_files(chart_dir):
            with open(file, "r", encoding="UTF-8") as f:
                contents = f.read()
                matches += re.findall(pattern, contents)

        return matches

    def get_artifact_list(
        self,
        helm_package: HelmPackageConfig,
        image_line_matches: List[Tuple[str, ...]],
    ) -> List[Any]:
        """
        Get the list of artifacts for the chart.

        param helm_package: The helm package config. param image_line_matches: The list
        of image line matches.
        """
        artifact_list = []
        (chart_name, chart_version) = self.get_chart_name_and_version(helm_package)
        helm_artifact = {
            "name": chart_name,
            "version": chart_version,
        }
        artifact_list.append(helm_artifact)

        for match in image_line_matches:
            artifact_list.append(
                {
                    "name": match[1],
                    "version": match[2],
                }
            )

        return artifact_list

    def get_chart_mapping_schema(
        self, helm_package: HelmPackageConfig
    ) -> Dict[Any, Any]:
        """
        Get the schema for the non default values (those with {deploymentParameter...}).
        Based on user provided values.schema.json.

        param helm_package: The helm package config.
        """

        logger.debug("Get chart mapping schema for %s", helm_package.name)

        mappings_path = helm_package.path_to_mappings
        values_schema = os.path.join(
            self._tmp_folder_name, helm_package.name, "values.schema.json"
        )

        if not os.path.exists(mappings_path):
            raise InvalidTemplateError(
                f"ERROR: The helm package '{helm_package.name}' does not have a valid values mappings file. \
                    The file at '{helm_package.path_to_mappings}' does not exist.\n\
                    Please fix this and run the command again."
            )
        if not os.path.exists(values_schema):
            raise InvalidTemplateError(
                f"ERROR: The helm package '{helm_package.name}' is missing values.schema.json. \
                    Please fix this and run the command again."
            )

        with open(mappings_path, "r", encoding="utf-8") as stream:
            values_data = yaml.load(stream, Loader=yaml.SafeLoader)

        with open(values_schema, "r", encoding="utf-8") as f:
            data = json.load(f)
            schema_data = data["properties"]

        try:
            final_schema = self.find_deploy_params(values_data, schema_data, {})
        except KeyError as e:
            raise InvalidTemplateError(
                f"ERROR: Your schema and values for the helm package '{helm_package.name}' do not match. \
                    Please fix this and run the command again."
            ) from e

        logger.debug("Generated chart mapping schema for %s", helm_package.name)
        return final_schema

    def _replace_values_with_deploy_params(
        self,
        values_yaml_dict,
        final_values_mapping_dict,
        key_prefix: Optional[str] = None,
    ) -> Dict[Any, Any]:
        """
        Given the yaml dictionary read from values.yaml, replace all the values with {deploymentParameter.keyname}.

        Thus creating a values mapping file if the user has not provided one in config.
        """
        for k, v in values_yaml_dict.items():
            # if value is a string and contains deployParameters.
            if isinstance(v, (str, int, bool)):
                # Replace the parameter with {deploymentParameter.keyname}
                if key_prefix:
                    param_name = f"{key_prefix}_{k}"
                else:
                    param_name = k
                if self.interactive:
                    # Interactive mode. Prompt user to include or exclude parameters
                    # This requires the enter key after the y/n input which isn't ideal
                    if not input_ack("y", f"Expose parameter {param_name}? y/n "):
                        logger.debug("Excluding parameter %s", param_name)
                        final_values_mapping_dict.update({k: v})
                        continue
                replacement_value = f"{{deploymentParameter.{param_name}}}"

                # add the schema for k (from the big schema) to the (smaller) schema
                final_values_mapping_dict.update({k: replacement_value})
            elif isinstance(v, dict):
                new_key_prefix = k if key_prefix is None else f"{key_prefix}_{k}"
                final_values_mapping_dict[k] = self._replace_values_with_deploy_params(
                    v, {}, new_key_prefix
                )
            elif isinstance(v, list):
                final_values_mapping_dict[k] = []
                for index, item in enumerate(v):
                    if isinstance(item, dict):
                        new_key_prefix = (
                            k if key_prefix is None else f"{key_prefix}_{k}"
                        )
                        final_values_mapping_dict[k].append(
                            self._replace_values_with_deploy_params(
                                item, {}, new_key_prefix
                            )
                        )
                    else:
                        if key_prefix:
                            param_name = f"{key_prefix}_{k}_{index}"
                        else:
                            param_name = f"{k})_{index}"
                        replacement_value = f"{{deploymentParameter.{param_name}}}"
                        final_values_mapping_dict[k].append(replacement_value)

        return final_values_mapping_dict

    def find_deploy_params(
        self, nested_dict, schema_nested_dict, final_schema
    ) -> Dict[Any, Any]:
        """Find the deploy parameters in the values.mappings.yaml file and add them to the schema."""
        original_schema_nested_dict = schema_nested_dict
        for k, v in nested_dict.items():
            # if value is a string and contains deployParameters.
            if isinstance(v, str) and re.search(DEPLOYMENT_PARAMETER_MAPPING_REGEX, v):
                # only add the parameter name (e.g. from {deployParameter.zone} only param = zone)
                param = v.split(".", 1)[1]
                param = param.split("}", 1)[0]

                # add the schema for k (from the big schema) to the (smaller) schema
                final_schema.update(
                    {param: {"type": schema_nested_dict["properties"][k]["type"]}}
                )

            # else if value is a (non-empty) dictionary (i.e another layer of nesting)
            elif hasattr(v, "items") and v.items():
                # handling schema having properties which doesn't map directly to the values file nesting
                if "properties" in schema_nested_dict.keys():
                    schema_nested_dict = schema_nested_dict["properties"][k]
                else:
                    schema_nested_dict = schema_nested_dict[k]
                # recursively call function with values (i.e the nested dictionary)
                self.find_deploy_params(v, schema_nested_dict, final_schema)
                # reset the schema dict to its original value (once finished with that level of recursion)
                schema_nested_dict = original_schema_nested_dict

        return final_schema

    def get_chart_name_and_version(
        self, helm_package: HelmPackageConfig
    ) -> Tuple[str, str]:
        """Get the name and version of the chart."""
        chart = os.path.join(self._tmp_folder_name, helm_package.name, "Chart.yaml")

        if not os.path.exists(chart):
            raise InvalidTemplateError(
                f"There is no Chart.yaml file in the helm package '{helm_package.name}'. \
                    Please fix this and run the command again."
            )

        with open(chart, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if "name" in data and "version" in data:
                chart_name = data["name"]
                chart_version = data["version"]
            else:
                raise FileOperationError(
                    f"A name or version is missing from Chart.yaml in the helm package '{helm_package.name}'. \
                        Please fix this and run the command again."
                )

        return (chart_name, chart_version)

    def generate_parameter_mappings(self, helm_package: HelmPackageConfig) -> str:
        """Generate parameter mappings for the given helm package."""
        values = os.path.join(
            self._tmp_folder_name, helm_package.name, "values.mappings.yaml"
        )

        mappings_folder_path = os.path.join(self._tmp_folder_name, CONFIG_MAPPINGS)
        mappings_filename = f"{helm_package.name}-mappings.json"

        if not os.path.exists(mappings_folder_path):
            os.mkdir(mappings_folder_path)

        mapping_file_path = os.path.join(mappings_folder_path, mappings_filename)

        with open(values, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        with open(mapping_file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        logger.debug("Generated parameter mappings for %s", helm_package.name)
        return os.path.join(CONFIG_MAPPINGS, mappings_filename)
