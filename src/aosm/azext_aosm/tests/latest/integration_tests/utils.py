# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
""" This module provides utility functions for integration tests. """
import os
import unittest
from typing import Dict
from jinja2 import Template

from azure.cli.core.azclierror import CLIInternalError

CHART_NAME = "nginxdemo-0.1.0.tgz"


def mock_in_unit_test(unit_test, target, replacement):
    """Mock a function in a unit test."""

    if not isinstance(unit_test, unittest.TestCase):
        raise CLIInternalError("Patches can be only called from a unit test")

    patcher = unittest.mock.patch(target, replacement)
    patcher.__enter__()
    unit_test.addCleanup(patcher.__exit__, None, None, None)


def update_input_file(input_template_name, output_file_name, params: Dict[str, str]):
    # TODO: change this to have a custom output_file_path. Then we can use a temp directory
    """Update the input file with the given parameters and return the path to the updated file."""
    code_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(
        code_dir, "integration_test_mocks", "mock_input_templates"
    )
    input_template_path = os.path.join(templates_dir, input_template_name)

    with open(input_template_path, "r", encoding="utf-8") as file:
        contents = file.read()

    jinja_template = Template(contents)

    rendered_template = jinja_template.render(**params)

    output_path = os.path.join(templates_dir, output_file_name)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(rendered_template)

    return output_path


def get_path_to_test_chart():
    """Get the path to the chart used in the tests."""
    code_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(code_dir, "integration_test_mocks", "cnf_mocks")
    chart_path = os.path.join(templates_dir, CHART_NAME)
    return chart_path
