from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def get_defaults(self):
        pass

    @abstractmethod
    def get_schema(self):
        pass
