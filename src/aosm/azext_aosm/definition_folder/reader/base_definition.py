# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod

class BaseDefinitionElement(ABC):
    """Base element definition."""
    # TODO: Implement.

    @abstractmethod
    def write(self):
        return NotImplementedError


    def add_supporting_file(self):
        return NotImplementedError
