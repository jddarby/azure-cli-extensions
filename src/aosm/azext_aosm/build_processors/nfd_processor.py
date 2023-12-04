# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

@staticmethod
@abstractmethod
def get_artifact_details() -> tuple[list[BaseArtifact], list[LocalFileBuilder]]:
    """Get the artifact details."""

    # TODO: this function will need to generate ARM templates for NFs, and output the corresponding file builder objects.
    raise NotImplementedError

