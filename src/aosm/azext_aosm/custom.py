# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from pathlib import Path

# from azext_aosm.cli_handlers.onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from __future__ import annotations
from azext_aosm.cli_handlers.onboarding_cnf_handler import OnboardingCNFCLIHandler
from azext_aosm.cli_handlers.onboarding_vnf_handler import OnboardingVNFCLIHandler
from azext_aosm.cli_handlers.onboarding_nsd_handler import OnboardingNSDCLIHandler
from azext_aosm.common.command_context import CommandContext
from azure.cli.core.commands import AzCliCommand


def onboard_nfd_generate_config(definition_type: str, output_file: str | None):
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler()
        handler.generate_config(output_file)
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler()
        handler.generate_config(output_file)
    else:
        # TODO: better error
        raise Exception("Invalid definition type")


def onboard_nfd_build(definition_type: str, config_file: str):
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(config_file)
        handler.build()
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(config_file)
        handler.build()
    else:
        # TODO: better error
        raise Exception("Invalid definition type")


def onboard_nfd_publish(
    cmd: AzCliCommand,
    definition_type: str,
    config_file: str,
    no_subscription_permissions: bool = False,
    definition_folder: str | None = None,
):
    # TODO: doc string for use with --help
    command_context = CommandContext(
        cli_ctx=cmd.cli_ctx,
        cli_options={
            "no_subscription_permissions": no_subscription_permissions,
            "definition_folder": Path(definition_folder) if definition_folder else None,
        },
    )
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(config_file)
        handler.publish(command_context=command_context)
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(config_file)
        handler.publish(command_context=command_context)
    else:
        # TODO: better error
        raise Exception("Invalid definition type")


def onboard_nfd_delete(cmd: AzCliCommand, definition_type: str, config_file: str):
    command_context = CommandContext(cmd.cli_ctx)
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(config_file)
        handler.delete(command_context=command_context)
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(config_file)
        handler.delete(command_context=command_context)
    else:
        # TODO: better error
        raise Exception("Invalid definition type")


def onboard_nsd_generate_config(output_file: str | None):
    handler = OnboardingNSDCLIHandler()
    handler.generate_config(output_file)


def onboard_nsd_build(config_file: str):
    handler = OnboardingNSDCLIHandler(config_file)
    handler.build()


def onboard_nsd_publish(cmd: AzCliCommand, config_file: str):
    CommandContext(cmd.cli_ctx)
    handler = OnboardingNSDCLIHandler(config_file)
    handler.publish(command_context=command_context)


def onboard_nsd_delete(cmd: AzCliCommand, config_file: str):
    command_context = CommandContext(cmd.cli_ctx)
    handler = OnboardingNSDCLIHandler(config_file)
    handler.delete(command_context=command_context)
