# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import inspect
from pathlib import Path

from azext_aosm.definition_folder.reader.base_definition import BaseDefinitionElement
from azext_aosm.common.artifact import ARTIFACT_TYPE_TO_CLASS, BaseArtifact

from typing import List


class ArtifactDefinitionElement(BaseDefinitionElement):
    """Definition for Artifact"""

    artifacts: List[BaseArtifact]

    def __init__(self, path: Path, only_delete_on_clean: bool):
        super().__init__(path, only_delete_on_clean)
        artifact_list = json.loads((path / "artifacts.json").read_text())
        self.artifacts = [self.create_artifact_object(artifact) for artifact in artifact_list]

    def create_artifact_object(self, artifact: dict) -> BaseArtifact:
        """
        Use the inspect module to identify the artifact class's required fields and
        create an instance of the class using the supplied artifact dict.
        """
        if "type" not in artifact or artifact["type"] not in ARTIFACT_TYPE_TO_CLASS:
            raise ValueError("Artifact type is missing or invalid")
        class_sig = inspect.signature(ARTIFACT_TYPE_TO_CLASS[artifact["type"]].__init__)
        class_args = [arg for arg, _ in class_sig.parameters.items() if arg != 'self']
        filtered_dict = {arg: artifact[arg] for arg in class_args}
        if not all(arg in artifact for arg in class_args):
            raise ValueError(f"Artifact is missing required fields."
                             f"Required fields are: {class_args}."
                             f"Artifact is: {artifact}")
        return ARTIFACT_TYPE_TO_CLASS[artifact["type"]](**filtered_dict)

    def deploy(self):
        """Deploy the element."""
        for artifact in self.artifacts:
            artifact.upload()

    def delete(self):
        """Delete the element."""
        # TODO: Implement?
        pass
