# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from typing import List, Tuple
from azext_aosm.build_processors.base_processor import BaseBuildProcessor
from azext_aosm.common.artifact import (
    BaseStorageAccountArtifact,
    BlobStorageAccountArtifact,
    LocalFileStorageAccountArtifact
)
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.common.utils import snake_case_to_camel_case
from azext_aosm.inputs.vhd_file_input import VHDFile
from azext_aosm.vendored_sdks.models import (
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

    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        return [
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.VHD_IMAGE_FILE,
                artifact_version=self.input_artifact.artifact_version,
            )
        ]

    def get_artifact_details(self) -> Tuple[List[BaseStorageAccountArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        artifacts = []
        file_builders = []

        artifact_manifest = ManifestArtifactFormat(
            artifact_name=self.input_artifact.artifact_name,
            artifact_type=ArtifactType.VHD_IMAGE_FILE,
            artifact_version=self.input_artifact.artifact_version,
        )

        self.input_artifact = VHDFile(**self.input_artifact)

        if self.input_artifact.file_path:
            artifacts.append(LocalFileStorageAccountArtifact(
                artifact_manifest=artifact_manifest,
                file_path=self.input_artifact.file_path,
            ))
        elif self.input_artifact.blob_sas_uri:
            artifacts.append(BlobStorageAccountArtifact(
                artifact_manifest=artifact_manifest,
                blob_sas_uri=self.input_artifact.blob_sas_uri,
            ))
        else:
            raise ValueError("VHDFile must have either a file path or a blob SAS URI.")

        return artifacts, file_builders

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
            artifact_store=ReferencedResource(id=""),
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
