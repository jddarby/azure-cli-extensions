# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# May want common get_vnf_handler, and get_cnf_handler, get_nsd_handler.

# Branch based on CNF or VNF
def onboard_nfd_generate_config():
    # If VNF:
        # handler = OnboardVNFCLIHandler()
        # handler.generate_config()
    return NotImplementedError

def onboard_nfd_build():
    return NotImplementedError

def onboard_nfd_deploy():
    return NotImplementedError

def onboard_nfd_delete():
    return NotImplementedError


def onboard_nsd_generate_config():
    return NotImplementedError

def onboard_nsd_build():
    return NotImplementedError

def onboard_nsd_deploy():
    return NotImplementedError

def onboard_nsd_delete():
    return NotImplementedError
