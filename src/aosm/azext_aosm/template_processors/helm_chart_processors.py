from template_processors.template_processor_strategy import TemplateProcessorStrategy
from vendored_sdks.models import (
    ResourceElementTemplate,
    NetworkFunctionApplication,
    AzureArcKubernetesHelmApplication,
)


class HelmChartProcessor(TemplateProcessorStrategy):
    """
    A template processor for Helm charts.

    This class provides methods to generate resource element templates and network function applications
    for Helm charts.
    """

    def generate_resource_element_template(self) -> ResourceElementTemplate:
        raise NotImplementedError("NSDs do not support deployment of Helm charts.")

    def generate_nf_application(self) -> NetworkFunctionApplication:
        return AzureArcKubernetesHelmApplication()
