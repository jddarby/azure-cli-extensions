from abc import abstractmethod
from template_processors.template_processor_strategy import TemplateProcessorStrategy
from vendored_sdks.models import (
    ResourceElementTemplate,
    NetworkFunctionApplication,
    ArmResourceDefinitionResourceElementTemplateDetails,
)


class BaseArmTemplateProcessor(TemplateProcessorStrategy):
    """
    Base class for ARM template processors.

    This class provides a set of template methods to generate NF applications
    and RETs from a given ARM template.
    """

    def generate_resource_element_template(self) -> ResourceElementTemplate:
        return ArmResourceDefinitionResourceElementTemplateDetails()

    def generate_nf_application(self) -> NetworkFunctionApplication:
        self.generate_schema()
        self.generate_mappings()
        self.generate_artifact_profile()
        self.generate_nfvi_specific_nf_application()
        return NetworkFunctionApplication()

    def generate_schema(self):
        pass

    def generate_mappings(self):
        pass

    # @abstractmethod?
    def generate_artifact_profile(self):
        pass

    @abstractmethod
    def generate_nfvi_specific_nf_application(self):
        pass


class AzureCoreArmTemplateProcessor(BaseArmTemplateProcessor):
    """
    This class represents an ARM template processor for Azure Core.
    """

    def generate_nfvi_specific_nf_application(self):
        pass


class NexusArmTemplateProcessor(BaseArmTemplateProcessor):
    """
    This class represents a processor for generating ARM templates specific to Nexus.
    """

    def generate_nfvi_specific_nf_application(self):
        pass
