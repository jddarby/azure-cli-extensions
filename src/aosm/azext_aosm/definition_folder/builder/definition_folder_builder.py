
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path
from azure.cli.core.azclierror import UnclassifiedUserFault
from azext_aosm.definition_folder.builder.base_builder import BaseDefinitionElementBuilder
from azext_aosm.definition_folder.builder.bicep_builder import BicepDefinitionElementBuilder

from typing import List
class DefinitionFolderBuilder():
    """Builds and writes out a definition folder for an NFD or NSD."""
    path: Path
    elements : "list[BaseDefinitionElementBuilder]"

    def __init__(self, path: Path):
        self.path = path
        self.elements = []

    def add_element(self, element: BaseDefinitionElementBuilder):
        """Add an element to the definition folder."""
        self.elements.append(element)

    def write(self):
        """Write the definition folder."""
        self._check_for_overwrite()
        self.path.mkdir(exist_ok=True)
        for element in self.elements:
            element.write()
        index_json = []
        for element in self.elements:
            index_json.append({
                "name": element.path.name,
                "type": "bicep" if isinstance(element, BicepDefinitionElementBuilder) else "artifact",
                "only_delete_on_clean": element.only_delete_on_clean
            })
        (self.path / "index.json").write_text(json.dumps(index_json, indent=4))
        # TODO: Write some readme file

    def _check_for_overwrite(self):
        if self.path.exists():
            carry_on = input(
                f"The output folder {self.path.name} already exists in this location - do you want to overwrite it?"
                " (y/n)"
            )
            if carry_on != "y":
                raise UnclassifiedUserFault("User aborted!")

    