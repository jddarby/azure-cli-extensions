# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC
from dataclasses import dataclass, field


@dataclass
class OnboardingBaseInputConfig(ABC):
    """Base input configuration for onboarding commands."""

    location: str = field(
        metadata={"comment": "Azure location to use when creating resources."}
    )
    publisher_name: str = field(
        metadata={
            "comment:": (
                "Name of the Publisher resource you want your definition published to. "
                "Will be created if it does not exist."
            )
        }
    )
    publisher_resource_group_name: str = field(
        metadata={
            "comment": (
                "Optional. Resource group for the Publisher resource. "
                "Will be created if it does not exist (with a default name if none is supplied)."
            )
        }
    )
    acr_artifact_store_name: str = field(
        metadata={
            "comment": (
                "Optional. Name of the ACR Artifact Store resource. "
                "Will be created if it does not exist (with a default name if none is supplied)."
            )
        }
    )
