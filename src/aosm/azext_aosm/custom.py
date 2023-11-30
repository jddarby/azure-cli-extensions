# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# from azext_aosm.cli_handlers.onboarding_nfd_base_handler import OnboardingNFDBaseCLIHandler
from azext_aosm.cli_handlers.onboarding_cnf_handler import OnboardingCNFCLIHandler
from azext_aosm.cli_handlers.onboarding_vnf_handler import OnboardingVNFCLIHandler
from azext_aosm.cli_handlers.onboarding_nsd_handler import OnboardingNSDCLIHandler


def onboard_nfd_generate_config(definition_type: str):
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler()
        handler.generate_config("cnf-input.jsonc")
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler()
        handler.generate_config("vnf-input.jsonc")
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


def onboard_nfd_publish(definition_type: str, config_file: str):
    if definition_type == "cnf":
        handler = OnboardingCNFCLIHandler(config_file)
        handler.publish()
    elif definition_type == "vnf":
        handler = OnboardingVNFCLIHandler(config_file)
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


def onboard_nsd_generate_config():
    handler = OnboardingNSDCLIHandler()
    handler.generate_config("nsd-input.jsonc")


def onboard_nsd_build(config_file: str):
    handler = OnboardingNSDCLIHandler(config_file)
    handler.build()


def onboard_nsd_publish(config_file: str):
    handler = OnboardingNSDCLIHandler(config_file)
    handler.publish()


def onboard_nsd_delete(config_file: str):
    handler = OnboardingNSDCLIHandler(config_file)
    handler.delete()
