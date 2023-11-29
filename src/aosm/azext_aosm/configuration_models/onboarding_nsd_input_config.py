# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from common_input import ArmTemplatePropertiesConfig
from onboarding_base_input_config import OnboardingBaseInputConfig


@dataclass
class NetworkFunctionPropertiesConfig:
    """Network function object for NSDs."""

    # TODO: Change publisher commment
    publisher: str = field(
        metadata={"comment": "The name of the existing publisher for the NSD."}
    )
    publisher_resource_group: str = field(
        metadata={"comment:": "The resource group that the publisher is hosted in."}
    )
    name: str = field(
        metadata={
            "comment:": "The name of the existing Network Function Definition Group to deploy using this NSD."
        }
    )
    version: str = field(
        metadata={
            "comment": (
                "The version of the existing Network Function Definition to base this NSD on.\n "
                "This NSD will be able to deploy any NFDV with deployment parameters"
                " compatible with this version."
            )
        }
    )

    publisher_offering_location: str = field(
        metadata={"comment": "The region that the NFDV is published to."}
    )
    type: str = field(
        metadata={
            "comment:": "Type of Network Function. Valid values are 'cnf' or 'vnf'."
        }
    )
    multiple_instances: str = field(
        metadata={
            "comment:": (
                "Set to true or false. Whether the NSD should allow arbitrary numbers of this type of NF. "
                "If false only a single instance will be allowed. Only supported on VNFs, must be set to false on CNFs."
            )
        }
    )


@dataclass
class NetworkFunctionConfig:
    """Network function object for NSDs."""

    resource_element_type: str = field(
        metadata={"comment": "Type of Resource Element. Either NF or ArmTemplate"}
    )
    properties: NetworkFunctionPropertiesConfig = field()


@dataclass
class ArmTemplateConfig:
    """Configuration for RET."""

    resource_element_type: str = field(
        metadata={"comment": "Type of Resource Element. Either NF or ArmTemplate"}
    )
    # Jordan: look up how to do this properly, Union?
    properties: ArmTemplatePropertiesConfig = field(
        metadata={"comment": "Properties of the Resource Element."}
    )


@dataclass
class OnboardingNSDInputConfig(OnboardingBaseInputConfig):
    """Input configuration for onboarding NSDs."""

    nsd_name: str = field(
        metadata={
            "comment": (
                "Network Service Design (NSD) name. "
                "This is the collection of Network Service Design Versions. Will be created if it does not exist."
            )
        }
    )
    nsd_version: str = field(
        metadata={
            "comment:": "Version of the NSD to be created. This should be in the format A.B.C"
        }
    )
    nsdv_description: str = field(
        metadata={
            "comment": "Description of the Network Service Design Version (NSDV)."
        }
    )

    # TODO: Add detailed comment for this
    resource_element_templates: [NetworkFunctionConfig, ArmTemplateConfig] = field(
        metadata={"comment": "List of Resource Element Templates."}
    )
