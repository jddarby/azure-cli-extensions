from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class BaseInput(ABC):

    artifact_name: str
    artifact_version: str
    default_config: Optional[Dict[str, Any]] = None

    @abstractmethod
    def get_defaults(self):
        pass

    @abstractmethod
    def get_schema(self):
        pass
