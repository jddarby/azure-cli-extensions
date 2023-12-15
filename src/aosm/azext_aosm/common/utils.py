# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import tarfile
from pathlib import Path
from typing import Any, Dict

from azext_aosm.common.exceptions import InvalidFileTypeError


def convert_bicep_to_arm():
    # Need this in bicep element and artifacts
    return NotImplementedError


def create_bicep_from_template():
    # Take j2 template, take params, return bicep file
    return NotImplementedError


def extract_tarfile(file_path: Path, target_dir: Path) -> Path:
    """
    Extracts the tar file to a temporary directory.
    Args:
        file_path: Path to the tar file.
    Returns:
        Path to the temporary directory.
    """
    file_extension = file_path.suffix

    if file_extension in (".gz", ".tgz"):
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=target_dir)
    elif file_extension == ".tar":
        with tarfile.open(file_path, "r:") as tar:
            tar.extractall(path=target_dir)
    else:
        raise InvalidFileTypeError(
            f"ERROR: The helm package, '{file_path}', is not"
            "a .tgz, .tar or .tar.gz file."
        )

    return Path(target_dir, os.listdir(target_dir)[0])


def snake_case_to_camel_case(text):
    """Converts snake case to camel case."""
    components = text.split("_")
    return components[0] + "".join(x[0].upper() + x[1:] for x in components[1:])


def generate_values_mappings(
    schema_name: str,
    schema: Dict[str, Any],
    values: Dict[str, Any],
    is_nsd: bool = False,
) -> Dict[str, Any]:
    """
    Generate values mappings for a Helm chart.

    Args:
        schema (Dict[str, Any]): The schema of the Helm chart.
        values (Dict[str, Any]): The values of the Helm chart.

    Returns:
        Dict[str, Any]: The value mappings for the Helm chart.
    """
    # Loop through each property in the schema.
    for k, v in schema["properties"].items():
        # If the property is not in the values, and is required, add it to the values.
        if k not in values and k in schema["required"]:
            print(f"Adding {k} to values")
            if v["type"] == "object":
                values[k] = generate_values_mappings(schema_name, v, {}, is_nsd)
            else:
                values[k] = (
                    f"{{configurationparameters('{schema_name}').{k}}}"
                    if is_nsd
                    else f"{{deployParameters.{schema_name}.{k}}}"
                )
        # If the property is in the values, and is an object, generate the values mappings
        # for the subschema.
        if k in values and v["type"] == "object" and values[k]:
            values[k] = generate_values_mappings(schema_name, v, {}, is_nsd)
    return values
