# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from base_definition import BaseDefinitionElement

class BicepDefinitionElement(BaseDefinitionElement):
    """ Bicep definition """

    def write(self):
        return NotImplementedError

    def add_supporting_file(self):
        return NotImplementedError
    