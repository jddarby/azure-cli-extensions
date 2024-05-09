# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field

from azure.cli.core.azclierror import ValidationError

@dataclass
class PreexistingCgv:
    name: str = field(
        default="",
        metadata={
            "comment": (
                "Name of the cgv."
            )
        },
    )
    resource_group: str = field(
        default="",
        metadata={
            "comment": (
                "If left blank, resource group is assumed to be same as operator_resource_group"
            )
        },
    )
    configuration_group_schema_name: str = field(
        default="",
        metadata={
            "comment": (
                "Name of the configuration group schema."
            )
        },
    )

    def validate(self):
        """Validate the configuration."""
        if not self.name:
            raise ValidationError("CGV name must be set")
        if not self.configuration_group_schema_name:
            raise ValidationError("Configuration group schema name must be set")

@dataclass
class NsdReference:
    publisher_name: str = field(
        default="",
        metadata={
            "comment": (
                "Name of the Publisher resource you want your definition published to.\n"
                "Will be created if it does not exist."
            )
        },
    )
    publisher_resource_group_name: str = field(
        default="",
        metadata={
            "comment": (
                "Resource group for the Publisher resource.\n"
                "Will be created if it does not exist."
            )
        },
    )
    nsd_name: str = field(
        default="",
        metadata={
            "comment": (
                "Network Service Design (NSD) name. "
                "This is the collection of Network Service Design Versions. Will be created if it does not exist."
            )
        },
    )
    nsd_version: str = field(
        default="",
        metadata={
            "comment": "Version of the NSD to be created. This should be in the format A.B.C"
        },
    )

    def validate(self):
        """Validate the configuration."""
        if not self.publisher_name:
            raise ValidationError("Publisher name must be set")
        if not self.publisher_resource_group_name:
            raise ValidationError("Publisher resource group name must be set")
        if not self.nsd_name:
            raise ValidationError("NSD group name must be set")
        if not self.nsd_version:
            raise ValidationError("NSD version must be set")

@dataclass
class OnboardingSNSInputConfig(ABC):
    """Base input configuration for onboarding commands."""

    location: str = field(
        default="",
        metadata={
            "comment": "Azure location to use when creating resources e.g uksouth"
        },
    )
    operator_resource_group_name: str = field(
        default="",
        metadata={
            "comment": (
                "Resource group for the operator resources.\n"
                "Will be created if it does not exist."
            )
        },
    )
    sns_name: str = field(
        default="",
        metadata={
            "comment": "Name of the sns."}
    )
    site_name: str = field(
        default="",
        metadata={
            "comment": "Name of the site."}
    )
    nsd_reference: NsdReference = (
        field(
            default_factory=NsdReference,
            metadata={
                "comment": (
                    "Reference to the NSD to be used for the SNS."
                )
            },
        )
    )
    # preexisting_cgvs: List[PreexistingCgv] = field(default_factory=list)# # TODO: Add detailed comment for this

    def validate(self):
        """Validate the configuration."""
        if not self.location:
            raise ValidationError("Location must be set")
        if not self.operator_resource_group_name:
            raise ValidationError("Operator resource group name must be set")
        if not self.site_name:
            raise ValidationError("Site name must be set")
        if not self.nsd_reference:
            raise ValidationError("NSD reference must be set")
    
    def __post_init__(self):
        if self.nsd_reference and isinstance(self.nsd_reference, dict):
            self.nsd_reference = NsdReference(**self.nsd_reference)