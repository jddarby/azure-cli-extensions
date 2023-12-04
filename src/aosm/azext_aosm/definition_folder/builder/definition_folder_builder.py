
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from pathlib import Path

from azext_aosm.definition_folder.builder.base_builder import BaseDefinitionElementBuilder


class DefinitionFolderBuilder():
    """Builds and writes out a definition folder for an NFD or NSD."""
    path: Path
    elements : list[BaseDefinitionElementBuilder]

    def __init__(self, path: Path):
        self.path = path
        self.elements = []

    def add_element(self, element: BaseDefinitionElementBuilder):
        """Add an element to the definition folder."""
        self.elements.append(element)

    def write(self):
        """Write the definition folder."""
        self.path.mkdir()
        for element in self.elements:
            element.write()
        # TODO: Write the index file
        # TODO: Write some readme file
