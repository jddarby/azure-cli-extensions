# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json

from base_definition import BaseDefinitionElement
from azext_aosm.build_processors.artifact_details import BaseArtifact


class ArtifactDefinitionElement(BaseDefinitionElement):
    """ Definition for Artifact """
    artifacts: [BaseArtifact]

    def __init__(self, path: str, only_delete_on_clean: bool):
        super().__init__(path, only_delete_on_clean)
        artifact_list =  json.loads((path / "artifacts.json").read_text())
        for artifact in artifact_list:
            self.artifacts.append(BaseArtifact.from_dict(artifact))

    def deploy(self):
        """Deploy the element."""
        for artifact in self.artifacts:
            artifact.upload()

    def delete(self):
        """Delete the element."""
        # TODO: Implement?
        pass
