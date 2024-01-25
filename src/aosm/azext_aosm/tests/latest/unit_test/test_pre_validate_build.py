# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from unittest import TestCase
from pathlib import Path

from azure.cli.core.azclierror import ValidationError

from azext_aosm.cli_handlers.onboarding_cnf_handler import (
    OnboardingCNFCLIHandler,
)
from azext_aosm.tests.latest.tests_utils import update_input_file, get_tests_path

CNF_NF_AGENT_INPUT_TEMPLATE_NAME = "input-nf-agent-cnf-template.jsonc"
CNF_NF_AGENT_INPUT_FILE_NAME = "test_pre_validate_build_input-nf-agent-cnf.jsonc"
CNF_NF_AGENT_INVALID_INPUT_TEMPLATE_NAME = (
    "input-nf-agent-cnf-template-invalid-chart.jsonc"
)
CNF_NF_AGENT_INVALID_INPUT_FILE_NAME = (
    "test_pre_validate_build_input-nf-agent-cnf-invalid.jsonc"
)


class TestOnboardingCNFCLIHandler(TestCase):
    """Test the OnboardingCNFCLIHandler class."""

    def test_validate_helm_template_valid_chart(self):
        """Test validating a valid Helm chart using helm template."""
        config_file = update_input_file(
            CNF_NF_AGENT_INPUT_TEMPLATE_NAME,
            CNF_NF_AGENT_INPUT_FILE_NAME,
            params={
                "tests_directory": get_tests_path(),
            },
        )

        handler = OnboardingCNFCLIHandler(Path(config_file))
        # We want to test a specific private method so disable the pylint warning
        # pylint: disable=protected-access
        handler._validate_helm_template()

    def test_validate_helm_template_invalid_chart(self):
        """Test validating an invalid Helm chart using helm template."""
        config_file = update_input_file(
            CNF_NF_AGENT_INVALID_INPUT_TEMPLATE_NAME,
            CNF_NF_AGENT_INVALID_INPUT_FILE_NAME,
            params={
                "tests_directory": get_tests_path(),
            },
        )

        handler = OnboardingCNFCLIHandler(Path(config_file))

        with self.assertRaises(ValidationError):
            # We want to test a specific private method so disable the pylint warning
            # pylint: disable=protected-access
            handler._validate_helm_template()
