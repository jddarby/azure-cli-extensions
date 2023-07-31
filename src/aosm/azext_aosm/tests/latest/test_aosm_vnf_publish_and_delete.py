from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
from knack.log import get_logger
import os
from jinja2 import Template
from .recording_processors import AcrTokenReplacer, SasUriReplacer


logger = get_logger(__name__)

NFD_INPUT_TEMPLATE_NAME = "vnf_input_template.json"
NFD_INPUT_FILE_NAME = "vnf_input.json"
NSD_INPUT_TEMPLATE_NAME = "vnf_nsd_input_template.json"
NSD_INPUT_FILE_NAME = "nsd_input.json"
ARM_TEMPLATE_RELATIVE_PATH = "scenario_test_mocks/vnf_mocks/ubuntu_template.json"


def update_resource_group_in_input_file(
    input_template_name: str, output_file_name: str, resource_group: str
) -> str:
    code_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(
        code_dir, "scenario_test_mocks", "mock_input_templates"
    )
    input_template_path = os.path.join(templates_dir, input_template_name)

    with open(input_template_path, "r", encoding="utf-8") as file:
        contents = file.read()

    jinja_template = Template(contents)

    rendered_template = jinja_template.render(
        publisher_resource_group_name=resource_group
    )

    output_path = os.path.join(templates_dir, output_file_name)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(rendered_template)

    return output_path


class VnfNsdTest(ScenarioTest):
    def __init__(self, method_name):
        super(VnfNsdTest, self).__init__(
            method_name,
            recording_processors=[AcrTokenReplacer(), SasUriReplacer()]
        )

    @ResourceGroupPreparer(name_prefix="cli_test_vnf_nsd_", location="northeurope")
    def test_vnf_nsd_publish_and_delete(self, resource_group):
        nfd_input_file_path = update_resource_group_in_input_file(
            NFD_INPUT_TEMPLATE_NAME, NFD_INPUT_FILE_NAME, resource_group
        )

        self.cmd(
            f'az aosm nfd build -f "{nfd_input_file_path}" --definition-type vnf --force'
        )

        # There is currently a bug in the CLI testing framework that causes the command 
        # to fail on timeout. This is a workaround to retry the command if it fails.
        retry_attempts = 0
        while retry_attempts < 2:
            try:
                self.cmd(
                    f'az aosm nfd publish -f "{nfd_input_file_path}" --definition-type vnf'
                )
                break
            except Exception:
                retry_attempts += 1

        nsd_input_file_path = update_resource_group_in_input_file(
            NSD_INPUT_TEMPLATE_NAME, NSD_INPUT_FILE_NAME, resource_group
        )

        self.cmd(f'az aosm nsd build -f "{nsd_input_file_path}" --force')

        self.cmd(f'az aosm nsd publish -f "{nsd_input_file_path}"')

        self.cmd(f'az aosm nsd delete -f "{nsd_input_file_path}" --clean --force')
        self.cmd(
            f'az aosm nfd delete --definition-type vnf -f "{nfd_input_file_path}" --clean --force'
        )
