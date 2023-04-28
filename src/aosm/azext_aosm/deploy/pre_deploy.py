# --------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT
# License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------
"""Contains class for deploying resources required by NFDs/NSDs via the SDK."""

from knack.log import get_logger
from azure.mgmt.resource import ResourceManagementClient
from azure.cli.core.azclierror import AzCLIError

from azext_aosm.vendored_sdks import HybridNetworkManagementClient
from azext_aosm.vendored_sdks.models import (
    ArtifactStore,
    ArtifactStoreType,
    NetworkFunctionDefinitionGroup,
    NetworkServiceDesignGroup,
    Publisher,
)
from azext_aosm._configuration import Configuration, VNFConfiguration

logger = get_logger(__name__)


class PreDeployerViaSDK:
    """A class for checking or publishing resources required by NFDs/NSDs."""

    def __init__(
        self,
        aosm_client: HybridNetworkManagementClient,
        resource_client: ResourceManagementClient,
        config: Configuration,
    ) -> None:
        """
        Initializes a new instance of the Deployer class.

        :param aosm_client: The client to use for managing AOSM resources.
        :type aosm_client: HybridNetworkManagementClient
        :param resource_client: The client to use for managing Azure resources.
        :type resource_client: ResourceManagementClient
        """

        self.aosm_client = aosm_client
        self.resource_client = resource_client
        self.config = config

    def ensure_publisher_exists(
        self, resource_group_name: str, publisher_name: str, location: str
    ) -> None:
        """
        Ensures that the publisher exists in the resource group.

        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param publisher_name: The name of the publisher.
        :type publisher_name: str
        :param location: The location of the publisher.
        :type location: str
        """

        logger.info(
            "Creating publisher %s if it does not exist", publisher_name
        )
        if not self.resource_client.check_existence(
            resource_group_name=resource_group_name,
            resource_type="Microsoft.HybridNetwork/publishers",
            resource_name=publisher_name,
        ):
            self.aosm_client.publishers.begin_create_or_update(
                resource_group_name=resource_group_name,
                publisher_name=publisher_name,
                parameters=Publisher(location=location, scope="Public"),
            )
            
    def ensure_config_publisher_exists(self) -> None:
        """
        Ensures that the publisher exists in the resource group.

        Finds the parameters from self.config
        """
        self.ensure_publisher_exists(self.config.publisher_resource_group_name,
                                     self.config.publisher_name,
                                     self.config.location)

    def ensure_artifact_store_exists(
        self,
        resource_group_name: str,
        publisher_name: str,
        artifact_store_name: str,
        artifact_store_type: ArtifactStoreType,
        location: str,
    ) -> None:
        """
        Ensures that the artifact store exists in the resource group.

        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param publisher_name: The name of the publisher.
        :type publisher_name: str
        :param artifact_store_name: The name of the artifact store.
        :type artifact_store_name: str
        :param artifact_store_type: The type of the artifact store.
        :type artifact_store_type: ArtifactStoreType
        :param location: The location of the artifact store.
        :type location: str
        """

        logger.info(
            "Creating artifact store %s if it does not exist",
            artifact_store_name,
        )
        self.aosm_client.artifact_stores.begin_create_or_update(
            resource_group_name=resource_group_name,
            publisher_name=publisher_name,
            artifact_store_name=artifact_store_name,
            parameters=ArtifactStore(
                location=location,
                artifact_store_type=artifact_store_type,
            ),
        )
        
    def ensure_acr_artifact_store_exists(self) -> None:
        """
        Ensures that the ACR Artifact store exists.

        Finds the parameters from self.config
        """
        self.ensure_artifact_store_exists(self.config.publisher_resource_group_name,
                                          self.config.publisher_name,
                                          self.config.acr_artifact_store_name,
                                          ArtifactStoreType.AZURE_CONTAINER_REGISTRY,
                                          self.config.location)
        
        
    def ensure_sa_artifact_store_exists(self) -> None:
        """
        Ensures that the Storage Account Artifact store for VNF exists.

        Finds the parameters from self.config
        """
        if not isinstance(self.config, VNFConfiguration):
            raise AzCLIError(
                "Check that storage account artifact store exists failed as requires VNFConfiguration file"
            )

        self.ensure_artifact_store_exists(self.config.publisher_resource_group_name,
                                          self.config.publisher_name,
                                          self.config.blob_artifact_store_name,
                                          ArtifactStoreType.AZURE_STORAGE_ACCOUNT,
                                          self.config.location)

    def ensure_nfdg_exists(
        self,
        resource_group_name: str,
        publisher_name: str,
        nfdg_name: str,
        location: str,
    ):
        """
        Ensures that the network function definition group exists in the resource group.

        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param publisher_name: The name of the publisher.
        :type publisher_name: str
        :param nfdg_name: The name of the network function definition group.
        :type nfdg_name: str
        :param location: The location of the network function definition group.
        :type location: str
        """

        logger.info(
            "Creating network function definition group %s if it does not exist",
            nfdg_name,
        )
        self.aosm_client.network_function_definition_groups.begin_create_or_update(
            resource_group_name=resource_group_name,
            publisher_name=publisher_name,
            network_function_definition_group_name=nfdg_name,
            parameters=NetworkFunctionDefinitionGroup(location=location),
        )
        
    def ensure_config_nfdg_exists(
        self,
    ):
        """
        Ensures that the Network Function Definition Group exists.

        Finds the parameters from self.config
        """
        self.ensure_nfdg_exists(self.config.publisher_resource_group_name,
                                self.config.publisher_name,
                                self.config.nfdg_name,
                                self.config.location)

    def ensure_nsdg_exists(
        self,
        resource_group_name: str,
        publisher_name: str,
        nsdg_name: str,
        location: str,
    ):
        """
        Ensures that the network service design group exists in the resource group.

        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param publisher_name: The name of the publisher.
        :type publisher_name: str
        :param nsdg_name: The name of the network service design group.
        :type nsdg_name: str
        :param location: The location of the network service design group.
        :type location: str
        """

        logger.info(
            "Creating network service design group %s if it does not exist",
            nsdg_name,
        )
        self.aosm_client.network_service_design_groups.begin_create_or_update(
            resource_group_name=resource_group_name,
            publisher_name=publisher_name,
            network_service_design_group_name=nsdg_name,
            parameters=NetworkServiceDesignGroup(location=location),
        )
