import json
import re
from typing import Any, Dict, List, Set, Tuple

from azext_aosm.build_processors.base_processor import BaseBuildProcessor
from azext_aosm.common.artifact import (BaseACRArtifact, LocalFileACRArtifact,
                                        RemoteACRArtifact)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.common.utils import generate_values_mappings
from azext_aosm.inputs.helm_chart_input import HelmChartInput
from azext_aosm.vendored_sdks.models import (
    ApplicationEnablement, ArtifactType, AzureArcKubernetesArtifactProfile,
    AzureArcKubernetesDeployMappingRuleProfile,
    AzureArcKubernetesHelmApplication, DependsOnProfile, HelmArtifactProfile,
    HelmMappingRuleProfile, ManifestArtifactFormat, ReferencedResource,
    ResourceElementTemplate)

VALUE_PATH_REGEX = (
    r".Values\.([^\s})]*)"  # Regex to find values paths in Helm chart templates
)


class HelmChartProcessor(BaseBuildProcessor):
    """
    A template processor for Helm charts.

    This class provides methods to generate resource element templates and network function applications
    for Helm charts.
    """

    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        artifact_manifest_list = []
        artifact_manifest_list.append(
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.OCI_ARTIFACT,
                artifact_version=self.input_artifact.artifact_version,
            )
        )

        for image_name, image_version in self._find_chart_images():
            artifact_manifest_list.append(
                ManifestArtifactFormat(
                    artifact_name=image_name,
                    artifact_type=ArtifactType.OCI_ARTIFACT,
                    artifact_version=image_version,
                )
            )

        return artifact_manifest_list

    def get_artifact_details(
        self,
    ) -> Tuple[List[BaseACRArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        assert isinstance(self.input_artifact, HelmChartInput)
        artifact_details = []
        helm_chart_details = LocalFileACRArtifact(
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.OCI_ARTIFACT,
                artifact_version=self.input_artifact.artifact_version,
            ),
            self.input_artifact.chart_path,
        )
        artifact_details.append(helm_chart_details)

        for image_name, image_version in self._find_chart_images():
            artifact_details.append(
                RemoteACRArtifact(
                    ManifestArtifactFormat(
                        artifact_name=image_name,
                        artifact_type=ArtifactType.OCI_ARTIFACT,
                        artifact_version=image_version,
                    ),
                    self.input_artifact.image_source_acr,
                )
            )

        return artifact_details, []

    def generate_resource_element_template(self) -> ResourceElementTemplate:
        raise NotImplementedError("NSDs do not support deployment of Helm charts.")

    def generate_nf_application(self) -> AzureArcKubernetesHelmApplication:
        """
        Generates an Azure Arc Kubernetes Helm application for the given artifact store and Helm chart.

        Returns:
            AzureArcKubernetesHelmApplication: The generated Helm application.
        """
        artifact_profile = self._generate_artifact_profile()
        # We want to remove the registry values paths and image pull secrets values paths from the values mappings
        # as these values are supplied by NFM when it installs the chart.
        values_to_remove = (
            artifact_profile.helm_artifact_profile.registry_values_paths
            | artifact_profile.helm_artifact_profile.image_pull_secrets_values_paths
        )
        mapping_rule_profile = self._generate_mapping_rule_profile(values_to_remove)

        return AzureArcKubernetesHelmApplication(
            name=self.name,
            depends_on_profile=DependsOnProfile(),
            artifact_profile=artifact_profile,
            deploy_parameters_mapping_rule_profile=mapping_rule_profile,
        )

    def _find_chart_images(self) -> List[Tuple[str, str]]:
        """
        Find the images used in the Helm chart.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing the image registry and image name.
        """
        image_lines: Set[str] = set()
        self._find_image_lines(image_lines)

        images: List[Tuple[str, str]] = []
        for line in image_lines:
            # Images are specified in the format <registry>/<image>:<tag>
            # so we split the line on '/' and then split the second element
            # of the resulting list on ':' to get the image name and tag.
            name_and_tag = line.split("/")[1].split(":")
            images.append((name_and_tag[0], name_and_tag[1]))

        return images

    def _find_image_lines(self, chart: HelmChartInput, image_lines: Set[str]) -> None:
        """
        Finds the lines containing image references in the given Helm chart and its dependencies.

        Args:
            image_lines (Set[str]): A set to store the found image lines.

        Returns:
            None
        """
        for template in chart.get_templates():
            for line in template.data:
                if "image:" in line:
                    image_lines.add(line.replace("image:", "").strip())

        for dep in chart.get_dependencies():
            self._find_image_lines(dep, image_lines)

    def _generate_artifact_profile(self) -> AzureArcKubernetesArtifactProfile:
        """
        Generates an Azure Arc Kubernetes artifact profile for the given artifact store and Helm chart.

        Returns:
            AzureArcKubernetesArtifactProfile: The generated artifact profile.
        """
        image_pull_secrets_values_paths: Set[str] = set()
        self._find_image_pull_secrets_values_paths(image_pull_secrets_values_paths)

        registry_values_paths: Set[str] = set()
        self._find_registry_values_paths(registry_values_paths)

        chart_profile = HelmArtifactProfile(
            helm_package_name=self.input_artifact.artifact_name,
            helm_package_version_range=self.input_artifact.artifact_version,
            registry_values_paths=registry_values_paths,
            image_pull_secrets_values_paths=image_pull_secrets_values_paths,
        )

        return AzureArcKubernetesArtifactProfile(
            artifact_store=ReferencedResource(id=""),
            helm_artifact_profile=chart_profile,
        )

    def _find_image_pull_secrets_values_paths(self, matches: Set[str]) -> None:
        """
        Find image pull secrets values paths in the Helm chart templates.

        Args:
            chart (HelmChartInput): The Helm chart to search for image pull secrets
            values paths.
            matches (Set[str]): A set of image pull secrets parameters found so far.

        Returns:
            None
        """
        for template in self.input_artifact.get_templates():
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
        for chart in self.input_artifact.get_dependencies():
            HelmChartProcessor._find_image_pull_secrets_values_paths(chart, matches)

    def _find_registry_values_paths(self, matches: Set[str]) -> None:
        """
        Find registry values paths in the Helm chart templates.

        Args:
            chart (HelmChartInput): The Helm chart to search for registry values paths.
            matches (Set[str]): A set of registry values paths found so far.

        Returns:
            None
        """
        image_lines: Set[str] = set()
        for line in self._find_image_lines(image_lines):
            # Images are specified in the format <registry>/<image>:<tag>
            # so we split the line on '/' and then find the value path
            # in the first element of the resulting list.
            new_matches = re.findall(VALUE_PATH_REGEX, line.split("/")[0])
            if len(new_matches) != 0:
                matches.update(new_matches)

    def _generate_mapping_rule_profile(
        self, values_to_remove: Set[str]
    ) -> AzureArcKubernetesDeployMappingRuleProfile:
        """
        Generate the mappings for a Helm chart.

        Args:
            name (str): The name of the Helm release.
            chart (HelmChartInput): The Helm chart object.
            values_to_remove (Set[str]): The values to remove from the values mappings.

        Returns:
            AzureArcKubernetesDeployMappingRuleProfile: The mapping rule profile for Azure Arc Kubernetes deployment.
        """
        # Generate the values mappings for the Helm chart.
        values_mappings = generate_values_mappings(
            self.name,
            self.input_artifact.get_schema(),
            self.input_artifact.get_defaults(),
        )

        # Remove the values to remove from the values mappings.
        for value_to_remove in values_to_remove:
            self._remove_key_from_dict(values_mappings, value_to_remove)

        # TODO: Should namespace be configurable?
        mapping_rule_profile = HelmMappingRuleProfile(
            release_name=self.name,
            release_namespace=self.name,
            helm_package_version=self.input_artifact.artifact_version,
            values=json.dumps(values_mappings),
        )

        return AzureArcKubernetesDeployMappingRuleProfile(
            application_enablement=ApplicationEnablement.ENABLED,
            helm_mapping_rule_profile=mapping_rule_profile,
        )

    def _remove_key_from_dict(self, dictionary: Dict[str, Any], path: str) -> None:
        """
        Remove a key from a nested dictionary based on the given path.

        Args:
            dictionary (Dict[str, Any]): The nested dictionary.
            path (str): The path to the key in dot notation.

        Returns:
            None: This method does not return anything.
        """
        # Split the path by the dot character
        keys = path.split(".")
        # Check if the path is valid
        if len(keys) == 0 or keys[0] not in dictionary:
            return None  # Invalid path
        # If the path has only one key, remove it from the dictionary
        if len(keys) == 1:
            del dictionary[keys[0]]
            return None  # Key removed
        # Otherwise, recursively call the function on the sub-dictionary
        return self._remove_key_from_dict(dictionary[keys[0]], ".".join(keys[1:]))
