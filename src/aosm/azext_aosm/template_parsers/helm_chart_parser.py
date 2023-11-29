import json
import os
import shutil
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import genson
import yaml
from common.exceptions import DefaultValuesNotFoundError, InvalidFileTypeError, MissingChartDependencyError, SchemaGetOrGenerateError
from template_parsers.base_parser import BaseParser


@dataclass
class HelmChartMetadata:
    name: str
    version: str
    dependencies: List[str] = None


@dataclass
class HelmChartTemplate:
    name: str
    data: List[str]


class HelmChart(BaseParser):
    def __init__(self, chart_path: Path, defaults_path: Path = None):
        super().__init__(chart_path, defaults_path)
        self._temp_dir_path = Path(tempfile.mkdtemp())
        if chart_path.is_dir():
            self._chart_dir = chart_path
        else:
            self._chart_dir = self._extract_chart_to_dir(chart_path, self._temp_dir_path)
        self._validate()
        self.metadata = self._get_metadata()

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
                if self.defaults_path:
                    with self.defaults_path.open(encoding="UTF-8") as values_file:
                        values_yaml = yaml.safe_load(values_file)
                    return values_yaml
                else:
                    return self._read_values_yaml()
            except FileNotFoundError:
                raise DefaultValuesNotFoundError(
                    "ERROR: No default values file was found for the Helm chart"
                    f" '{self.chart_path}'. Please provide a default values file"
                    " or add a values.yaml file to the Helm chart."
                )

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
                )

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
            HelmChart(Path(dependency_chart_dir, chart_dir.name))
            for chart_dir in dependency_chart_dir.iterdir()
        ]

        # Check that the charts found in the charts directory match the
        # all the dependency names defined in Chart.yaml.
        for dependency in self.metadata.dependencies:
            if dependency not in [
                dependency_chart.name for dependency_chart in dependency_charts
            ]:
                raise MissingChartDependencyError(
                    f"ERROR: The Helm chart '{self.name}' has a"
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
        templates = []

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

    def _extract_chart_to_dir(self, chart_path: Path, target_dir: Path) -> Path:
            """
            Extracts the helm chart package to the target directory.

            Args:
                chart_path (Path): The path to the helm chart package.
                target_dir (Path): The target directory to extract the chart to.

            Returns:
                Path: The path to the extracted chart directory.

            Raises:
                InvalidFileTypeError: If the file type is not supported by the parser.
            """
            file_extension = chart_path.suffix

            if file_extension in (".gz", ".tgz"):
                with tarfile.open(chart_path, "r:gz") as tar:
                    tar.extractall(path=target_dir)
            elif file_extension == ".tar":
                with tarfile.open(chart_path, "r:") as tar:
                    tar.extractall(path=target_dir)
            else:
                raise InvalidFileTypeError(
                    f"ERROR: The helm package, '{chart_path}', is not"
                    "a .tgz, .tar or .tar.gz file."
                )

            return Path(target_dir, os.listdir(target_dir)[0])

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
