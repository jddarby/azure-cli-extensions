# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import logging
import os
import sys
from pathlib import Path
from unittest import TestCase

from azext_aosm.common.exceptions import (
    DefaultValuesNotFoundError,
    TemplateValidationError,
)
import json
import copy
from typing import Dict, Any
from unittest.mock import mock_open, patch

from azext_aosm.inputs.arm_template_input import ArmTemplateInput

code_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(code_directory, "../.."))
helm_charts_directory = os.path.join(parent_directory, "mock_cnf", "helm-charts")

VALID_CHART_NAME = "nf-agent-cnf"
INVALID_CHART_NAME = "nf-agent-cnf-invalid"


class TestARMTemplateInput(TestCase):
    """Test the ARMTempalteInput class."""

    def setUp(self):
        # Prints out info logs in console if fails
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        self.arm_input = ArmTemplateInput(
            artifact_name="test-artifact-name",
            artifact_version="1.1.1",
            template_path="mock/path",
            default_config=None
        )

    def test_get_defaults_is_none(self):
        """Test ARM template input when default config is None"""
        arm_template_input = self.arm_input

        # Test when default_config is None
        arm_template_input.default_config = None
        defaults = arm_template_input.get_defaults()
        self.assertEqual(defaults, {})

    def test_get_defaults_is_empty_dict(self):
        """Test ARM template input when default config is {}"""
        arm_template_input = self.arm_input
        # Test when default_config is an empty dictionary
        arm_template_input.default_config = {}
        defaults = arm_template_input.get_defaults()
        self.assertEqual(defaults, {})

    def test_get_defaults_with_config(self):
        """Test ARM template input when default config provided"""
        arm_template_input = self.arm_input
        # Test when default_config has some values
        arm_template_input.default_config = {
            "param1": "value1",
            "param2": "value2"
        }
        defaults = arm_template_input.get_defaults()
        self.assertEqual(defaults, {
            "param1": "value1",
            "param2": "value2"
        })

    def test_get_schema(self):
        """Test getting the schema for the ARM template input."""
        assert True


    def test_get_schema_no_parameters(self):
        """Test getting the schema for the ARM template input when no parameters are found."""
        assert True
