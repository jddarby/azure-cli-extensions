# --------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT
# License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------
"""Contains a class for generating VNF NFDs and associated resources."""
from knack.log import get_logger
import json
import logging
import os
import shutil
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, Optional

from azext_aosm.generate_nfd.nfd_generator_base import NFDGenerator

from azext_aosm._configuration import NSConfiguration
from azext_aosm.util.constants import (
    NSD_DEFINITION_BICEP_SOURCE_TEMPLATE,
    NSD_DEFINITION_BICEP_FILE,
    NF_TEMPLATE_BICEP_FILE,
    NF_DEFINITION_BICEP_FILE,
    NSD_ARTIFACT_MANIFEST_BICEP_FILE,
)

from jinja2 import Template


logger = get_logger(__name__)


class BicepNsdGenerator:
    """
    VNF NFD Generator.

    This takes a source ARM template and a config file, and outputs:
    - A bicep file for the NFDV
    - Parameters files that are used by the NFDV bicep file, these are the
      deployParameters and the mapping profiles of those deploy parameters
    - A bicep file for the Artifact manifests
    """

    def __init__(self, config: NSConfiguration):
        self.config = config
        self.bicep_template_name = NSD_DEFINITION_BICEP_SOURCE_TEMPLATE
        self.nf_template_name = NF_TEMPLATE_BICEP_FILE

        # self.arm_template_path = self.config.arm_template.file_path
        self.folder_name = self.config.build_output_folder_name

        self._bicep_path = os.path.join(self.folder_name, self.bicep_template_name)

    def generate_nsd(self, deploy_parameters) -> None:
        """Generate a NSD which comprises an group, an Artifact Manifest and a NFDV."""
        self.deploy_parameters = deploy_parameters
        if self.bicep_path:
            print(f"Using the existing NSD bicep template {self.bicep_path}.")
            print(
                f"To generate a new NSD, delete the folder {os.path.dirname(self.bicep_path)} and re-run this command."
            )
        else:
            self.write()

    def write(self) -> None:
        """Create a bicep template for an NFD from the ARM template for the VNF."""
        logger.info(f"Generate NSD bicep template")
        # print(f"Generate NFD bicep template for {self.arm_template_path}")

        self._create_nsd_folder()
        self.create_parameter_files()
        self.write_nsd_manifest()
        self.write_nf_bicep()
        self.write_nsd_bicep()
        print(f"Generated NFD bicep template created in {self.folder_name}")

    @property
    def bicep_path(self) -> Optional[str]:
        """Returns the path to the bicep file for the NFD if it has been created."""
        if os.path.exists(self._bicep_path):
            return self._bicep_path

        return None

    @property
    def manifest_path(self) -> Optional[str]:
        """Returns the path to the bicep file for the NFD if it has been created."""
        if os.path.exists(self._manifest_path):
            return self._manifest_path

        return None

    def _create_nsd_folder(self) -> None:
        """
        Create the folder for the NSD bicep files.

        :raises RuntimeError: If the user aborts.
        """
        if os.path.exists(self.folder_name):
            carry_on = input(
                f"The folder {self.folder_name} already exists - delete it and continue? (y/n)"
            )
            if carry_on != "y":
                raise RuntimeError("User aborted!")

            shutil.rmtree(self.folder_name)

        logger.info("Create NFD bicep %s", self.folder_name)
        os.mkdir(self.folder_name)

    @cached_property
    def vm_parameters(self) -> Dict[str, Any]:
        """The parameters from the VM ARM template."""
        with open(self.arm_template_path, "r") as _file:
            parameters: Dict[str, Any] = json.load(_file)["parameters"]

        return parameters

    def create_parameter_files(self) -> None:
        """Create the Deployment and Template json parameter files."""
        schemas_folder_path = os.path.join(self.folder_name, "schemas")
        os.mkdir(schemas_folder_path)
        self.write_deployment_parameters(schemas_folder_path)

        mappings_folder_path = os.path.join(self.folder_name, "configMappings")
        os.mkdir(mappings_folder_path)
        self.write_template_parameters(mappings_folder_path)

    def write_deployment_parameters(self, folder_path: str) -> None:
        """
        Write out the NFD deploymentParameters.json file.

        :param folder_path: The folder to put this file in.
        """
        logger.debug("Create deploymentParameters.json")

        deployment_parameters_path = os.path.join(
            folder_path, f"{self.config.cgSchemaName}.json"
        )

        # # Heading for the deployParameters schema
        # deploy_parameters_full: Dict[str, Any] = {
        #     "$schema": "https://json-schema.org/draft-07/schema#",
        #     "title": "DeployParametersSchema",
        #     "type": "object",
        #     "properties": nfd_parameters,
        # }

        with open(deployment_parameters_path, "w") as _file:
            _file.write(self.deploy_parameters)

        logger.debug(f"{deployment_parameters_path} created")

    def write_template_parameters(self, folder_path: str) -> None:
        """
        Write out the NFD templateParameters.json file.

        :param folder_path: The folder to put this file in.
        """

        deploy_properties = json.loads(self.deploy_parameters)
        deploy_properties = deploy_properties["properties"]

        logger.debug("Create templateParameters.json")
        template_parameters = {
            key: f"{{{self.config.cgSchemaName}.{key}}}" for key in deploy_properties
        }

        template_parameters_path = os.path.join(folder_path, "configMappings.json")

        with open(template_parameters_path, "w") as _file:
            _file.write(json.dumps(template_parameters, indent=4))

        logger.debug(f"{template_parameters_path} created")

    def write_nf_bicep(self) -> None:
        bicep_params = ""

        bicep_deploymentValues = ""

        deploy_properties = json.loads(self.deploy_parameters)
        deploy_properties = deploy_properties["properties"]

        for key, value in deploy_properties.items():
            bicep_params += f"param {key} {value['type']}\n"
            bicep_deploymentValues += f"  {key}: {key}\n"

        self.generate_bicep(
            self.nf_template_name,
            NF_DEFINITION_BICEP_FILE,
            {"bicep_params": bicep_params, "deploymentValues": bicep_deploymentValues},
        )

    def write_nsd_bicep(self) -> None:
        params = {
            "nfviSiteName": self.config.nfviSiteName,
            "NfArmTemplateName": self.config.NfArmTemplateName,
            "NfArmTemplateVersion": self.config.NfArmTemplateVersion,
            "cgSchemaName": self.config.cgSchemaName,
            "nsdDescription": self.config.nsdDescription,
            "nfviSiteType": self.config.nfviSiteType,
            "nfviSiteType": self.config.nfviSiteType,
            "ResourceElementName": self.config.resource_element_name,
        }

        self.generate_bicep(self.bicep_template_name, NSD_DEFINITION_BICEP_FILE, params)

    def write_nsd_manifest(self) -> None:
        """Write out the NSD manifest file."""
        logger.debug("Create NSD manifest")

        self.generate_bicep(
            "artifact_manifest_template.bicep", NSD_ARTIFACT_MANIFEST_BICEP_FILE, {}
        )

    def generate_bicep(self, template_name, created_bicep_file_name, params) -> None:
        """Render the bicep templates with the correct parameters and copy them into the build output folder."""

        code_dir = os.path.dirname(__file__)

        bicep_template_path = os.path.join(code_dir, "templates", template_name)

        with open(bicep_template_path, "r") as file:
            bicep_contents = file.read()

        bicep_template = Template(bicep_contents)

        # Render all the relevant parameters in the bicep template
        rendered_template = bicep_template.render(**params)

        bicep_file_build_path = os.path.join(self.folder_name, created_bicep_file_name)

        with open(bicep_file_build_path, "w") as file:
            file.write(rendered_template)
