from unittest import TestCase
from azext_aosm.tests.latest.tests_utils import update_input_file, get_tests_path
from azext_aosm.cli_handlers.onboarding_cnf_handler import (
    OnboardingCNFCLIHandler,
)
from pathlib import Path

CNF_NF_AGENT_INPUT_TEMPLATE_NAME = "input-nf-agent-cnf-template.jsonc"
CNF_NF_AGENT_INPUT_FILE_NAME = "test_helm_chart_processor_input-nf-agent-cnf.jsonc"


class TestHelmChartProcessor(TestCase):
    def setUp(self):
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
        self.helm_chart_processor = handler.processors[0]

    def test_find_chart_images(self):
        # We want to test a specific private method so disable the pylint warning
        # pylint: disable=protected-access
        collected_images = self.helm_chart_processor._find_chart_images()

        # Assert the expected images are returned
        expected_images = {("pez-nfagent", "879624")}
        self.assertEqual(collected_images, expected_images)
