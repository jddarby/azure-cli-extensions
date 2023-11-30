
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from pathlib import Path

from azext_aosm.definition_folder.reader.base_definition import BaseDefinitionElement
from azext_aosm.definition_folder.reader.bicep_definition import BicepDefinitionElement
from azext_aosm.definition_folder.reader.artifact_definition import ArtifactDefinitionElement


class DefinitionFolder():
    """Represents a definition folder for an NFD or NSD."""
    path: Path
    elements: list[BaseDefinitionElement]

    def __init__(self, path: Path):
        self.path = path
        index = self._parse_index_file((path / "index.json").read_text())
        for element in index:
            if element["type"] == "bicep":
                self.elements.append(BicepDefinitionElement(element["path"], element["only_delete_on_clean"]))
            elif element["type"] == "artifact":
                self.elements.append(ArtifactDefinitionElement(element["path"], element["only_delete_on_clean"]))

    def _parse_index_file(self) -> list[dict[str, any]]:
        """Read the index file. Return a list of dicts containing path, type, only_delete_on_clean"""
        # TODO: Implement.
        pass

    def deploy(self):
        """Deploy the resources defined in the folder."""
        for element in self.elements:
            element.deploy()

    def delete(self):
        """Delete the definition folder."""
        for element in self.elements:
            element.delete()
