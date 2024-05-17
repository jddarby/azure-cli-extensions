# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from pathlib import Path
from typing import Dict
from knack.log import get_logger
from azext_aosm.vendored_sdks.models import (
    NfviDetails,
)
from azext_aosm.definition_folder.builder.json_builder import (
    JSONDefinitionElementBuilder,
)
from azext_aosm.common.constants import SNS_DEPLOYMENT_INPUT_FILENAME

logger = get_logger(__name__)


class SNSDeploymentInputDefinitionElementBuilder(JSONDefinitionElementBuilder):
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
        (self.path / SNS_DEPLOYMENT_INPUT_FILENAME).write_text(json.dumps({"nfvis": nfvis_list}, indent=4))
