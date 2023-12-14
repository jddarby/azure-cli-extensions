# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from azext_aosm.inputs.base_input import BaseInput


@dataclass
class VHDFile(BaseInput):
    """
    A utility class for working with VHD files.
    """

    file_path: Optional[Path] = None
    blob_sas_uri: Optional[str] = None

    def get_defaults(self) -> Dict[str, Any]:
        """
        Abstract method to get the default values for configuring the artifact.
        Returns:
            A dictionary containing the default values.
        """
        return self.default_config

    def get_schema(self) -> Dict[str, Any]:
        """
        Abstract method to get the schema for configuring the artifact.
        Returns:
            A dictionary containing the schema.
        """
        vhd_schema = """
        {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "title": "vhdImageSchema",
            "type": "object",
            "properties": {
                "imageName": {
                    "type": "string"
                },
                "azureDeployLocation": {
                    "type": "string"
                },
                "imageDiskSizeGB": {
                    "type": "integer"
                },
                "imageOsState": {
                    "type": "string"
                },
                "imageHyperVGeneration": {
                    "type": "string"
                },
                "apiVersion": {
                    "type": "string"
                }
            }
            "required": [
                "imageName",
                "azureDeployLocation"
            ]
        }
        """

        return json.loads(vhd_schema)
