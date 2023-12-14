# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from typing import List, Tuple
from azext_aosm.build_processors.base_processor import BaseBuildProcessor
from azext_aosm.common.artifact import BaseArtifact
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.common.utils import generate_values_mappings
from azext_aosm.vendored_sdks.models import (
    ArmResourceDefinitionResourceElementTemplate,
    ArtifactType,
    DependsOnProfile,
    NetworkFunctionApplication,
    NetworkFunctionDefinitionResourceElementTemplateDetails as NFDResourceElementTemplate,
    NSDArtifactProfile,
    ReferencedResource,
    ManifestArtifactFormat,
    TemplateType,
)


class NFDProcessor(BaseBuildProcessor):
    """Base class for build processors."""

    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """Get the artifact list."""
        return [
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.OCI_ARTIFACT,
                artifact_version=self.input_artifact.artifact_version,
            )
        ]

    def get_artifact_details(self) -> Tuple[List[BaseArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        return [], []

    def generate_nf_application(self) -> NetworkFunctionApplication:
        """Generate the NF application."""
        raise NotImplementedError("NFDs do not support deployment of NFs.")

    def generate_resource_element_template(self) -> NFDResourceElementTemplate:
        """Generate the resource element template."""
        parameter_values_dict = generate_values_mappings(
            schema_name=self.name,
            schema=self.input_artifact.get_schema(),
            values=self.input_artifact.get_defaults(),
            is_nsd=True,
        )

        configuration = ArmResourceDefinitionResourceElementTemplate(
            template_type=TemplateType.ARM_TEMPLATE,
            artifact_profile=self._generate_artifact_profile(),
            parameter_values=json.dumps(parameter_values_dict),
        )
        return NFDResourceElementTemplate(
            name=self.name,
            configuration=configuration,
            depends_on_profile=DependsOnProfile(),
        )

    def _generate_artifact_profile(self) -> NSDArtifactProfile:
        """Generate the artifact profile."""
        return NSDArtifactProfile(
            artifact_store_reference=ReferencedResource(id=""),
            artifact_name=self.input_artifact.artifact_name,
            artifact_version=self.input_artifact.artifact_version,
        )
