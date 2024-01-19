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
        Use reflection (via the inspect module) to identify the artifact class's required fields
        and create an instance of the class using the supplied artifact dict.
        """
        print("artifact: ", artifact)
        if "type" not in artifact or artifact["type"] not in ARTIFACT_TYPE_TO_CLASS:
            raise ValueError("Artifact type is missing or invalid for artifact {artifact}")
        # Use reflection to get the required fields for the artifact class
        class_sig = inspect.signature(ARTIFACT_TYPE_TO_CLASS[artifact["type"]].__init__)
        class_args = [arg for arg, _ in class_sig.parameters.items() if arg != 'self']
        logger.debug("Artifact configuration from definition folder: %s", artifact)
        logger.debug("class_args found for artifact type %s: %s", artifact["type"], class_args)
        # Filter the artifact dict to only include the required fields, erroring if any are missing
        try:
            filtered_dict = {arg: artifact[arg] for arg in class_args}
        except KeyError as e:
            raise ValueError(f"Artifact is missing required field {e}.\n"
                             f"Required fields are: {class_args}.\n"
                             f"Artifact is: {artifact}.\n"
                             "This is unexpected and most likely comes from manual editing "
                             "of the definition folder.")
        return ARTIFACT_TYPE_TO_CLASS[artifact["type"]](**filtered_dict)

    def deploy(self, config: BaseCommonParametersConfig, command_context: CommandContext):
        """Deploy the element."""
        for artifact in self.artifacts:
            logger.info("Deploying artifact %s of type %s", artifact.artifact_name, type(artifact))
            artifact.upload(config=config, command_context=command_context)

    def delete(self):
        """Delete the element."""
        # TODO: Implement?
        pass
