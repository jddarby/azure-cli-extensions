# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""Contains a class for generating NSDs and associated resources."""
import json
import os
import shutil
import tempfile
from functools import cached_property
from typing import Any, Dict

from jinja2 import Template
from knack.log import get_logger

from azext_aosm._configuration import (
    NFDRETConfiguration,
    NSConfiguration,
    ArmArtifactConfig,
)
from azext_aosm.generate_nsd.nf_ret import NFRETGenerator
from azext_aosm.generate_nsd.arm_ret import ARMRETGenerator
from azext_aosm.util.constants import (
    CONFIG_MAPPINGS_DIR_NAME,
    NF_TEMPLATE_JINJA2_SOURCE_TEMPLATE,
    NSD_ARTIFACT_MANIFEST_BICEP_FILENAME,
    NSD_ARTIFACT_MANIFEST_SOURCE_TEMPLATE_FILENAME,
    NSD_BICEP_FILENAME,
    NSD_DEFINITION_JINJA2_SOURCE_TEMPLATE,
    SCHEMAS_DIR_NAME,
    TEMPLATES_DIR_NAME,
)
from azext_aosm.util.management_clients import ApiClients
from azext_aosm.util.utils import get_cgs_dict

logger = get_logger(__name__)

# Different types are used in Bicep templates and NFDs. The list accepted by NFDs is
# documented in the AOSM meta-schema. This will be published in the future but for now
# can be found in
# https://microsoft.sharepoint.com/:w:/t/NSODevTeam/Ec7ovdKroSRIv5tumQnWIE0BE-B2LykRcll2Qb9JwfVFMQ
NFV_TO_BICEP_PARAM_TYPES: Dict[str, str] = {
    "integer": "int",
    "boolean": "bool",
}


class NSDGenerator:  # pylint: disable=too-few-public-methods
    """
    NSD Generator.

    This takes a config file and a set of NFDV deploy_parameters and outputs:
    - A bicep file for the NSDV
    - Parameters files that are used by the NSDV bicep file, these are the
      schemas and the mapping profiles of those schemas parameters
    - A bicep file for the Artifact manifest
    - A bicep and JSON file defining the Network Function that will
      be deployed by the NSDV
    """

    def __init__(self, api_clients: ApiClients, config: NSConfiguration):
        self.config = config
        self.nsd_bicep_template_name = NSD_DEFINITION_JINJA2_SOURCE_TEMPLATE
        self.nsd_bicep_output_name = NSD_BICEP_FILENAME

        self.nf_ret_generators = []
        self.arm_ret_generators = []

        for nf_config in self.config.network_functions:
            assert isinstance(nf_config, NFDRETConfiguration)
            self.nf_ret_generators.append(
                NFRETGenerator(api_clients, nf_config, self.config.nf_cg_schema_name)
            )

        for index, arm_ret_config in enumerate(self.config.arm_templates):
            # This should end up with ARM RETs in the order specified in the config.
            assert isinstance(arm_ret_config, ArmArtifactConfig)
            self.arm_ret_generators.append(
                ARMRETGenerator(
                    config=arm_ret_config,
                    cg_schema_name=self.config.arm_cg_schema_names[index],
                    shared_cg_schema_name=self.config.nf_cg_schema_name,
                )
            )

    def generate_nsd(self) -> None:
        """Generate a NSD templates which includes an Artifact Manifest, NFDV and NF templates."""
        logger.info("Generate NSD bicep templates")

        # Create temporary folder.
        with tempfile.TemporaryDirectory() as tmpdirname:
            self._write_config_group_schemas_json(tmpdirname)
            self._write_config_mapping_files(tmpdirname)
            self._write_nsd_manifest(tmpdirname)
            self._write_nf_bicep_files(tmpdirname)
            self._write_nsd_bicep(tmpdirname)

            self._copy_to_output_folder(tmpdirname)
            print(
                "Generated NSD bicep templates created in"
                f" {self.config.output_directory_for_build}"
            )
            print(
                "Please review these templates. When you are happy with them run "
                "`az aosm nsd publish` with the same arguments."
            )

    @cached_property
    def _nfs_config_group_schema_dict(self) -> Dict[str, Any]:
        """
        :return: The Config Group Schema as a dictionary.

        See src/aosm/azext_aosm/tests/latest/nsd_output/*/schemas for examples of the
        output from this function.
        """
        managed_identity_description_string = (
            "The managed identity to use to deploy NFs within this SNS.  This should "
            "be of the form '/subscriptions/{subscriptionId}/resourceGroups/"
            "{resourceGroupName}/providers/Microsoft.ManagedIdentity/"
            "userAssignedIdentities/{identityName}.  "
            "If you wish to use a system assigned identity, set this to a blank string."
        )

        properties = {
            nf.config.name: nf.config_schema_snippet for nf in self.nf_ret_generators
        }

        properties.update(
            {
                "managedIdentity": {
                    "type": "string",
                    "description": managed_identity_description_string,
                }
            }
        )

        required = [nf.config.name for nf in self.nf_ret_generators]
        required.append("managedIdentity")

        if not self.config.cgs_split:
            # ARM RETs should go in the NF CGS schema (which becomes the shared schema)
            logger.debug("Creating shared CGS for all.")
            for arm_ret in self.arm_ret_generators:
                properties[arm_ret.config.artifact_name] = arm_ret.config_schema_snippet
                required.append(arm_ret.config.artifact_name)

        cgs_dict = get_cgs_dict(self.config.nf_cg_schema_name, properties, required)

        return cgs_dict

    def _write_config_group_schemas_json(self, output_directory) -> None:
        """Create a file containing the json schema for the CGS."""
        temp_schemas_folder_path = os.path.join(output_directory, SCHEMAS_DIR_NAME)
        os.mkdir(temp_schemas_folder_path)

        if self.config.cgs_split:
            # Separate CGS schema for each ARM RET and one for all NFs
            for arm_ret in self.arm_ret_generators:
                logger.debug("Create %s.json", arm_ret.cg_schema_name)

                schema_path = os.path.join(
                    temp_schemas_folder_path, f"{arm_ret.cg_schema_name}.json"
                )

                with open(schema_path, "w", encoding="utf-8") as _file:
                    _file.write(json.dumps(arm_ret.full_config_schema, indent=4))

                logger.debug("%s created", schema_path)

        # CGS schema for all NFs (and shared ARM RETs if not split)
        logger.debug("Create %s.json", self.config.nf_cg_schema_name)

        schema_path = os.path.join(
            temp_schemas_folder_path, f"{self.config.nf_cg_schema_name}.json"
        )

        with open(schema_path, "w", encoding="utf-8") as _file:
            _file.write(json.dumps(self._nfs_config_group_schema_dict, indent=4))

        logger.debug("%s created", schema_path)

    def _write_config_mapping_files(self, output_directory) -> None:
        """Write out a config mapping file for each NF."""
        temp_mappings_folder_path = os.path.join(
            output_directory, CONFIG_MAPPINGS_DIR_NAME
        )

        os.mkdir(temp_mappings_folder_path)

        for nf in self.nf_ret_generators:
            config_mappings_path = os.path.join(
                temp_mappings_folder_path, nf.config_mapping_filename
            )

            with open(config_mappings_path, "w", encoding="utf-8") as _file:
                _file.write(json.dumps(nf.config_mappings, indent=4))

            logger.debug("%s created", config_mappings_path)

        for arm_ret in self.arm_ret_generators:
            config_mappings_path = os.path.join(
                temp_mappings_folder_path, arm_ret.config_mapping_filename
            )

            with open(config_mappings_path, "w", encoding="utf-8") as _file:
                _file.write(json.dumps(arm_ret.config_mappings, indent=4))

            logger.debug("%s created", config_mappings_path)

    def _write_nf_bicep_files(self, output_directory) -> None:
        """
        Write bicep files for deploying NFs.

        In the publish step these bicep files will be uploaded to the publisher storage
        account as artifacts.
        """
        for nf in self.nf_ret_generators:
            substitutions = {"location": self.config.location}
            substitutions.update(nf.nf_bicep_substitutions)

            self._generate_bicep(
                NF_TEMPLATE_JINJA2_SOURCE_TEMPLATE,
                os.path.join(output_directory, nf.config.nf_bicep_filename),
                substitutions,
            )

    def _write_nsd_bicep(self, output_directory) -> None:
        """
        Write out the NSD bicep file.

        This method creates the jinja2 parameters used to render the NSD bicep template
        and then calls the _generate_bicep method to render the template.

        It is important that the parameters referencing artifacts match those artifacts
        that are put into the artifact manifest.  The order in the manifest doesn't
        matter, but the names and versions do. The parameters put into the artifact
        manifest are defined at deploy time, in
        deploy_with_arm.construct_manifest_parameters.
        """
        nf_config = [
            {
                "resource_element_name": nf.config.resource_element_name,
                "artifact_name": nf.config.arm_template.artifact_name,
                "config_mapping_file": nf.config_mapping_filename,
            }
            for nf in self.nf_ret_generators
        ]
        schema_names = [self.config.nf_cg_schema_name]
        if self.config.cgs_split:
            schema_names.extend([arm.cg_schema_name for arm in self.arm_ret_generators])
        arm_templates_config = [
            {
                "ret_name": arm.config.artifact_name,
                "config_mapping_file": arm.config_mapping_filename,
            }
            for arm in self.arm_ret_generators
        ]

        # We want all armTemplateVersions to be the same as the NSD Version.  That
        # means that if we create a new NSDV then the existing artifacts won't be
        # overwritten. An ARM template update should require a new NSDV.
        #
        # Values must also match those given to the artifact manifest
        # (in deploy_with_arm.construct_manifest_parameters)
        params = {
            "nfvi_site_name": self.config.nfvi_site_name,
            "nf_config": nf_config,
            "armTemplateVersion": self.config.nsd_version,
            "cg_schema_names": schema_names,
            "nsdv_description": self.config.nsdv_description,
            "arm_templates_config": arm_templates_config,
        }

        self._generate_bicep(
            self.nsd_bicep_template_name,
            os.path.join(output_directory, self.nsd_bicep_output_name),
            params,
        )

    def _write_nsd_manifest(self, output_directory) -> None:
        """Write out the NSD manifest bicep file."""
        logger.debug("Create NSD manifest")

        self._generate_bicep(
            NSD_ARTIFACT_MANIFEST_SOURCE_TEMPLATE_FILENAME,
            os.path.join(output_directory, NSD_ARTIFACT_MANIFEST_BICEP_FILENAME),
            {},
        )

    @staticmethod
    def _generate_bicep(
        template_name: str, output_file_name: str, params: Dict[Any, Any]
    ) -> None:
        """
        Render the bicep templates with the correct parameters and copy them into the build output folder.

        :param template_name: The name of the template to render
        :param output_file_name: The name of the output file
        :param params: The jinja2 parameters to render the template with
        """

        code_dir = os.path.dirname(__file__)

        bicep_template_path = os.path.join(code_dir, TEMPLATES_DIR_NAME, template_name)

        with open(bicep_template_path, "r", encoding="utf-8") as file:
            bicep_contents = file.read()

        bicep_template = Template(bicep_contents)

        # Render all the relevant parameters in the bicep template
        rendered_template = bicep_template.render(**params)

        with open(output_file_name, "w", encoding="utf-8") as file:
            file.write(rendered_template)

    def _copy_to_output_folder(self, temp_dir) -> None:
        """Copy the bicep templates, config mappings and schema into the build output folder."""

        logger.info("Create NSD bicep %s", self.config.output_directory_for_build)
        os.mkdir(self.config.output_directory_for_build)

        shutil.copytree(
            temp_dir,
            self.config.output_directory_for_build,
            dirs_exist_ok=True,
        )

        logger.info("Copied files to %s", self.config.output_directory_for_build)
