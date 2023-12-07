# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path

from .base_builder import BaseDefinitionElementBuilder

from azext_aosm.common.artifact import BaseArtifact

class ArtifactDefinitionElementBuilder(BaseDefinitionElementBuilder):
    """ Artifact builder """
    artifacts: [BaseArtifact]

    def __init__(self, path: Path, artifacts: [BaseArtifact], only_delete_on_clean: bool = False):
        super().__init__(path, only_delete_on_clean)
        self.artifacts = artifacts

    def write(self):
        """Write the definition element to disk."""
        self.path.mkdir()
        artifacts_list = []
        for artifact in self.artifacts:
            artifacts_list.append(artifact.to_dict())
        (self.path / "artifacts.json").write_text(json.dumps(artifacts_list))
        self._write_supporting_files()