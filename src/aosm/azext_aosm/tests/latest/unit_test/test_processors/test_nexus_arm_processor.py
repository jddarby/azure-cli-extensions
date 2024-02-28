import os
import json
from unittest import TestCase
from unittest.mock import patch, MagicMock
from pathlib import Path
from typing import List
from azext_aosm.build_processors.arm_processor import NexusArmBuildProcessor
from azext_aosm.inputs.arm_template_input import ArmTemplateInput
from azext_aosm.vendored_sdks.models import (
    ArtifactType,
    AzureOperatorNexusNetworkFunctionArmTemplateApplication,
    ApplicationEnablement, ArmResourceDefinitionResourceElementTemplate,
    ArmResourceDefinitionResourceElementTemplateDetails,
    ArmTemplateArtifactProfile,
    ArmTemplateMappingRuleProfile,
    AzureCoreArmTemplateArtifactProfile,
    NetworkFunctionApplication, NSDArtifactProfile,
    ResourceElementTemplate, TemplateType, AzureOperatorNexusArtifactType,
    AzureOperatorNexusArmTemplateDeployMappingRuleProfile, AzureOperatorNexusArmTemplateArtifactProfile,
    DependsOnProfile,
    ManifestArtifactFormat,
    ReferencedResource,
)
from azext_aosm.definition_folder.builder.local_file_builder import LocalFileBuilder
from azext_aosm.common.constants import VNF_OUTPUT_FOLDER_FILENAME, ARTIFACT_LIST_FILENAME
from azext_aosm.common.artifact import LocalFileACRArtifact

code_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(code_directory, "../.."))
mock_vnf_directory = os.path.join(parent_directory, "mock_nexus_vnf")


class NexusArmProcessorTest(TestCase):

    def setUp(self):
        mock_arm_template_path = os.path.join(mock_vnf_directory, "ubuntu-template.json")
        self.nexus_arm_input = ArmTemplateInput(
            artifact_name="test-artifact-name",
            artifact_version="1.1.1",
            template_path=mock_arm_template_path,
            default_config=None
        )
        self.processor = NexusArmBuildProcessor("test-name", self.nexus_arm_input)
        
    def test_get_artifact_manifest_list(self):
        """Test get artifact manifest list for nexus arm processor."""
        manifest_list = self.processor.get_artifact_manifest_list()
        mock_manifest_artifact_format = ManifestArtifactFormat(
                artifact_name="test-artifact-name",
                artifact_type="ArmTemplate",
                artifact_version="1.1.1",
            )
        self.assertEqual(len(manifest_list), 1)
        self.assertIsInstance(manifest_list[0], ManifestArtifactFormat)
        self.assertEqual(manifest_list[0], mock_manifest_artifact_format)
        assert True
    
    def test_artifact_details(self):
        """Test get artifact details for nexus arm processor."""
        artifact_details = self.processor.get_artifact_details()
        mock_arm_template_path = os.path.join(mock_vnf_directory, "ubuntu-template.json")
        mock_artifact = [LocalFileACRArtifact(
                    artifact_name="test-artifact-name",
                    artifact_type="ArmTemplate",
                    artifact_version="1.1.1",
                    file_path=mock_arm_template_path,
                )]

        # Ensure no list of LocalFileBuilders is returned, as this is only for NSDs
        self.assertEqual(artifact_details[0][0].artifact_name, mock_artifact[0].artifact_name)
        self.assertEqual(artifact_details[0][0].artifact_version, mock_artifact[0].artifact_version)
        self.assertEqual(artifact_details[0][0].artifact_type, mock_artifact[0].artifact_type)
        self.assertEqual(artifact_details[0][0].file_path, mock_artifact[0].file_path)
        self.assertEqual(artifact_details[1], [])
        assert True

    def test_generate_nf_application(self):
        """Test generate nf application for nexus arm processor."""
        # Check type is correct, other functionality is tested in appropriate functions
        # (such as test_generate_artifact_profile)
        nf_application = self.processor.generate_nf_application()
        self.assertIsInstance(nf_application, AzureOperatorNexusNetworkFunctionArmTemplateApplication)
    
    def test_generate_resource_element_template(self):
        assert True

    def test_generate_parameters_file(self):
        """Test generate parameters file for nexus arm processor."""
        parameters_file = self.processor.generate_parameters_file()
        self.assertIsInstance(parameters_file, LocalFileBuilder)
        
    def test_generate_artifact_profile(self):
        """ Test generate artifact profile returned correctly with generate_nf_application."""
        
        nf_application = self.processor.generate_nf_application()
        expected_arm_artifact_profile = ArmTemplateArtifactProfile(template_name="test-artifact-name", template_version="1.1.1")
        expected_nexus_arm_artifact_profile = AzureOperatorNexusArmTemplateArtifactProfile(
                             artifact_store=ReferencedResource(id=""), 
                             template_artifact_profile=expected_arm_artifact_profile
                             )
        self.assertEqual(nf_application.artifact_profile, expected_nexus_arm_artifact_profile)
        self.assertIsInstance(nf_application.artifact_profile, AzureOperatorNexusArmTemplateArtifactProfile)

    def test_generate_mapping_rule_profile(self):
        """ Test generate artifact profile returned correctly with generate_nf_application."""
        nf_application = self.processor.generate_nf_application()
        mock_template_params = json.dumps({
            "subnetName": "{deployParameters.test-name.subnetName}",
            "virtualNetworkId": "{deployParameters.test-name.virtualNetworkId}",
            "sshPublicKeyAdmin": "{deployParameters.test-name.sshPublicKeyAdmin}",
            "imageName": "{deployParameters.test-name.imageName}"
        })
        expected_arm_mapping_profile = ArmTemplateMappingRuleProfile(template_parameters=mock_template_params)
        expected_nexus_arm_mapping_profile = AzureOperatorNexusArmTemplateDeployMappingRuleProfile(
            application_enablement=ApplicationEnablement.ENABLED,
            template_mapping_rule_profile=expected_arm_mapping_profile,
        )
        self.assertEqual(nf_application.deploy_parameters_mapping_rule_profile, expected_nexus_arm_mapping_profile)
        self.assertIsInstance(nf_application.deploy_parameters_mapping_rule_profile,
                              AzureOperatorNexusArmTemplateDeployMappingRuleProfile)