# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path
from typing import List, Tuple

from azext_aosm.build_processors.base_processor import BaseBuildProcessor
from azext_aosm.common.artifact import LocalFileACRArtifact
from azext_aosm.common.local_file_builder import LocalFileBuilder
from azext_aosm.inputs.nfd_input import NFDInput
from azext_aosm.vendored_sdks.models import (
    ArmResourceDefinitionResourceElementTemplate, ArtifactType,
    DependsOnProfile, ManifestArtifactFormat, NetworkFunctionApplication)
from azext_aosm.vendored_sdks.models import \
    NetworkFunctionDefinitionResourceElementTemplateDetails as \
    NFDResourceElementTemplate
from azext_aosm.vendored_sdks.models import (NSDArtifactProfile,
                                             ReferencedResource, TemplateType)

NF_BICEP_TEMPLATE_PATH = Path(__file__).parent.parent / "common" / "templates" / "nf_template.bicep"

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

    def get_artifact_details(
        self,
    ) -> Tuple[List[LocalFileACRArtifact], List[LocalFileBuilder]]:
        """Get the artifact details."""
        assert isinstance(self.input_artifact, NFDInput)
        artifact_details = LocalFileACRArtifact(
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.OCI_ARTIFACT,
                artifact_version=self.input_artifact.artifact_version,
            ),
            self.input_artifact.arm_template_output_path,
        )

        file_builder = LocalFileBuilder(
            self.input_artifact.arm_template_output_path,
            NF_BICEP_TEMPLATE_PATH.read_text(),
        )

        return [artifact_details], [file_builder]

    def generate_nf_application(self) -> NetworkFunctionApplication:
        """Generate the NF application."""
        raise NotImplementedError("NFDs do not support deployment of NFs.")

    def generate_resource_element_template(self) -> NFDResourceElementTemplate:
        """Generate the resource element template."""
        parameter_values_dict = self.generate_values_mappings(
            self.input_artifact.get_schema(), self.input_artifact.get_defaults(), True
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
