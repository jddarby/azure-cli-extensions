# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from base_definition import BaseDefinitionElement


class BicepDefinitionElement(BaseDefinitionElement):
    """ Bicep definition """

    def __init__(self, path: str, only_delete_on_clean: bool):
        super().__init__(path, only_delete_on_clean)

    def deploy(self):
        """Deploy the element."""
        # TODO: Implement.
        pass

    def delete(self):
        """Delete the element."""
        # TODO: Implement.
        pass