# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path
from typing import List, Tuple

from knack.log import get_logger

from azext_aosm.build_processors.base_processor import BaseInputProcessor
from azext_aosm.common.artifact import BaseArtifact, LocalFileACRArtifact
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

logger = get_logger(__name__)

NF_BICEP_TEMPLATE_PATH = (
    Path(__file__).parent.parent / "common" / "templates" / "nf_template.bicep"
)

NF_BICEP_TEMPLATE_PATH = (
    Path(__file__).parent.parent / "common" / "templates" / "nf_template.bicep"
)


class NFDProcessor(BaseInputProcessor):
    """
    A class for processing NFD inputs.

    :param name: The name of the artifact.
    :type name: str
    :param input_artifact: The input artifact.
    :type input_artifact: NFDInput
    """

    def __init__(self, name: str, input_artifact: NFDInput):
        super().__init__(name, input_artifact)
        self.input_artifact: NFDInput = input_artifact

    def get_artifact_manifest_list(self) -> List[ManifestArtifactFormat]:
        """
        Get the list of artifacts for the artifact manifest.

        :return: A list of artifacts for the artifact manifest.
        :rtype: List[ManifestArtifactFormat]
        """
        logger.info("Getting artifact manifest list for NFD input.")
        return [
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.OCI_ARTIFACT.value,
                artifact_version=self.input_artifact.artifact_version,
            )
        ]

    def get_artifact_details(
        self,
    ) -> Tuple[List[BaseArtifact], List[LocalFileBuilder]]:
        """
        Get the artifact details for publishing.

        :return: A tuple containing the list of artifacts and the list of local file builders.
        :rtype: Tuple[List[BaseArtifact], List[LocalFileBuilder]]
        """
        logger.info("Getting artifact details for NFD input.")

        # The ARM template is written to a local file to be used as the artifact
        artifact_details = LocalFileACRArtifact(
            ManifestArtifactFormat(
                artifact_name=self.input_artifact.artifact_name,
                artifact_type=ArtifactType.OCI_ARTIFACT.value,
                artifact_version=self.input_artifact.artifact_version,
            ),
            self.input_artifact.arm_template_output_path,
        )

        # Create a local file builder for the ARM template
        file_builder = LocalFileBuilder(
            self.input_artifact.arm_template_output_path,
            NF_BICEP_TEMPLATE_PATH.read_text(),
        )

        return [artifact_details], [file_builder]

    def generate_nf_application(self) -> NetworkFunctionApplication:
        """
        Generate the network function application from the input.

        :raises NotImplementedError: NFDs do not support deployment of NFs.
        """
        raise NotImplementedError("NFDs do not support deployment of NFs.")

    def generate_resource_element_template(self) -> NFDResourceElementTemplate:
        """
        Generate the resource element template from the input.

        :return: The resource element template.
        :rtype: NFDResourceElementTemplate
        """
        logger.info("Generating resource element template for NFD input.")
        parameter_values_dict = self.generate_values_mappings(
            self.input_artifact.get_schema(), self.input_artifact.get_defaults(), True
        )

        artifact_profile = NSDArtifactProfile(
            artifact_store_reference=ReferencedResource(id=""),
            artifact_name=self.input_artifact.artifact_name,
            artifact_version=self.input_artifact.artifact_version,
        )

        configuration = ArmResourceDefinitionResourceElementTemplate(
            template_type=TemplateType.ARM_TEMPLATE.value,
            artifact_profile=artifact_profile,
            parameter_values=json.dumps(parameter_values_dict),
        )

        return NFDResourceElementTemplate(
            name=self.name,
            configuration=configuration,
            depends_on_profile=DependsOnProfile(),
        )
