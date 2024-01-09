# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# from azext_aosm.cli_handlers.onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from __future__ import annotations
from azext_aosm.cli_handlers.onboarding_cnf_handler import OnboardingCNFCLIHandler
from azext_aosm.cli_handlers.onboarding_vnf_handler import OnboardingVNFCLIHandler
from azext_aosm.cli_handlers.onboarding_nsd_handler import OnboardingNSDCLIHandler
from azext_aosm.common.command_context import CommandContext
from azext_aosm.common.constants import ALL_PARAMETERS_FILE_NAME
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


def onboard_nfd_publish(definition_type: str, output_folder_path: str):
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(output_folder_path + ALL_PARAMETERS_FILE_NAME)
        handler.publish()
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(output_folder_path + ALL_PARAMETERS_FILE_NAME)
        handler.publish()
    else:
        # TODO: better error
        raise Exception("Invalid definition type")


def onboard_nfd_delete(definition_type: str, config_file: str):
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(config_file)
        handler.delete()
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(config_file)
        handler.delete()
    else:
        # TODO: better error
        raise Exception("Invalid definition type")


def onboard_nsd_generate_config(output_file: str | None):
    handler = OnboardingNSDCLIHandler(output_file)
    handler.generate_config(output_file)


def onboard_nsd_build(config_file: str, cmd: AzCliCommand):
    command_context = CommandContext(cli_ctx=cmd.cli_ctx)
    handler = OnboardingNSDCLIHandler(config_file)
    handler.build(command_context.aosm_client)


def onboard_nsd_publish(output_folder_path: str):
    handler = OnboardingNSDCLIHandler(output_folder_path + ALL_PARAMETERS_FILE_NAME)
    handler.publish()


def onboard_nsd_delete(config_file: str):
    handler = OnboardingNSDCLIHandler(config_file)
    handler.delete()
