# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path

from azext_aosm.definition_folder.reader.base_definition import BaseDefinitionElement
from azext_aosm.common.artifact import ARTIFACT_TYPE_TO_CLASS, BaseArtifact


class ArtifactDefinitionElement(BaseDefinitionElement):
    """ Definition for Artifact """
    artifacts: [BaseArtifact]

    def __init__(self, path: Path, only_delete_on_clean: bool):
        super().__init__(path, only_delete_on_clean)
        artifact_list =  json.loads((path / "artifacts.json").read_text())
        self.artifacts = []
        print(ARTIFACT_TYPE_TO_CLASS)
        for artifact in artifact_list:
            if "type" not in artifact or artifact["type"] not in ARTIFACT_TYPE_TO_CLASS:
                raise ValueError("Artifact type is missing or invalid")
            self.artifacts.append(ARTIFACT_TYPE_TO_CLASS[artifact["type"]].from_dict(artifact))

    def deploy(self):
        """Deploy the element."""
        for artifact in self.artifacts:
            artifact.upload()

    def delete(self):
        """Delete the element."""
        # TODO: Implement?
        pass
