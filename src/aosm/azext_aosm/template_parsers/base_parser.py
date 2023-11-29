from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

@dataclass
class BaseParser(ABC):

    template_path: Path
    defaults_path: Path

    @abstractmethod
    def get_defaults(self):
        pass

    @abstractmethod
    def get_schema(self):
        pass
