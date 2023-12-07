# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

@dataclass
class BaseInputArtifact(ABC):

    artifact_name: str
    artifact_version: str
    artifact_path: Path
    default_config: Optional[Dict[str, Any]] = None

    @abstractmethod
    def get_defaults(self) -> Dict[str, Any]:
        """
        Abstract method to get the default values for configuring the artifact.
        Returns:
            A dictionary containing the default values.
        """
        raise NotImplementedError

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Abstract method to get the schema for configuring the artifact.
        Returns:
            A dictionary containing the schema.
        """
        raise NotImplementedError
