# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
from dataclasses import dataclass
from distutils.dir_util import copy_tree
import json
import shutil
import subprocess
from filecmp import dircmp
from pathlib import Path
from unittest.mock import patch
from tempfile import TemporaryDirectory

import jsonschema

from azext_aosm.custom import generate_design_config, build_design

mock_nsd_folder = ((Path(__file__).parent) / "mock_nsd").resolve()
output_folder = ((Path(__file__).parent) / "nsd_output").resolve()


CGV_DATA = {
    "ubuntu-vm-nfdg": {
        "deploymentParameters": {
            "location": "eastus",
            "subnetName": "subnet",
            "virtualNetworkId": "bar",
            "sshPublicKeyAdmin": "foo",
        },
        "ubuntu_vm_nfdg_nfd_version": "1.0.0",
    },
    "managedIdentity": "blah",
}


MULTIPLE_INSTANCES_CGV_DATA = {
    "ubuntu-vm-nfdg": {
        "deploymentParameters": [
            {
                "location": "eastus",
                "subnetName": "subnet",
                "virtualNetworkId": "bar",
                "sshPublicKeyAdmin": "foo",
            },
            {
                "location": "eastus",
                "subnetName": "subnet2",
                "virtualNetworkId": "bar2",
                "sshPublicKeyAdmin": "foo2",
            },
        ],
        "ubuntu_vm_nfdg_nfd_version": "1.0.0",
    },
    "managedIdentity": "blah",
}


MULTIPLE_NFs_CGV_DATA = {
    "managedIdentity": "managed_identity",
    "nginx-nfdg": {
        "customLocationId": "custom_location",
        "nginx_nfdg_nfd_version": "1.0.0",
        "deploymentParameters": {"service_port": 5222, "serviceAccount_create": False},
    },
    "ubuntu-nfdg": {
        "ubuntu_nfdg_nfd_version": "1.0.0",
        "deploymentParameters": {
            "location": "eastus",
            "subnetName": "ubuntu-vm-subnet",
            "ubuntuVmName": "ubuntu-vm",
            "virtualNetworkId": "ubuntu-vm-vnet",
            "sshPublicKeyAdmin": "public_key",
        },
    },
}


ubuntu_deploy_parameters = {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "title": "DeployParametersSchema",
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "subnetName": {"type": "string"},
        "virtualNetworkId": {"type": "string"},
        "sshPublicKeyAdmin": {"type": "string"},
    },
}

nginx_deploy_parameters = {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "title": "DeployParametersSchema",
    "type": "object",
    "properties": {
        "serviceAccount_create": {"type": "boolean"},
        "service_port": {"type": "integer"},
    },
    "required": ["serviceAccount_create", "service_port"],
}


# We don't want to get details from a real NFD (calling out to Azure) in a UT.
# Therefore we pass in a fake client to supply the deployment parameters from the "NFD".
@dataclass
class NFDV:
    deploy_parameters: str


class NFDVs:
    def get(self, network_function_definition_group_name, **_):
        if "nginx" in network_function_definition_group_name:
            return NFDV(json.dumps(nginx_deploy_parameters))
        else:
            return NFDV(json.dumps(ubuntu_deploy_parameters))


class AOSMClient:
    def __init__(self) -> None:
        self.network_function_definition_versions = NFDVs()


mock_client = AOSMClient()


class FakeCmd:
    def __init__(self) -> None:
        self.cli_ctx = None


mock_cmd = FakeCmd()


def validate_schema_against_metaschema(schema_data):
    """
    Validate that the schema produced by the CLI matches the AOSM metaschema.
    """

    # There is a bug in the jsonschema module that means that it hits an error in with
    # the "$id" bit of the metaschema.  Here we use a modified version of the metaschema
    # with that small section removed.
    metaschema_file_path = (
        (Path(__file__).parent) / "metaschema_modified.json"
    ).resolve()
    with open(metaschema_file_path, "r", encoding="utf8") as f:
        metaschema = json.load(f)

    jsonschema.validate(instance=schema_data, schema=metaschema)


def validate_json_against_schema(json_data, schema_file):
    """
    Validate some test data against the schema produced by the CLI.
    """
    with open(schema_file, "r", encoding="utf8") as f:
        schema = json.load(f)

    validate_schema_against_metaschema(schema)

    jsonschema.validate(instance=json_data, schema=schema)


def build_bicep(bicep_template_path):
    bicep_output = subprocess.run(  # noqa
        [
            str(shutil.which("az")),
            "bicep",
            "build",
            "--file",
            bicep_template_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if bicep_output.returncode != 0:
        print(f"Invalid bicep: {bicep_template_path}")
        print(str(bicep_output.stderr).replace("\\n", "\n").replace("\\t", "\t"))
        raise RuntimeError("Invalid Bicep")


def compare_to_expected_output(expected_folder_name: str):
    """
    Compares nsd-bicep-templates to the supplied folder name

    :param expected_folder_name: The name of the folder within nsd_output to compare
    with.
    """
    # Check files and folders within the top level directory are the same.
    expected_output_path = output_folder / expected_folder_name
    comparison = dircmp("nsd-bicep-templates", expected_output_path)

    try:
        assert len(comparison.diff_files) == 0
        assert len(comparison.left_only) == 0
        assert len(comparison.right_only) == 0

        # Check the files and folders within each of the subdirectories are the same.
        for subdir in comparison.subdirs.values():
            assert len(subdir.diff_files) == 0
            assert len(subdir.left_only) == 0
            assert len(subdir.right_only) == 0
    except:
        copy_tree("nsd-bicep-templates", str(expected_output_path))
        print(
            f"Output has changed in {expected_output_path}, use git diff to check if "
            f"you are happy with those changes."
        )
        raise


class TestNSDGenerator:
    def test_generate_config(self):
        """
        Test generating a config file for a VNF.
        """
        starting_directory = os.getcwd()
        with TemporaryDirectory() as test_dir:
            os.chdir(test_dir)

            try:
                generate_design_config()
                assert os.path.exists("input.json")
            finally:
                os.chdir(starting_directory)

    @patch("azext_aosm.custom.cf_resources")
    def test_build(self, cf_resources):
        """
        Test building the NSD bicep templates.
        """
        starting_directory = os.getcwd()
        with TemporaryDirectory() as test_dir:
            os.chdir(test_dir)

            try:
                build_design(
                    mock_cmd,
                    client=mock_client,
                    config_file=str(mock_nsd_folder / "input.json"),
                )

                assert os.path.exists("nsd-bicep-templates")
                validate_json_against_schema(
                    CGV_DATA,
                    "nsd-bicep-templates/schemas/ubuntu_ConfigGroupSchema.json",
                )

                compare_to_expected_output("test_build")
            finally:
                os.chdir(starting_directory)

    @patch("azext_aosm.custom.cf_resources")
    def test_build_multiple_instances(self, cf_resources):
        """
        Test building the NSD bicep templates with multiple NFs allowed.
        """
        starting_directory = os.getcwd()
        with TemporaryDirectory() as test_dir:
            os.chdir(test_dir)

            try:
                build_design(
                    mock_cmd,
                    client=mock_client,
                    config_file=str(mock_nsd_folder / "input_multiple_instances.json"),
                )

                assert os.path.exists("nsd-bicep-templates")
                validate_json_against_schema(
                    MULTIPLE_INSTANCES_CGV_DATA,
                    "nsd-bicep-templates/schemas/ubuntu_ConfigGroupSchema.json",
                )

                compare_to_expected_output("test_build_multiple_instances")
            finally:
                os.chdir(starting_directory)

    @patch("azext_aosm.custom.cf_resources")
    def test_build_multiple_nfs(self, cf_resources):
        """
        Test building the NSD bicep templates with multiple NFs allowed.
        """
        starting_directory = os.getcwd()
        with TemporaryDirectory() as test_dir:
            os.chdir(test_dir)

            try:
                build_design(
                    mock_cmd,
                    client=mock_client,
                    config_file=str(mock_nsd_folder / "input_multi_nf_nsd.json"),
                )

                assert os.path.exists("nsd-bicep-templates")
                validate_json_against_schema(
                    MULTIPLE_NFs_CGV_DATA,
                    "nsd-bicep-templates/schemas/multinf_ConfigGroupSchema.json",
                )

                # The bicep checks take a while, so we only do them here and not on the
                # other tests.
                build_bicep("nsd-bicep-templates/nginx-nfdg_nf.bicep")
                build_bicep("nsd-bicep-templates/ubuntu-nfdg_nf.bicep")
                build_bicep("nsd-bicep-templates/nsd_definition.bicep")
                build_bicep("nsd-bicep-templates/artifact_manifest.bicep")

                compare_to_expected_output("test_build_multiple_nfs")
            finally:
                os.chdir(starting_directory)
