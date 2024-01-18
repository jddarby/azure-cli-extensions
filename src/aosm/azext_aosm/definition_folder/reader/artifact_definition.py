# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import inspect
from pathlib import Path
from typing import List

from azext_aosm.common.artifact import ARTIFACT_TYPE_TO_CLASS, BaseArtifact

from azext_aosm.configuration_models.common_parameters_config import (
    BaseCommonParametersConfig,
)
from azext_aosm.common.command_context import CommandContext
from knack.log import get_logger

from azext_aosm.definition_folder.reader.base_definition import \
    BaseDefinitionElement

logger = get_logger(__name__)


class ArtifactDefinitionElement(BaseDefinitionElement):
    """Definition for Artifact"""  # TODO: Is this actually an artifact manifest?

    def __init__(self, path: Path, only_delete_on_clean: bool):
        super().__init__(path, only_delete_on_clean)
        logger.debug("ArtifactDefinitionElement path: %s", path)
        artifact_list = json.loads((path / "artifacts.json").read_text())
        self.artifacts = [self.create_artifact_object(artifact) for artifact in artifact_list]

    def create_artifact_object(self, artifact: dict) -> BaseArtifact:
        """
        Use the inspect module to identify the artifact class's required fields and
        create an instance of the class using the supplied artifact dict.
        """
        if "type" not in artifact or artifact["type"] not in ARTIFACT_TYPE_TO_CLASS:
            raise ValueError("Artifact type is missing or invalid")
        class_sig = inspect.signature(ARTIFACT_TYPE_TO_CLASS[artifact["type"]].__init__)
        class_args = [arg for arg, _ in class_sig.parameters.items() if arg != 'self']
        logger.debug("Artifact configuration from definition folder: %s", artifact)
        logger.debug("class_args reflection: %s", class_args)
        try:
            filtered_dict = {arg: artifact[arg] for arg in class_args}
        except KeyError as e:
            raise ValueError(f"Artifact is missing required field {e}.\n"
                             f"Required fields are: {class_args}.\n"
                             f"Artifact is: {artifact}")
        if not all(arg in artifact for arg in class_args):
            raise ValueError(f"Artifact is missing required fields.\n"
                             f"Required fields are: {class_args}.\n"
                             f"Artifact is: {artifact}")
        return ARTIFACT_TYPE_TO_CLASS[artifact["type"]](**filtered_dict)

    def deploy(self, config: BaseCommonParametersConfig, command_context: CommandContext):
        """Deploy the element."""
        oras_client = None
        for artifact in self.artifacts:
            logger.info("Deploying artifact %s of type %s", artifact.artifact_name, type(artifact))
            logger.info("Oras client id: %s", id(oras_client))
            if oras_client:
                artifact.upload(config=config, command_context=command_context)
            else:
                oras_client = artifact.upload(config=config, command_context=command_context)

    def delete(self):
        """Delete the element."""
        # TODO: Implement?
        pass
