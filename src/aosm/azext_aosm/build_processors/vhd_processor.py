# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from typing import List, Tuple
from azext_aosm.build_processors.base_processor import BaseBuildProcessor
from azext_aosm.build_processors.artifact_details import BaseArtifact
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.common.utils import snake_case_to_camel_case
from azext_aosm.input_artifacts.vhd_file import VHDFile
from azext_aosm.vendored_sdks.models import (
    ArtifactStore,
    ArtifactType,
    ApplicationEnablement,
    AzureCoreNetworkFunctionVhdApplication,
    AzureCoreVhdImageArtifactProfile,
    AzureCoreVhdImageDeployMappingRuleProfile,
    DependsOnProfile,
    ReferencedResource,
    ResourceElementTemplate,
    ManifestArtifactFormat,
    VhdImageMappingRuleProfile,
    VhdImageArtifactProfile,
)

class VHDProcessor(BaseBuildProcessor):
    """Base class for build processors."""

    def __init__(self, name: str, artifact_store: ArtifactStore, input_artifact: VHDFile):
        """
        Initialize the HelmChartProcessor class.

        Args:
            artifact_store (ArtifactStore): The artifact store to use for the artifact profile.
            chart (HelmChart): The Helm chart to use for the artifact profile.
        """
        super().__init__(name, artifact_store, input_artifact)
        # assert isinstance(self.input_artifact, HelmChart)

    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        return [
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.VHD_IMAGE_FILE,
                artifact_version=self.input_artifact.artifact_version,
            )
        ]

    def get_artifact_details(self) -> Tuple[List[BaseArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        raise NotImplementedError

    def generate_nf_application(self) -> AzureCoreNetworkFunctionVhdApplication:
        """Generate the NF application."""
        return AzureCoreNetworkFunctionVhdApplication(
            name=self.name,
            depends_on_profile=DependsOnProfile(),
            artifact_profile=self._generate_artifact_profile(),
            deploy_parameters_mapping_rule_profile=self._generate_mapping_rule_profile(),
        )

    def generate_resource_element_template(self) -> ResourceElementTemplate:
        """Generate the resource element template."""
        raise NotImplementedError("NSDs do not support deployment of VHDs.")

    def _generate_artifact_profile(self) -> AzureCoreVhdImageArtifactProfile:
        """Generate the artifact profile."""
        artifact_profile = VhdImageArtifactProfile(
            vhd_name=self.input_artifact.artifact_name,
            vhd_version=self.input_artifact.artifact_version,
        )

        return AzureCoreVhdImageArtifactProfile(
            artifact_store=ReferencedResource(id=self.artifact_store.id),
            vhd_artifact_profile=artifact_profile
        )

    def _generate_mapping_rule_profile(self) -> AzureCoreVhdImageDeployMappingRuleProfile:
        """Generate the mapping rule profile."""

        user_configuration = {
            "imageName": self.input_artifact.artifact_name,
            **{
                snake_case_to_camel_case(key): value
                for key, value in self.input_artifact.get_defaults().items()
                if value is not None
            }
        }

        mapping = VhdImageMappingRuleProfile(
            user_configuration=json.dumps(user_configuration),
        )

        return AzureCoreVhdImageDeployMappingRuleProfile(
            application_enablement=ApplicationEnablement.ENABLED,
            vhd_image_mapping_rule_profile=mapping,
        )
