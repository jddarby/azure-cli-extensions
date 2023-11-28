# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod

class BaseDefinitionElementBuilder(ABC):
    """Base element definition builder."""
    # TODO: Implement.

    @abstractmethod
    def deploy(self):
        return NotImplementedError

    @abstractmethod
    def delete(self):
        return NotImplementedError
