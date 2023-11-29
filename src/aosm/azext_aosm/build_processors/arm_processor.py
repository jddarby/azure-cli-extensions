from abc import abstractmethod
from base_processor import BaseBuildProcessor
from ..vendored_sdks.models import (
    ResourceElementTemplate,
    NetworkFunctionApplication,
    ArmResourceDefinitionResourceElementTemplateDetails,
)


class BaseArmBuildProcessor(BaseBuildProcessor):
    """
    Base class for ARM template processors.

    This class follows the Template Method pattern to define the steps required
    to generate NF applications and RETs from a given ARM template.
    """

    @staticmethod
    def generate_resource_element_template(self) -> ResourceElementTemplate:
        return ArmResourceDefinitionResourceElementTemplateDetails()

    @staticmethod
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


class AzureCoreArmBuildProcessor(BaseArmBuildProcessor):
    """
    This class represents an ARM template processor for Azure Core.
    """

    def generate_nfvi_specific_nf_application(self):
        pass


class NexusArmBuildProcessor(BaseArmBuildProcessor):
    """
    This class represents a processor for generating ARM templates specific to Nexus.
    """

    def generate_nfvi_specific_nf_application(self):
        pass
