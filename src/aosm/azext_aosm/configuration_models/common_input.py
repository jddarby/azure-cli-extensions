# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from dataclasses import dataclass, field


@dataclass
class ArmTemplateConfig:
    """ARM template configuration."""

    artifact_name: str = field(metadata={"comment": "Optional. Name of the artifact."})
    version: str = field(
        metadata={"comment": "Version of the artifact in A.B.C format."}
    )
    file_path: str = field(
        metadata={
            "comment": (
                "File path of the artifact you wish to upload from your local disk. "
                "Relative paths are relative to the configuration file. "
                "On Windows escape any backslash with another backslash."
            )
        }
    )
