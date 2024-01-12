from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from azure.cli.core import AzCli
from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.profiles import ResourceType
from azure.mgmt.resource import ResourceManagementClient

from azext_aosm.vendored_sdks import HybridNetworkManagementClient


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

        # Old CLI also had a feature client and an ACR registry client, but they don't seem necessary.
        # Excluding from here for now, but leaving this note as a reminder in case we need to add them later.
        # TODO: Remove above note if we don't need to add them.
