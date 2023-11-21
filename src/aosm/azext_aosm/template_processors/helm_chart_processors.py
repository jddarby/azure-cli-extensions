import re
from template_processors.template_processor_strategy import TemplateProcessorStrategy
from template_parsers.helm_chart import HelmChart
from typing import Set
from util.constants import VALUE_PATH_REGEX
from vendored_sdks.models import (
    ArtifactStore,
    AzureArcKubernetesArtifactProfile,
    AzureArcKubernetesDeployMappingRuleProfile,
    DependsOnProfile,
    ReferencedResource,
    ResourceElementTemplate,
    NetworkFunctionApplication,
    AzureArcKubernetesHelmApplication,
    HelmArtifactProfile,
)


class HelmChartProcessor(TemplateProcessorStrategy):
    """
    A template processor for Helm charts.

    This class provides methods to generate resource element templates and network function applications
    for Helm charts.
    """

    @staticmethod
    def generate_resource_element_template() -> ResourceElementTemplate:
        raise NotImplementedError("NSDs do not support deployment of Helm charts.")

    @staticmethod
    def generate_nf_application(
        name: str, artifact_store: ArtifactStore, helm_chart: HelmChart
    ) -> AzureArcKubernetesHelmApplication:
        """
        Generates an Azure Arc Kubernetes Helm application for the given artifact store and Helm chart.

        Args:
            name (str): The name of the Helm application.
            artifact_store (ArtifactStore): The artifact store to use for the artifact profile.
            helm_chart (HelmChart): The Helm chart to use for the artifact profile.

        Returns:
            AzureArcKubernetesHelmApplication: The generated Helm application.
        """
        artifact_profile = HelmChartProcessor._generate_artifact_profile(
            artifact_store=artifact_store, chart=helm_chart
        )
        mapping_rule_profile = HelmChartProcessor._generate_mappings()

        return AzureArcKubernetesHelmApplication(
            name=name,
            depends_on_profile=DependsOnProfile(),
            artifact_profile=artifact_profile,
            deploy_parameters_mapping_rule_profile=mapping_rule_profile,
        )

    @staticmethod
    def _generate_artifact_profile(
        artifact_store: ArtifactStore, chart: HelmChart
    ) -> AzureArcKubernetesArtifactProfile:
        """
        Generates an Azure Arc Kubernetes artifact profile for the given artifact store and Helm chart.

        Args:
            artifact_store (ArtifactStore): The artifact store to use for the artifact profile.
            chart (HelmChart): The Helm chart to use for the artifact profile.

        Returns:
            AzureArcKubernetesArtifactProfile: The generated artifact profile.
        """
        image_pull_secrets_values_paths = set()
        HelmChartProcessor._find_image_pull_secrets_values_paths(
            chart, image_pull_secrets_values_paths
        )
        registry_values_paths = set()
        HelmChartProcessor._find_registry_values_paths(chart, registry_values_paths)
        chart_profile = HelmArtifactProfile(
            helm_package_name=chart.name,
            helm_package_version_range=chart.version,
            registry_values_paths=registry_values_paths,
            image_pull_secrets_values_paths=image_pull_secrets_values_paths,
        )

        return AzureArcKubernetesArtifactProfile(
            artifact_store=ReferencedResource(id=artifact_store.id),
            helm_artifact_profile=chart_profile,
        )

    @staticmethod
    def _generate_mappings() -> AzureArcKubernetesDeployMappingRuleProfile:
        return AzureArcKubernetesDeployMappingRuleProfile()

    @staticmethod
    def _find_image_pull_secrets_values_paths(
        chart: HelmChart, matches: Set[str]
    ) -> None:
        """
        Find image pull secrets values paths in the Helm chart templates.

        Args:
            chart (HelmChart): The Helm chart to search for image pull secrets
            values paths.
            matches (Set[str]): A set of image pull secrets parameters found so far.

        Returns:
            None
        """
        for template in chart.get_templates():
            # Loop through each line in the template.
            for index in range(len(template.data)):
                count = 0
                # If the line contains 'imagePullSecrets:' we check if there is a
                # value path matching the regex. If there is, we add it to the
                # matches set and break the loop. If there is not, we check the
                # next line. We do this until we find a line that contains a match.
                # NFM provides the image pull secrets parameter as a list. If we find
                # a line that contains 'name:' we know that the image pull secrets
                # parameter value path is for a string and not a list, and
                # so we can break from the loop.
                while ("imagePullSecrets:" in template.data[index]) and (
                    "name:" not in template.data[index + count]
                ):
                    new_matches = re.findall(
                        VALUE_PATH_REGEX, template.data[index + count]
                    )
                    if len(new_matches) != 0:
                        matches.update(new_matches)
                        break

                    count += 1

        # Recursively search the dependency charts for image pull secrets parameters
        for chart in chart.dependencies:
            HelmChartProcessor._find_image_pull_secrets_values_paths(chart, matches)

    @staticmethod
    def _find_registry_values_paths(chart: HelmChart, matches: Set[str]) -> None:
        """
        Find registry values paths in the Helm chart templates.

        Args:
            chart (HelmChart): The Helm chart to search for registry values paths.
            matches (Set[str]): A set of registry values paths found so far.

        Returns:
            None
        """
        for template in chart.get_templates():
            for line in template.data:
                if "image:" in line:
                    # Images are specified in the format <registry>/<image>:<tag>
                    # so we split the line on '/' and then find the value path
                    # in the first element of the resulting list.
                    print(f"line: {line}")
                    new_matches = re.findall(VALUE_PATH_REGEX, line.split("/")[0])
                    print(f"new_matches: {new_matches}")
                    if len(new_matches) != 0:
                        matches.update(new_matches)

        # Recursively search the dependency charts for registry values paths
        for chart in chart.dependencies:
            HelmChartProcessor._find_registry_values_paths(chart, matches)
