# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass, field

from azure.cli.core.azclierror import ValidationError


@dataclass
class SiteNetworkServicePropertiesConfig:
    """SNS Object."""
    location: str = field(
        default="",
        metadata={
            "comment": "Azure location to use when creating resources e.g uksouth"
        },
    )
    operator_resource_group: str = field(
        default="",
        metadata={"comment": "The resource group that the operator resources will be hosted in."},
    )
    site_name: str = field(
        default="",
        metadata={"comment": "Name of the site."},
    )
    nsd_reference: "NSDVReferenceConfig" = (
        field(
            default_factory=lambda: [NSDVReferenceConfig()],
            metadata={
                "comment": (
                   "Information regarding NSDV to be used in SNS."
                )
            },
        )
    )

    def validate(self):
        """Validate the configuration."""
        if not self.location:
            raise ValidationError("Location must be set")
        if not self.operator_resource_group:
            raise ValidationError("Operator resource group name must be set")
        if not self.site_name:
            raise ValidationError(
                "site name must be set"
            )


@dataclass
class NSDVReferenceConfig:
    """SNS Object."""
    publisher_name: str = field(
        default="",
        metadata={
            "comment": "Name of the Publisher resource where Network Service Design resource to be used in SNS exists"
        },
    )
    publisher_resource_group: str = field(
        default="",
        metadata={"comment": "The resource group that the publisher NSDV is hosted in. "},
    )
    nsd_name: str = field(
        default="",
        metadata={"comment": "Network Service Design"
                  "(NSD) to be used from the publisher. This is the collection of Network Service Design Versions. "},
    )
    nsd_version: str = field(
        default="",
        metadata={"comment": "Version of the NSD to be used which is in the format A.B.C "},
    )

    def validate(self):
        """Validate the configuration."""
        if not self.publisher_name:
            raise ValidationError("Publisher Name must be set")
        if not self.publisher_resource_group:
            raise ValidationError("Publisher Resource Group must be set")
        if not self.nsd_name:
            raise ValidationError(
                "NSD Name must be set"
            )
        if not self.nsd_version:
            raise ValidationError(
                "NSD Version must be set"
            )
