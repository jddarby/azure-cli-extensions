# # --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Integration tests for the aosm extension. They test the following commands for the
# cnf definition type:
#   aosm nfd build
#   aosm nfd publish
#   aosm nfd delete
#   aosm nsd build
#   aosm nsd publish
#   aosm nsd delete
#
# --------------------------------------------------------------------------------------------

import os
from typing import Dict
import logging
import sys

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
from jinja2 import Template
from knack.log import get_logger
from .recording_processors import TokenReplacer, SasUriReplacer, BlobStoreUriReplacer

logger = get_logger(__name__)

NFD_INPUT_TEMPLATE_NAME = "cnf_input_template.jsonc"
NFD_INPUT_FILE_NAME = "cnf_input.jsonc"
NSD_INPUT_TEMPLATE_NAME = "cnf_nsd_input_template.jsonc"
NSD_INPUT_FILE_NAME = "nsd_cnf_input.jsonc"
CHART_NAME = "nginxdemo-0.1.0.tgz"


def get_path_to_chart():
    code_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(code_dir, "scenario_test_mocks", "cnf_mocks")
    chart_path = os.path.join(templates_dir, CHART_NAME)
    return chart_path


def update_input_file(input_template_name, output_file_name, params: Dict[str, str]):
    code_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(
        code_dir, "scenario_test_mocks", "mock_input_templates"
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


class CnfNsdTest(ScenarioTest):
    """
    Integration tests for the aosm extension for cnf definition type.

    This test uses Live Scenario Test because it depends on using the `az login` command
    which does not work when playing back from the recording.
    """

    def __init__(self, method_name):
        """
        This constructor initializes the class
        :param method_name: The name of the test method.
        :param recording_processors: The recording processors to use for the test.
        These recording processors modify the recording of a test before it is saved,
        helping to remove sensitive information from the recording.
        """
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        super(CnfNsdTest, self).__init__(
            method_name,
            recording_processors=[
                TokenReplacer(),
                SasUriReplacer(),
                BlobStoreUriReplacer(),
            ],
        )

    @ResourceGroupPreparer(name_prefix="cli_test_cnf_nsd_", location="uksouth")
    def test_cnf_nsd_publish_and_delete(self, resource_group):
        """
        This test creates a cnf nfd and nsd, publishes them, and then deletes them.

        :param resource_group: The name of the resource group to use for the test.
        This is passed in by the ResourceGroupPreparer decorator.
        """

        chart_path = get_path_to_chart()

        nfd_input_file_path = update_input_file(
            NFD_INPUT_TEMPLATE_NAME,
            NFD_INPUT_FILE_NAME,
            params={
                "publisher_resource_group_name": resource_group,
                "path_to_chart": chart_path,
            },
        )

        self.cmd(f'az aosm nfd build -f "{nfd_input_file_path}" --definition-type cnf')

        self.cmd("az aosm nfd publish -b cnf-cli-output --definition-type cnf")
