# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path
from typing import Dict, List

from knack.log import get_logger

from azext_aosm.common.artifact import BaseArtifact

from .base_builder import BaseDefinitionElementBuilder
from azext_aosm.vendored_sdks.models import (
    NfviDetails,
)
from azext_aosm.definition_folder.builder.json_builder import (
    JSONDefinitionElementBuilder,
)

logger = get_logger(__name__)


class DeploymentInputDefinitionElementBuilder(JSONDefinitionElementBuilder):
    """Deployment input builder"""

    nfvis: Dict[str, NfviDetails]

    def __init__(
        self,
        path: Path,
        nfvis: Dict[str, NfviDetails],
        only_delete_on_clean: bool = False,
    ):
        super().__init__(path, only_delete_on_clean)
        self.nfvis = nfvis

    def write(self):
        """Write the definition element to disk."""
        self.path.mkdir(exist_ok=True)
        nfvis_list = []
        for nfvi in self.nfvis:
            logger.debug(
                "Writing nfvi %s as: %s", self.nfvis[nfvi].name, self.nfvis[nfvi].type
            )
            nfvi_dict = {
                "name": self.nfvis[nfvi].name,
                "nfviType": self.nfvis[nfvi].type,
                "customLocationReference": {
                    "id": ""
                }
            }
            nfvis_list.append(nfvi_dict)
        (self.path / "deploy_input.jsonc").write_text(json.dumps({"nfvis": nfvis_list}, indent=4))