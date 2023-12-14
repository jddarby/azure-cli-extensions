# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, List

import genson
import yaml
from azext_aosm.common.exceptions import (
    DefaultValuesNotFoundError,
    MissingChartDependencyError,
    SchemaGetOrGenerateError,
)
from azext_aosm.common.utils import extract_tarfile
from azext_aosm.inputs.base_input import BaseInput


@dataclass
class HelmChartMetadata:
    name: str
    version: str
    dependencies: List[str] = None


@dataclass
class HelmChartTemplate:
    name: str
    data: List[str]


class HelmChart(BaseInput):
    """
    A utility class for working with Helm charts.
    """

    def __init__(
        self,
        artifact_name: str,
        artifact_version: str,
        chart_path: Path,
        default_config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the HelmChart class."""
        super().__init__(artifact_name, artifact_version, default_config)
        self.chart_path = chart_path
        self._temp_dir_path = Path(tempfile.mkdtemp())
        if chart_path.is_dir():
            self._chart_dir = chart_path
        else:
            self._chart_dir = extract_tarfile(chart_path, self._temp_dir_path)
        self._validate()
        self.metadata = self._get_metadata()

    @staticmethod
    def from_chart_path(
        chart_path: Path, default_config: Optional[Dict[str, Any]]
    ) -> "HelmChart":
        """Create a HelmChart object from a HelmPackageConfig object."""
        temp_dir = Path(tempfile.mkdtemp())

        if chart_path.is_dir():
            chart_path = extract_tarfile(chart_path, temp_dir)
        else:
            chart_path = Path(chart_path)

        name, version = HelmChart._get_name_and_version(chart_path)

        shutil.rmtree(temp_dir)

        return HelmChart(
            artifact_name=name,
            artifact_version=version,
            chart_path=chart_path,
            default_config=default_config,
        )

    def get_defaults(self) -> Dict[str, Any]:
        """
        Retrieves the default values from the values.yaml or values.yml file in the Helm chart directory.

        Returns:
            Dict[str, Any]: The default values the Helm chart.

        Raises:
            DefaultValuesNotFoundError: If no default values file is given by the user or
            found in the Helm chart directory.
        """
        try:
            return self.default_config or self._read_values_yaml()
        except FileNotFoundError as error:
            raise DefaultValuesNotFoundError(
                "ERROR: No default values found for the Helm chart"
                f" '{self.chart_path}'. Please provide default values"
                " or add a values.yaml file to the Helm chart."
            ) from error

    def get_schema(self) -> Dict[str, Any]:
        """
        Retrieves the schema for the Helm chart.

        If a values.schema.json file is present in the chart directory, it is used as the schema.
        Otherwise, a schema is generated from the values in values.yaml.

        Returns:
            Dict[str, Any]: The schema for the Helm chart.

        Raises:
            SchemaGetOrGenerateError: If the schema cannot be generated or retrieved.
        """
        try:
            # Use the schema provided in the chart if there is one.
            for file in self._chart_dir.iterdir():
                if file.name == "values.schema.json":
                    with file.open(encoding="UTF-8") as schema_file:
                        schema = json.load(schema_file)
                    return schema

            # Otherwise, generate a schema from the default values in values.yaml.
            schema = genson.Schema()
            schema.add_object(self._read_values_yaml())
            return schema.to_dict()
        except FileNotFoundError as error:
            raise SchemaGetOrGenerateError(
                "ERROR: Encountered an error while trying to generate or"
                f" retrieve the helm chart values schema:\n{error}"
            ) from error

    def get_dependencies(self) -> List["HelmChart"]:
        """
        Get the dependency charts for the Helm chart.

        Returns:
            List["HelmChart"]: The dependency charts for the Helm chart.

        Raises:
            MissingChartDependencyError: If the Helm chart has a dependency on a chart
            that is not a local dependency.
        """
        # All dependency charts should be located in the charts directory.
        dependency_chart_dir = Path(self._chart_dir, "charts")

        if not dependency_chart_dir.exists():
            assert len(self.metadata.dependencies) == 0
            return []

        # For each chart in the charts directory, create a HelmChart object.
        dependency_charts = [
            HelmChart.from_chart_path(Path(chart_dir), None)
            for chart_dir in dependency_chart_dir.iterdir()
        ]

        # Check that the charts found in the charts directory match the
        # all the dependency names defined in Chart.yaml.
        for dependency in self.metadata.dependencies:
            if dependency not in [
                dependency_chart.metadata.name for dependency_chart in dependency_charts
            ]:
                raise MissingChartDependencyError(
                    f"ERROR: The Helm chart '{self.metadata.name}' has a"
                    f"dependency on the chart '{dependency}' which is not"
                    "a local dependency."
                )

        return dependency_charts

    def get_templates(self) -> List[HelmChartTemplate]:
        """
        Get the templates for the Helm chart.

        Returns:
            List[HelmChartTemplate]: The templates for the Helm chart.
        """
        # Template files are located in the templates directory.
        template_dir = Path(self._chart_dir, "templates")
        templates: List[HelmChartTemplate] = []

        # TODO: Decide whether to raise an exception if the templates directory
        # does not exist.
        if not template_dir.exists():
            return templates

        for file in template_dir.iterdir():
            # Template files are only ever YAML files.
            if file.name.endswith(".yaml"):
                with file.open(encoding="UTF-8") as template_file:
                    template_data = template_file.readlines()

                templates.append(HelmChartTemplate(name=file.name, data=template_data))

        return templates

    @staticmethod
    def _get_name_and_version(chart_dir: Path) -> (str, str):
        """
        Retrieves the name and version of the Helm chart.

        Args:
            chart_dir (Path): The path to the Helm chart directory.

        Returns:
            (str, str): The name and version of the Helm chart.
        """
        chart_yaml_path = Path(chart_dir, "Chart.yaml")

        with chart_yaml_path.open(encoding="UTF-8") as chart_yaml_file:
            chart_yaml = yaml.safe_load(chart_yaml_file)

        return chart_yaml["name"], chart_yaml["version"]

    def _validate(self):
        """
        Validates the Helm chart by checking if the Chart.yaml file exists.

        Raises:
            FileNotFoundError: If the Chart.yaml file does not exist.
        """
        if not Path(self._chart_dir, "Chart.yaml").exists():
            raise FileNotFoundError(
                f"ERROR: The Helm chart '{self.chart_path}' does not contain"
                "a Chart.yaml file."
            )

    def _get_metadata(self) -> HelmChartMetadata:
        """
        Retrieves the metadata of the Helm chart.

        Returns:
            HelmChartMetadata: The metadata of the Helm chart.
        """
        # The metadata is stored in the Chart.yaml file.
        chart_yaml_path = Path(self._chart_dir, "Chart.yaml")

        with chart_yaml_path.open(encoding="UTF-8") as chart_yaml_file:
            chart_yaml = yaml.safe_load(chart_yaml_file)

        # We only need the name of the dependency charts.
        dependencies = [
            dependency["name"] for dependency in chart_yaml.get("dependencies", [])
        ]

        return HelmChartMetadata(
            name=chart_yaml["name"],
            version=chart_yaml["version"],
            dependencies=dependencies,
        )

    def _read_values_yaml(self) -> Dict[str, Any]:
        """
        Reads the values.yaml file in the Helm chart directory.

        Returns:
            Dict[str, Any]: The values in the values.yaml file.

        Raises:
            FileNotFoundError: If no values file was found in the Helm chart directory.
        """
        for file in self._chart_dir.iterdir():
            if file.name.endswith(("values.yaml", "values.yml")):
                with file.open(encoding="UTF-8") as f:
                    content = yaml.safe_load(f)
                return content

        raise FileNotFoundError(
            f"ERROR: No values file was found in the Helm chart"
            f" '{self.chart_path}'."
        )

    def __del__(self):
        shutil.rmtree(self._temp_dir_path)
