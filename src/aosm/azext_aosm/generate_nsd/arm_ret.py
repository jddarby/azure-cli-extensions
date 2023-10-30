# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""Handles the creation of a resource element template for an ARM template."""

import json

from typing import Dict, Any
from knack.log import get_logger
from pathlib import Path
from functools import cached_property

from azext_aosm._configuration import ArmArtifactConfig
from azext_aosm.util.constants import CNF, VNF, ARM_RET_SHARED_PARAMETERS, ARM_TO_JSON_PARAM_TYPES
from azext_aosm.util.utils import get_cgs_dict


logger = get_logger(__name__)


class ARMRETGenerator:
    """Represents a single Arm resource element template within an NSD."""

    def __init__(
        self,
        config: ArmArtifactConfig,
        cg_schema_name: str,
        shared_cg_schema_name: str,
    ) -> None:
        self.config = config
        self.cg_schema_name = cg_schema_name
        self.shared_cg_schema_name = shared_cg_schema_name
        print(
            f"Finding the template parameters for {self.config.file_path}:{self.config.version}"
        )
        assert self.config.file_path
        self.arm_template_path = Path(self.config.file_path)
        self.config_mapping_filename = f"{self.config.artifact_name}_config_mapping.json"

    @cached_property
    def arm_template_parameters(self) -> Dict[str, Any]:
        """The parameters from the ARM template."""
        with open(self.arm_template_path, "r", encoding="utf-8") as _file:
            data = json.load(_file)
            if "parameters" in data:
                parameters: Dict[str, Any] = data["parameters"]
            else:
                print(
                    f"No parameters found in Arm template {self.arm_template_path} "
                    "provided. Your NSD will have no parameters for this template in "
                    "the Config Group Schema."
                )
                parameters = {}

        return parameters

    @property
    def config_mappings(self) -> Dict[str, Any]:
        """
        Return the contents of the config mapping file for this RET.

        Output will look something like:
        {
            "parameter1": "{configurationparameters('foo_ConfigGroupSchema').parameter1}",
            "parameter2": "{configurationparameters('foo_ConfigGroupSchema').parameter2}",
            "managedIdentity": "{configurationparameters('shared_ConfigGroupSchema').managedIdentity}",
        }

        Certain special parameters which are added to the NF CGS are assumed to come
        from there if a parameter of the same name is found in the Arm template.
        """
        logger.debug("Create %s", self.config_mapping_filename)

        config_mappings = {
        }

        for arm_template_parameter in self.arm_template_parameters:
            if (
                arm_template_parameter in ARM_RET_SHARED_PARAMETERS and
                self.shared_cg_schema_name != self.cg_schema_name
            ):
                logger.debug("%s parameter found. Using shared schema", arm_template_parameter)
                print(
                    f"\n{arm_template_parameter} parameter found in ARM template "
                    f"{self.arm_template_path}. Assuming this is shared and "
                    f"supplied in the shared CGS {self.shared_cg_schema_name}. If "
                    "this is not the case, you will need to add it to the schema "
                    f"file {self.cg_schema_name} and edit the config mapping file "
                    f"{self.config_mapping_filename} to change the schema name."
                )
                config_mappings[arm_template_parameter] = (
                    f"{{configurationparameters('{self.shared_cg_schema_name}')"
                    f".{arm_template_parameter}}}"
                )
            elif self.shared_cg_schema_name == self.cg_schema_name:
                # Shared CGS schema has an object for each RET, matching the artifact 
                # name. So need to reference the object too. e.g. 
                # "param2": "{configurationparameters('shared_ConfigGroupSchema').foo.param2}",
                config_mappings[arm_template_parameter] = (
                    f"{{configurationparameters('{self.cg_schema_name}').{self.config.artifact_name}.{arm_template_parameter}}}"
                )
            else:
                # Individual CGS for this RET. No sub-objects required. e.g.
                # "param2": "{configurationparameters('foo_ConfigGroupSchema').param2}"
                config_mappings[arm_template_parameter] = (
                    f"{{configurationparameters('{self.cg_schema_name}').{arm_template_parameter}}}"
                )

        return config_mappings

    @property
    def full_config_schema(self) -> Dict[str, Any]:
        """Return the full individual CGS for this Arm template."""
        cgs_snippet = self.config_schema_snippet
        full_cgs = get_cgs_dict(
            self.cg_schema_name,
            cgs_snippet["properties"],
            cgs_snippet["required"],
        )

        return full_cgs

    @property
    def config_schema_snippet(self) -> Dict[str, Any]:
        """Return the CGS snippet for this ARM RET to go in the shared CGS."""
        # Map ARM parameter types to JSON parameter types accepted by AOSM
        arm_ret_parameters = {}
        properties = {}
        required = []
        for key in self.arm_template_parameters.keys():
            arm_type = self.arm_template_parameters[key]["type"]
            json_type = ARM_TO_JSON_PARAM_TYPES.get(arm_type.lower(), arm_type.lower())
            arm_ret_parameters[key] = {"type": json_type}

        properties.update(arm_ret_parameters)
        required.extend(list(arm_ret_parameters.keys()))
        cgs_snippet = {
            "type": "object",
            "properties": properties,
            "required": required
        }

        return cgs_snippet
