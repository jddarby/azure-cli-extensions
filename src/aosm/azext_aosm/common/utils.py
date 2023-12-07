# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def convert_bicep_to_arm(bicep_template_path: Path) -> dict:
    """
    Convert a bicep template into an ARM template.

    :param bicep_template_path: The path to the bicep template to be converted
    :return: Output dictionary representation of the ARM template JSON.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        bicep_filename = bicep_template_path.name
        arm_template_name = bicep_filename.replace(".bicep", ".json")
        arm_path = Path(tmpdir) / arm_template_name

        try:
            subprocess.run(  # noqa
                [
                    str(shutil.which("az")),
                    "bicep",
                    "build",
                    "--file",
                    bicep_template_path,
                    "--outfile",
                    str(arm_path),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as err:
            raise RuntimeError("Bicep to ARM template compilation failed")

        arm_json = json.loads(arm_path.read_text())

    return arm_json


def create_bicep_from_template():
    # Take j2 template, take params, return bicep file
    return NotImplementedError
