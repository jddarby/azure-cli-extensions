# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from pathlib import Path

class BaseDefinitionElement(ABC):
    """Base element definition."""
    path: str
    only_delete_on_clean: bool

    def __init__(self, path: Path, only_delete_on_clean: bool):
        self.path = path
        self.only_delete_on_clean = only_delete_on_clean

    @abstractmethod
    def deploy(self):
        """Deploy the element."""
        return NotImplementedError
    
    @abstractmethod
    def delete(self):
        """Delete the element."""
        return NotImplementedError
