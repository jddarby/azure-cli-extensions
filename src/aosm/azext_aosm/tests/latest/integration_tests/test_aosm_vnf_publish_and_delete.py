# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# This is an integration tests for the aosm extension. It tests the following commands for the
# vnf definition type:
#   aosm nfd build
#   aosm nfd publish
#   aosm nfd delete
#   aosm nsd build
#   aosm nsd publish
#   aosm nsd delete
# --------------------------------------------------------------------------------------------

import os
import logging
import sys
from typing import Dict

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
from jinja2 import Template
from knack.log import get_logger
from azext_aosm.tests.latest.integration_tests.recording_processors import (
    TokenReplacer,
    SasUriReplacer,
    BlobStoreUriReplacer,
)

logger = get_logger(__name__)

NFD_INPUT_TEMPLATE_NAME = "vnf_input_template.jsonc"
NFD_INPUT_FILE_NAME = "vnf_input.jsonc"
NSD_INPUT_TEMPLATE_NAME = "vnf_nsd_input_template.jsonc"
NSD_INPUT_FILE_NAME = "nsd_input.jsonc"
ARM_TEMPLATE_NAME = "ubuntu_template.json"
VHD_NAME = "ubuntu.vhd"


def get_path_to_vnf_mocks():
    code_dir = os.path.dirname(__file__)
    vnf_mocks_dir = os.path.join(code_dir, "integration_test_mocks", "vnf_mocks")

    return vnf_mocks_dir


def update_input_file(input_template_name, output_file_name, params: Dict[str, str]):
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


class VnfNsdTest(ScenarioTest):
    """This class contains the integration tests for the aosm extension for vnf definition type."""

    def __init__(self, method_name):
        """
        This constructor initializes the class
        :param method_name: The name of the test method.
        :param recording_processors: The recording processors to use for the test.
        These recording processors modify the recording of a test before it is saved,
        helping to remove sensitive information from the recording.
        """
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        super(VnfNsdTest, self).__init__(
            method_name,
            recording_processors=[
                TokenReplacer(),
                SasUriReplacer(),
                BlobStoreUriReplacer(),
            ],
        )

    @ResourceGroupPreparer(name_prefix="cli_test_vnf_nsd_", location="uksouth")
    def test_vnf_nsd_publish_and_delete(self, resource_group):
        """
        This test creates a vnf nfd and nsd, publishes them, and then deletes them.

        :param resource_group: The name of the resource group to use for the test.
        This is passed in by the ResourceGroupPreparer decorator.
        """

        vnf_mocks_dir = get_path_to_vnf_mocks()

        arm_template_path = os.path.join(vnf_mocks_dir, ARM_TEMPLATE_NAME)
        vhd_path = os.path.join(vnf_mocks_dir, VHD_NAME)

        nfd_input_file_path = update_input_file(
            NFD_INPUT_TEMPLATE_NAME,
            NFD_INPUT_FILE_NAME,
            params={
                "publisher_resource_group_name": resource_group,
                "arm_template_path": arm_template_path,
                "vhd_path": vhd_path,
            },
        )

        self.cmd(
            f'az aosm nfd build --config-file "{nfd_input_file_path}" --definition-type vnf'
        )

        self.cmd(
            "az aosm nfd publish --build-output-folder vnf-cli-output --definition-type vnf"
        )

        nsd_input_file_path = update_input_file(
            NSD_INPUT_TEMPLATE_NAME,
            NSD_INPUT_FILE_NAME,
            params={"publisher_resource_group_name": resource_group},
        )

        self.cmd(f'az aosm nsd build -f "{nsd_input_file_path}"')

        self.cmd("az aosm nsd publish --build-output-folder nsd-cli-output")
