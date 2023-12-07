
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
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
        try:
            index = self._parse_index_file((path / "index.json").read_text())
        except Exception as e:
            raise ValueError(f"Error parsing index file - {e}")
        self.elements = []
        for element in index:
            if element["type"] == "bicep":
                self.elements.append(BicepDefinitionElement(element["path"], element["only_delete_on_clean"]))
            elif element["type"] == "artifact":
                self.elements.append(ArtifactDefinitionElement(element["path"], element["only_delete_on_clean"]))

    def _parse_index_file(self, file_content: str) -> list[dict[str, any]]:
        """Read the index file. Return a list of dicts containing path, type, only_delete_on_clean"""
        json_content = json.loads(file_content)
        parsed_elements = []
        for element in json_content:
            if "name" not in element:
                raise ValueError("Index file element is missing name")
            if "type" not in element:
                raise ValueError(f"Index file element {element['name']} is missing type")
            if "only_delete_on_clean" not in element:
                element["only_delete_on_clean"] = False
            elif not isinstance(element["only_delete_on_clean"], bool):
                raise ValueError(f"Index file element {element['name']} only_delete_on_clean should be a boolean")
            parsed_elements.append({
                "path": self.path / element["name"],
                "type": element["type"],
                "only_delete_on_clean": element["only_delete_on_clean"]
            })
        return parsed_elements

    def deploy(self, resource_client):
        """Deploy the resources defined in the folder."""
        for element in self.elements:
            element.deploy(resource_client)

    def delete(self, resource_client, clean: bool = False):
        """Delete the definition folder."""
        for element in reversed(self.elements):
            if clean or not element.only_delete_on_clean:
                element.delete(resource_client)
