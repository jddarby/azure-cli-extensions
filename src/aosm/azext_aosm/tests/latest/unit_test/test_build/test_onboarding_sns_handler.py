# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from azext_aosm.cli_handlers.onboarding_sns_handler import OnboardingSNSCLIHandler
from azext_aosm.configuration_models.sns_parameters_config import SNSCommonParametersConfig
from azext_aosm.vendored_sdks import HybridNetworkManagementClient
from azext_aosm.vendored_sdks.models import (
    NetworkServiceDesignVersion,
)
from azext_aosm.common.constants import (
    SNS_OUTPUT_FOLDER_FILENAME,
)

class TestOnboardingSNSCLIHandler(unittest.TestCase):
    @patch('azext_aosm.cli_handlers.onboarding_sns_handler.get_template_path')
    @patch('azext_aosm.cli_handlers.onboarding_sns_handler.render_bicep_contents_from_j2')
    @patch('azext_aosm.cli_handlers.onboarding_sns_handler.BicepDefinitionElementBuilder')
    def test_build_resource_bicep(self, mock_bicep_builder, mock_render_bicep, mock_get_template_path):
        # Arrange
        mock_get_template_path.return_value = 'template_path'
        mock_render_bicep.return_value = 'bicep_contents'
        mock_bicep_builder.return_value = 'bicep_file'
        handler = OnboardingSNSCLIHandler()

        # Act
        result = handler.build_resource_bicep()

        # Assert
        mock_get_template_path.assert_called_once_with('sns', 'snsdefinition.bicep.j2')
        mock_render_bicep.assert_called_once_with('template_path', {})
        mock_bicep_builder.assert_called_once_with(Path('sns-cli-output', 'snsDefinition'), 'bicep_contents')
        self.assertEqual(result, 'bicep_file')
    
    @patch('azext_aosm.cli_handlers.onboarding_sns_handler.CommandContext')
    @patch('azext_aosm.cli_handlers.onboarding_sns_handler.DefinitionFolder')
    def test_deploy(self, mock_definition_folder, mock_command_context):
        # Arrange
        mock_definition_folder_instance = mock_definition_folder.return_value
        mock_command_context_instance = mock_command_context.return_value
        handler = OnboardingSNSCLIHandler()
        handler.config = SNSCommonParametersConfig('location', 'operatorResourceGroupName', 'siteName')

        # Act
        handler.deploy(mock_command_context_instance)

        # Assert
        mock_definition_folder.assert_called_once_with(mock_command_context_instance.cli_options["definition_folder"])
        mock_definition_folder_instance.deploy.assert_called_once_with(config=handler.config, command_context=mock_command_context_instance)

    @patch('azext_aosm.cli_handlers.onboarding_sns_handler.DeploymentInputDefinitionElementBuilder')
    @patch('azext_aosm.cli_handlers.onboarding_sns_handler.OnboardingSNSCLIHandler._get_nsdv')
    def test_build_deploy_input(self, mock_get_nsdv, mock_deployment_input_builder):
        # Arrange
        mock_get_nsdv.return_value = NetworkServiceDesignVersion(location='location', properties=MagicMock(nfvis_from_site='nfvis_from_site'))
        handler = OnboardingSNSCLIHandler()

        # Act
        result = handler.build_deploy_input()

        # Assert
        mock_get_nsdv.assert_called_once()
        mock_deployment_input_builder.assert_called_once_with(Path(SNS_OUTPUT_FOLDER_FILENAME), 'nfvis_from_site')
        self.assertEqual(result, mock_deployment_input_builder.return_value)
