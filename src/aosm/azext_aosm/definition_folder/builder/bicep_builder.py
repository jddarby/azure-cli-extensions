# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from pathlib import Path
from base_builder import BaseDefinitionElementBuilder

class BicepDefinitionElementBuilder(BaseDefinitionElementBuilder):
    """Bicep definition element builder."""
    bicep_content: str

    def __init__(self, path: Path, bicep_content: str):
        super().__init__(path)
        self.bicep_content = bicep_content

    def write(self):
        """Write the definition element to disk."""
        self.path.mkdir()
        (self.path / "deploy.bicep").write_text(self.bicep_content)

        self._write_supporting_files()
