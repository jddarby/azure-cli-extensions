# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class BaseParser(ABC):
    """
    Base class for template parsers.
    """

    template_path: Path
    defaults_path: Path

    @abstractmethod
    def get_defaults(self) -> Dict[str, Any]:
        """
        Abstract method to get the default values for the template.
        Returns:
            A dictionary containing the default values.
        """
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Abstract method to get the schema for the template.
        Returns:
            A dictionary containing the schema.
        """
        pass
