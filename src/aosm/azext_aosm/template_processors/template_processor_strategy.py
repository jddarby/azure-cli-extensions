from abc import ABC, abstractmethod
from vendored_sdks.models import ResourceElementTemplate, NetworkFunctionApplication


class TemplateProcessorStrategy(ABC):
    """
    Abstract base class for template processor strategy.
    """

    @abstractmethod
    def generate_resource_element_template(self) -> ResourceElementTemplate:
        """
        Abstract method to generate resource element template.
        """
        pass

    @abstractmethod
    def generate_nf_application(self) -> NetworkFunctionApplication:
        """
        Abstract method to generate network function application.
        """
        pass
