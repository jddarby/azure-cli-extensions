# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# from azext_aosm.cli_handlers.onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from __future__ import annotations
from pathlib import Path
from azext_aosm.cli_handlers.onboarding_cnf_handler import OnboardingCNFCLIHandler
from azext_aosm.cli_handlers.onboarding_vnf_handler import OnboardingVNFCLIHandler
from azext_aosm.cli_handlers.onboarding_nsd_handler import OnboardingNSDCLIHandler
from azext_aosm.common.command_context import CommandContext
from azext_aosm.common.constants import ALL_PARAMETERS_FILE_NAME
from azure.cli.core.commands import AzCliCommand
from azure.cli.core.azclierror import UnrecognizedArgumentError


def onboard_nfd_generate_config(definition_type: str, output_file: str | None):
    """Generate config file for onboarding NFs."""
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler()
        handler.generate_config(output_file)
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler()
        handler.generate_config(output_file)
    else:
        raise UnrecognizedArgumentError("Invalid definition type")


def onboard_nfd_build(definition_type: str, config_file: Path):
    """Build the NF definition."""
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(Path(config_file))
        handler.build()
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(Path(config_file))
        handler.build()
    else:
        raise UnrecognizedArgumentError("Invalid definition type")


def onboard_nfd_publish(definition_type: str, output_folder_path: Path):
    """Publish the NF definition."""
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(
            output_folder_path + "/" + ALL_PARAMETERS_FILE_NAME
        )
        handler.publish()
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(
            output_folder_path + "/" + ALL_PARAMETERS_FILE_NAME
        )
        handler.publish()
    else:
        raise UnrecognizedArgumentError("Invalid definition type")


def onboard_nfd_delete(definition_type: str, config_file: str):
    """Delete the NF definition."""
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(config_file)
        handler.delete()
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(config_file)
        handler.delete()
    else:
        raise UnrecognizedArgumentError("Invalid definition type")


def onboard_nsd_generate_config(output_file: str | None):
    """Generate config file for onboarding NSD."""
    handler = OnboardingNSDCLIHandler(output_file)
    handler.generate_config(output_file)


def onboard_nsd_build(config_file: Path, cmd: AzCliCommand):
    """Build the NSD definition."""
    command_context = CommandContext(cli_ctx=cmd.cli_ctx)
    handler = OnboardingNSDCLIHandler(Path(config_file), command_context.aosm_client)
    handler.build()


def onboard_nsd_publish(output_folder_path: str):
    """Publish the NSD definition."""
    handler = OnboardingNSDCLIHandler(
        output_folder_path + "/" + ALL_PARAMETERS_FILE_NAME
    )
    handler.publish()


def onboard_nsd_delete(config_file: str):
    """Delete the NSD definition."""
    handler = OnboardingNSDCLIHandler(config_file)
    handler.delete()
