# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.profiles import ResourceType

from .vendored_sdks import HybridNetworkManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient


def cf_aosm(cli_ctx, *_) -> HybridNetworkManagementClient:
    return get_mgmt_service_client(cli_ctx, HybridNetworkManagementClient)


def cf_resources(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(
        cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES, subscription_id=subscription_id
    )


def cf_acr_registries(cli_ctx, *_) -> ContainerRegistryManagementClient:
    """
    Returns the client for managing container registries.

    :param cli_ctx: CLI context
    :return: ContainerRegistryManagementClient object
    """
    return get_mgmt_service_client(
        cli_ctx, ResourceType.MGMT_CONTAINERREGISTRY
    ).registries
