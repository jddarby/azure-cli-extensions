# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from azext_aosm.definition_folder.builder.sns_deploy_input_builder import (
    SNSDeploymentInputDefinitionElementBuilder,
)
from azext_aosm.vendored_sdks.models import NfviDetails


class TestDeploymentInputDefinitionElementBuilder(TestCase):
    """Test the DeploymentInputDefinitionElementBuilder."""

    @patch("pathlib.Path.write_text")
    @patch("pathlib.Path.mkdir")
    def test_write(self, mock_mkdir, mock_write_text):
        """Test writing the definition element to disk."""

        # Create some mocks to act as nfvis.
        nfvi_1 = NfviDetails(name="nfvi1", type="type1")
        nfvi_2 = NfviDetails(name="nfvi2", type="type2")
        nfvis = {"nfvi1": nfvi_1, "nfvi2": nfvi_2}

        # Create a DeploymentInputDefinitionElementBuilder.
        deployment_input_definition_element_builder = SNSDeploymentInputDefinitionElementBuilder(
            Path("/some/folder"), nfvis
        )

        # Write the definition element to disk.
        deployment_input_definition_element_builder.write()

        # Check that the definition element was written to disk.
        mock_mkdir.assert_called_once()
        expected_nfvis = [
            {
                "name": "nfvi1",
                "nfviType": "type1",
                "customLocationReference": {"id": ""},
            },
            {
                "name": "nfvi2",
                "nfviType": "type2",
                "customLocationReference": {"id": ""},
            },
        ]
        expected_params = {"nfvis": expected_nfvis}
        mock_write_text.assert_called_once_with(json.dumps(expected_params, indent=4))