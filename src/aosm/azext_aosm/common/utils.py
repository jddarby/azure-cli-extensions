# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import tarfile
from pathlib import Path
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
    return components[0] + "".join(
        x[0].upper() + x[1:] for x in components[1:]
    )
