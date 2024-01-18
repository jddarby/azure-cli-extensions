from dataclasses import dataclass

from azext_aosm.vendored_sdks import HybridNetworkManagementClient
from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.profiles import ResourceType
from azure.mgmt.resource import ResourceManagementClient
from azure.cli.core import AzCli

from typing import Dict, Optional


@dataclass
class CommandContext:

    cli_ctx: AzCli
    cli_options: Optional[Dict] = None

    def __post_init__(self):
        self.aosm_client: HybridNetworkManagementClient = get_mgmt_service_client(
            self.cli_ctx, HybridNetworkManagementClient, base_url_bound=False
        )
        self.resources_client: ResourceManagementClient = get_mgmt_service_client(
            self.cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES
        )
