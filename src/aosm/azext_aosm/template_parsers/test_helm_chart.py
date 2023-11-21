import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from aosm.azext_aosm.template_parsers.helm_chart import (
    HelmChart,
    HelmChartMetadata,
    HelmChartTemplate,
    InvalidChartDependencyError,
    InvalidFileTypeError,
    MissingChartDependencyError,
)


class HelmChartTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.chart_dir = Path(self.temp_dir, "mychart")
        self.chart_dir.mkdir()
        self.chart_yaml_path = Path(self.chart_dir, "Chart.yaml")
        self.chart_yaml_path.write_text(
            """
            name: mychart
            version: 0.1.0
            description: A Helm chart for testing.
            dependencies:
              - name: dependency1
                version: 1.0.0
              - name: dependency2
                version: 2.0.0
            """
        )
        self.values_path = Path(self.chart_dir, "values.yaml")
        self.values_path.write_text(
            """
            key1: value1
            key2: value2
            """
        )
        self.templates_dir = Path(self.chart_dir, "templates")
        self.templates_dir.mkdir()
        self.template1_path = Path(self.templates_dir, "template1.yaml")
        self.template1_path.write_text(
            """
            apiVersion: v1
            kind: Service
            metadata:
              name: {{ .Release.Name }}-web
            """
        )
        self.template2_path = Path(self.templates_dir, "template2.txt")
        self.template2_path.write_text("This is not a YAML file.")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_init_with_valid_chart(self):
        chart = HelmChart(self.chart_dir)
        self.assertEqual(chart.name, "mychart")
        self.assertEqual(chart.version, "0.1.0")
        self.assertEqual(chart.description, "A Helm chart for testing.")
        self.assertEqual(len(chart.dependencies), 2)
        self.assertEqual(chart.dependencies[0].name, "dependency1")
        self.assertEqual(chart.dependencies[0].version, "1.0.0")
        self.assertEqual(chart.dependencies[1].name, "dependency2")
        self.assertEqual(chart.dependencies[1].version, "2.0.0")

    def test_init_with_invalid_chart(self):
        with self.assertRaises(FileNotFoundError):
            HelmChart(Path(self.temp_dir, "invalid_chart"))

    def test_init_with_invalid_file_type(self):
        invalid_file_path = Path(self.temp_dir, "invalid_file.txt")
        invalid_file_path.write_text("This is not a Helm chart.")
        with self.assertRaises(InvalidFileTypeError):
            HelmChart(invalid_file_path)

    def test_extract_chart_to_dir_with_tgz_file(self):
        chart_tgz_path = Path(self.temp_dir, "mychart.tgz")
        with tarfile.open(chart_tgz_path, "w:gz") as tar:
            tar.add(self.chart_dir, arcname="mychart")
        chart_dir = HelmChart(chart_tgz_path).chart_dir
        self.assertTrue(chart_dir.is_dir())
        self.assertEqual(chart_dir.name, "mychart")
        self.assertTrue(Path(chart_dir, "Chart.yaml").exists())

    def test_extract_chart_to_dir_with_tar_file(self):
        chart_tar_path = Path(self.temp_dir, "mychart.tar")
        with tarfile.open(chart_tar_path, "w:") as tar:
            tar.add(self.chart_dir, arcname="mychart")
        chart_dir = HelmChart(chart_tar_path).chart_dir
        self.assertTrue(chart_dir.is_dir())
        self.assertEqual(chart_dir.name, "mychart")
        self.assertTrue(Path(chart_dir, "Chart.yaml").exists())

    def test_extract_chart_to_dir_with_tgz_file(self):
        chart_tgz_path = Path(self.temp_dir, "mychart.tgz")
        with tarfile.open(chart_tgz_path, "w:gz") as tar:
            tar.add(self.chart_dir, arcname="mychart")
        chart_dir = HelmChart(chart_tgz_path).chart_dir
        self.assertTrue(chart_dir.is_dir())
        self.assertEqual(chart_dir.name, "mychart")
        self.assertTrue(Path(chart_dir, "Chart.yaml").exists())

    def test_extract_chart_to_dir_with_invalid_file_type(self):
        invalid_file_path = Path(self.temp_dir, "invalid_file.txt")
        invalid_file_path.write_text("This is not a Helm chart.")
        with self.assertRaises(InvalidFileTypeError):
            HelmChart(invalid_file_path)

    def test_validate_with_valid_chart(self):
        chart = HelmChart(self.chart_dir)
        chart._validate()

    def test_validate_with_invalid_chart(self):
        chart_dir = Path(self.temp_dir, "invalid_chart")
        chart_dir.mkdir()
        with self.assertRaises(FileNotFoundError):
            HelmChart(chart_dir)._validate()

    def test_get_metadata(self):
        chart = HelmChart(self.chart_dir)
        metadata = chart._get_metadata()
        self.assertIsInstance(metadata, HelmChartMetadata)
        self.assertEqual(metadata.name, "mychart")
        self.assertEqual(metadata.version, "0.1.0")
        self.assertEqual(metadata.description, "A Helm chart for testing.")
        self.assertEqual(len(metadata.dependencies), 2)
        self.assertEqual(metadata.dependencies[0], "dependency1")
        self.assertEqual(metadata.dependencies[1], "dependency2")

    def test_get_dependency_charts_with_valid_chart(self):
        chart = HelmChart(self.chart_dir)
        dependency_charts = chart._get_dependency_charts(["dependency1", "dependency2"])
        self.assertEqual(len(dependency_charts), 2)
        self.assertEqual(dependency_charts[0].name, "dependency1")
        self.assertEqual(dependency_charts[0].version, "1.0.0")
        self.assertEqual(dependency_charts[1].name, "dependency2")
        self.assertEqual(dependency_charts[1].version, "2.0.0")

    def test_get_dependency_charts_with_missing_dependency(self):
        chart = HelmChart(self.chart_dir)
        with self.assertRaises(MissingChartDependencyError):
            chart._get_dependency_charts(["dependency1", "dependency3"])

    def test_get_default_values(self):
        chart = HelmChart(self.chart_dir)
        values = chart.get_default_values()
        self.assertIsInstance(values, dict)
        self.assertEqual(values["key1"], "value1")
        self.assertEqual(values["key2"], "value2")

    def test_get_templates(self):
        chart = HelmChart(self.chart_dir)
        templates = chart.get_templates()
        self.assertEqual(len(templates), 1)
        self.assertIsInstance(templates[0], HelmChartTemplate)
        self.assertEqual(templates[0].name, "template1.yaml")
        self.assertEqual(
            templates[0].data,
            [
                "apiVersion: v1\n",
                "kind: Service\n",
                "metadata:\n",
                "  name: {{ .Release.Name }}-web\n",
            ],
        )
