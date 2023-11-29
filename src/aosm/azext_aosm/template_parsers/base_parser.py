from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class BaseParser(ABC):

    template_path: Path
    defaults_path: Optional(Path)

    @abstractmethod
    def get_defaults(self):
        pass

    @abstractmethod
    def get_schema(self):
        pass
