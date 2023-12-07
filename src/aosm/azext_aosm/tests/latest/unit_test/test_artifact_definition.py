# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from pathlib import Path
from unittest import TestCase
from unittest.mock import call, MagicMock, patch

from azext_aosm.definition_folder.reader.artifact_definition import ArtifactDefinitionElement


class TestArtifactDefinitionElement(TestCase):
    """Test the Artifact definition element."""

    @patch("pathlib.Path.read_text")
    def test_deploy(self, mock_read_text):
        """Test deploying an Artifact definition element."""

        # Example artifacts.json
        # Fields other than type are ignored as Artifact classes are mocked.
        mock_read_text.return_value = """
        [
            {
                "type": "MockType1",
                "abc": "def"
            },
            {
                "type": "MockType2",
                "ghi": "jkl"
            }
        ]
        """

        # Create artifact type mocks.
        mock_type_1 = MagicMock()
        mock_type_2 = MagicMock()
        mock_artifact_type_to_class = {
            "MockType1": mock_type_1,
            "MockType2": mock_type_2,
        }

        with patch.dict(
            "azext_aosm.definition_folder.reader.artifact_definition.ARTIFACT_TYPE_TO_CLASS",
            mock_artifact_type_to_class
        ):
            # Create an Artifact definition element.
            element_path = Path("/element/path")
            definition_element = ArtifactDefinitionElement(element_path, False)

        # Deploy the element.
        definition_element.deploy()

        # Check results.
        mock_type_1.assert_has_calls(
            [
                call.from_dict({"type": "MockType1", "abc": "def"}),
                call.from_dict().upload(),
            ]
        )
        mock_type_2.assert_has_calls(
            [
                call.from_dict({"type": "MockType2", "ghi": "jkl"}),
                call.from_dict().upload(),
            ]
        )

    @patch("pathlib.Path.read_text")
    def test_delete(self, mock_read_text):
        """Test deleting an Artifact definition element."""

        # Example artifacts.json
        # Fields other than type are ignored as Artifact classes are mocked.
        mock_read_text.return_value = """
        [
            {
                "type": "MockType1",
                "abc": "def"
            },
            {
                "type": "MockType2",
                "ghi": "jkl"
            }
        ]
        """

        # Create artifact type mocks.
        mock_type_1 = MagicMock()
        mock_type_2 = MagicMock()
        mock_artifact_type_to_class = {
            "MockType1": mock_type_1,
            "MockType2": mock_type_2,
        }

        with patch.dict(
            "azext_aosm.definition_folder.reader.artifact_definition.ARTIFACT_TYPE_TO_CLASS",
            mock_artifact_type_to_class
        ):
            # Create an Artifact definition element.
            # only_delete_on_clean is True, but this is not checked in the delete method.
            # It is expected to be checked in the owning DefinitionFolder before calling delete.
            element_path = Path("/element/path")
            definition_element = ArtifactDefinitionElement(element_path, True)

        # Delete the element.
        # TODO: Implement? Currently no-op.
        definition_element.delete()

        # Check results.
        # TODO: Implement.
