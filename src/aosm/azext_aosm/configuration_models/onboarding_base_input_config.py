# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
from abc import ABC
from dataclasses import dataclass, field
from azure.cli.core.azclierror import (
    # CLIInternalError,
    # InvalidArgumentValueError,
    UnclassifiedUserFault,
    ValidationError
)

@dataclass
class OnboardingBaseInputConfig(ABC):
    """Base input configuration for onboarding commands."""

    location: str = field(
        default="",
        metadata={"comment": "Azure location to use when creating resources."}
    )
    publisher_name: str = field(
        default="",
        metadata={
            "comment": (
                "Name of the Publisher resource you want your definition published to. "
                "Will be created if it does not exist."
            )
        }
    )
    publisher_resource_group_name: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. Resource group for the Publisher resource. "
                "Will be created if it does not exist (with a default name if none is supplied)."
            )
        }
    )
    acr_artifact_store_name: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. Name of the ACR Artifact Store resource. "
                "Will be created if it does not exist (with a default name if none is supplied)."
            )
        }
    )
    
    def validate(self):
        """Validate the configuration."""
        print("in validate")
        if not self.location:
            raise ValidationError("Location must be set")
        if not self.publisher_name:
            raise ValidationError("Publisher name must be set")
        if not self.publisher_resource_group_name:
            raise ValidationError("Publisher resource group name must be set")
        if not self.acr_artifact_store_name:
            raise ValidationError("ACR Artifact Store name must be set")
