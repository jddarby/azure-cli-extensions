from pathlib import Path
from typing import Any, Dict, List
import tempfile
from utils.exceptions import InvalidFileTypeError, MissingChartDependencyError
import tarfile
import os
import shutil
import yaml
from dataclasses import dataclass


@dataclass
class HelmChartMetadata:
    name: str
    version: str
    description: str = None
    dependencies: List[str] = None


@dataclass
class HelmChartTemplate:
    name: str
    data: List[str]


class HelmChart:
    """
    A utility class for working with Helm charts.

    Attributes:
        chart_dir (Path): The path to the unpacked Helm chart.
    """

    def __init__(self, chart_path: Path):
        """Initialize the HelmChartUtils class."""
        if chart_path.is_dir():
            self.chart_dir = chart_path
        else:
            self.temp_dir_path = Path(tempfile.mkdtemp())
            self.chart_dir = self._extract_chart_to_dir(
                chart_path,
                self.temp_dir_path
            )
        self._validate()
        metadata = self._get_metadata()
        self.name = metadata.name
        self.version = metadata.version
        self.description = metadata.description
        self.dependencies = self._get_dependency_charts(metadata.dependencies)

    def _extract_chart_to_dir(self, chart_path: Path, target_dir: Path) -> Path:
        """
        Extract the chart into the target directory.

        Args:
            chart_path (Path): The path to the Helm chart.
            target_dir (Path): The path to the target directory where the chart
            will be extracted.

        Raises:
            InvalidFileTypeError: If the chart file is not a .tgz, .tar, or
            .tar.gz file.

        Returns:
            str: The path to the extracted chart.
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
                f"ERROR: The helm package '{chart_path}' is not"
                "a .tgz, .tar or .tar.gz file."
            )

        return Path(target_dir, os.listdir(target_dir)[0])

    def _validate(self):
        """
        Validate the Helm chart.
        """
        if not Path(self.chart_dir, "Chart.yaml").exists():
            raise FileNotFoundError(
                f"ERROR: The Helm chart '{self.chart_path}' does not contain"
                "a Chart.yaml file."
            )

    def _get_metadata(self) -> HelmChartMetadata:
        """
        Get the metadata from the Helm chart (Chart.yaml).

        Returns:
            HelmChartMetadata: The metadata from the Helm chart.
        """
        # The metadata is stored in the Chart.yaml file.
        chart_yaml_path = Path(self.chart_dir, "Chart.yaml")

        with chart_yaml_path.open(encoding="UTF-8") as chart_yaml_file:
            chart_yaml = yaml.safe_load(chart_yaml_file)

        # We only need the name of the dependency charts.
        dependencies = [
            dependency["name"] for dependency
            in chart_yaml.get("dependencies", [])
        ]

        return HelmChartMetadata(
            name=chart_yaml["name"],
            version=chart_yaml["version"],
            description=chart_yaml.get("description", None),
            dependencies=dependencies
        )

    def _get_dependency_charts(
        self, dependencies: List[str]
    ) -> List["HelmChart"]:
        """
        Get the dependency charts for the Helm chart.

        Args:
            dependencies (List[str]): The list of dependency helm chart names.

        Raises:
            InvalidChartDependencyError: If the chart dependency is not a local
            dependency.

        Returns:
            List[HelmChart]: A list of HelmChart objects for the dependency
            charts.
        """
        # All dependency charts should be located in the charts directory.
        dependency_chart_dir = Path(self.chart_dir, "charts")

        if not dependency_chart_dir.exists():
            assert len(dependencies) == 0
            return []

        # For each chart in the charts directory, create a HelmChart object.
        dependency_charts = [
            HelmChart(Path(dependency_chart_dir, chart_dir.name))
            for chart_dir in dependency_chart_dir.iterdir()
        ]

        # Check that the charts found in the charts directory match the
        # all the dependency names defined in Chart.yaml.
        for dependency in dependencies:
            if dependency not in [
                dependency_chart.name for dependency_chart in dependency_charts
            ]:
                raise MissingChartDependencyError(
                    f"ERROR: The Helm chart '{self.name}' has a"
                    f"dependency on the chart '{dependency}' which is not"
                    "a local dependency."
                )

        return dependency_charts

    def get_default_values(self) -> Dict[str, Any]:
        """
        Get the values file from the Helm chart.

        Returns:
            Dict[str, Any]: The values file.
        """
        for file in self.chart_dir.iterdir():
            if file.name.endswith(("values.yaml", "values.yml")):
                with file.open(encoding="UTF-8") as values_file:
                    values_yaml = yaml.safe_load(values_file)
                return values_yaml

        raise FileNotFoundError(
            f"ERROR: No values file was not found in the Helm chart"
            f" '{self.chart_path}'."
        )

    def get_templates(self) -> List[HelmChartTemplate]:
        """
        Get the templates from the Helm chart.
        """
        # Template files are located in the templates directory.
        template_dir = Path(self.chart_dir, "templates")
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

                templates.append(
                    HelmChartTemplate(name=file.name, data=template_data)
                )

        return templates

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.temp_dir_path)
