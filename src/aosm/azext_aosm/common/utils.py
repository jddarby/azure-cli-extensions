# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

from knack.log import get_logger
from knack.util import CLIError

from azext_aosm.common.exceptions import InvalidFileTypeError, MissingDependency

logger = get_logger(__name__)


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
        logger.debug(
            "Converting bicep template %s to ARM.",
            bicep_template_path,
        )

        try:
            subprocess.run(
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
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                f"Bicep to ARM template compilation failed.\n{error.stderr}"
            )

        logger.debug("ARM template:\n%s", arm_path.read_text())
        arm_json = json.loads(arm_path.read_text())

    return arm_json


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


def check_tool_installed(tool_name: str) -> None:
    """
    Check whether a tool such as docker or helm is installed.

    :param tool_name: name of the tool to check, e.g. docker
    """
    if shutil.which(tool_name) is None:
        raise MissingDependency(f"You must install {tool_name} to use this command.")


def call_subprocess_raise_output(cmd: list) -> None:
    """
    Call a subprocess and raise a CLIError with the output if it fails.

    :param cmd: command to run, in list format
    :raise CLIError: if the subprocess fails
    """
    log_cmd = cmd.copy()
    if "--password" in log_cmd:
        # Do not log out passwords.
        log_cmd[log_cmd.index("--password") + 1] = "[REDACTED]"

    try:
        called_process = subprocess.run(
            cmd, encoding="utf-8", capture_output=True, text=True, check=True
        )
        logger.debug(
            "Output from %s: %s. Error: %s",
            log_cmd,
            called_process.stdout,
            called_process.stderr,
        )
        if called_process.returncode == 1:
            return None
        return called_process.stdout
    except subprocess.CalledProcessError as error:
        all_output: str = (
            f"Command: {' '.join(log_cmd)}\n"
            f"stdout: {error.stdout}\n"
            f"stderr: {error.stderr}\n"
            f"Return code: {error.returncode}"
        )
        logger.debug("The following command failed to run:\n%s", all_output)
        # Raise the error without the original exception, which may contain secrets.
        raise CLIError(all_output) from None


def clean_registry_name(registry_name: str) -> str:
    """Remove https:// from the registry name."""
    return registry_name.replace("https://", "")
