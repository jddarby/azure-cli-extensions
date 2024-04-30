import unittest
from unittest.mock import Mock, patch
from azext_aosm.definition_folder.reader.bicep_definition import BicepDefinitionElement
from azure.core.exceptions import ResourceNotFoundError
from azext_aosm.configuration_models.common_parameters_config import (
    CoreVNFCommonParametersConfig,
    CNFCommonParametersConfig,
    NexusVNFCommonParametersConfig,
    NSDCommonParametersConfig,
)

class TestBicepDefinitionElement(unittest.TestCase):
    @patch('azext_aosm.definition_folder.reader.bicep_definition.azure_exceptions.ResourceNotFoundError', new_callable=ResourceNotFoundError)
    def setUp(self, mock_exception):
        self.command_context = Mock()
        self.config = Mock()
        self.mock_exception = mock_exception

        self.resources = {
            "cnf": CNFCommonParametersConfig(
                location="test_location",
                acrManifestName="test_acr_manifest",
                nfDefinitionVersion="test_nf_version",
                publisherResourceGroupName="test_resource_group",
                publisherName="test_publisher",
                acrArtifactStoreName="test_acr_store",
                nfDefinitionGroup="test_nf_group",
            ),
            "vnf": CoreVNFCommonParametersConfig(
                location="test_location",
                publisherResourceGroupName="test_resource_group",
                publisherName="test_publisher",
                acrArtifactStoreName="test_acr_store",
                acrManifestName="test_acr_manifest",
                saArtifactStoreName="test_sa_store",
                saManifestName="test_sa_manifest",
                nfDefinitionGroup="test_nf_group",
                nfDefinitionVersion="test_nf_version",
            ),
            "nexus_vnf": NexusVNFCommonParametersConfig(
                location="test_location",
                nfDefinitionVersion="test_nf_version",
                acrManifestName="test_acr_manifest",
                publisherResourceGroupName="test_resource_group",
                publisherName="test_publisher",
                acrArtifactStoreName="test_acr_store",
                nfDefinitionGroup="test_nf_group",
            ),
            "nsd": NSDCommonParametersConfig(
                location="test_location",
                publisherResourceGroupName="test_resource_group",
                publisherName="test_publisher",
                acrArtifactStoreName="test_acr_store",
                acrManifestName="test_acr_manifest",
                nsDesignGroup="test_ns_group",
                nsDesignVersion="test_ns_version",
                nfviSiteName="test_nfvi_site",
            ),
        }

    def test_base_resources_exist_all_exist(self):
        for resource_type, config in self.resources.items():
            with self.subTest(resource_type=resource_type):
                self.command_context.reset_mock()
                result = BicepDefinitionElement._base_resources_exist(config, self.command_context)
                self.assertTrue(result)
    
    def test_base_resources_exist_few_base_resources_missing(self):
        for resource_type, config in self.resources.items():
            with self.subTest(resource_type=resource_type):
                self.command_context.aosm_client.publishers.get.side_effect = self.mock_exception
                result = BicepDefinitionElement._base_resources_exist(config, self.command_context)
                self.assertFalse(result)

    def test_base_resources_exist_all_base_resources_missing_cnf(self):
        self.config = self.resources["cnf"]
        self.command_context.aosm_client.publishers.get.side_effect = self.mock_exception
        self.command_context.aosm_client.artifact_stores.get.side_effect = self.mock_exception
        self.command_context.aosm_client.network_function_definition_groups.get.side_effect = self.mock_exception
        result = BicepDefinitionElement._base_resources_exist(self.config, self.command_context)
        self.assertFalse(result)

    def test_base_resources_exist_all_base_resources_missing_vnf(self):
        self.config = self.resources["vnf"]
        self.command_context.aosm_client.publishers.get.side_effect = self.mock_exception
        self.command_context.aosm_client.artifact_stores.get.side_effect = self.mock_exception
        self.command_context.aosm_client.network_function_definition_groups.get.side_effect = self.mock_exception
        self.command_context.aosm_client.storage_accounts.get.side_effect = self.mock_exception
        result = BicepDefinitionElement._base_resources_exist(self.config, self.command_context)
        self.assertFalse(result)

    def test_base_resources_exist_all_base_resources_missing_nexus_vnf(self):
        self.config = self.resources["nexus_vnf"]
        self.command_context.aosm_client.publishers.get.side_effect = self.mock_exception
        self.command_context.aosm_client.artifact_stores.get.side_effect = self.mock_exception
        self.command_context.aosm_client.network_function_definition_groups.get.side_effect = self.mock_exception
        result = BicepDefinitionElement._base_resources_exist(self.config, self.command_context)
        self.assertFalse(result)

    def test_base_resources_exist_all_base_resources_missing_nsd(self):
        self.config = self.resources["nsd"]
        self.command_context.aosm_client.publishers.get.side_effect = self.mock_exception
        self.command_context.aosm_client.artifact_stores.get.side_effect = self.mock_exception
        self.command_context.aosm_client.network_service_design_groups.get.side_effect = self.mock_exception
        result = BicepDefinitionElement._base_resources_exist(self.config, self.command_context)
        self.assertFalse(result)