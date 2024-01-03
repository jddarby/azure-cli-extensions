from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class BaseInput(ABC):

    artifact_name: str
    artifact_version: str
    default_config: Optional[Dict[str, Any]]

    @abstractmethod
    def get_defaults(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        pass
