# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import annotations
from azure.cli.core.azclierror import ValidationError
from dataclasses import dataclass, field
from .onboarding_nfd_base_input_config import OnboardingNFDBaseInputConfig
from .common_input import ArmTemplatePropertiesConfig


@dataclass
class VhdImageConfig:
    """Configuration for a VHD image."""

    artifact_name: str = field(
        default="", metadata={"comment": "Optional. Name of the artifact."}
    )
    version: str = field(
        default="",
        metadata={"comment": "Version of the artifact in A-B-C format."}
    )
    file_path: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. File path of the artifact you wish to upload from your local disk. "
                "Delete if not required.\nRelative paths are relative to the configuration file. "
                "On Windows escape any backslash with another backslash."
            )
        }
    )
    blob_sas_url: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. SAS URL of the blob artifact you wish to copy to your Artifact Store.\n"
                "Delete if not required. "
                "On Windows escape any backslash with another backslash."
            )
        }
    )
    image_disk_size_GB: str | None = field(
        default="",
        metadata={
            "comment": (
                "Optional. Specifies the size of empty data disks in gigabytes.\n"
                "This value cannot be larger than 1023 GB. Delete if not required."
            )
        }
    )
    image_hyper_v_generation: str | None = field(
        default="",
        metadata={
            "comment": (
                "Optional. Specifies the HyperVGenerationType of the VirtualMachine created from the image.\n"
                "Valid values are V1 and V2. V1 is the default if not specified. Delete if not required."
            )
        }
    )
    image_api_version: str | None = field(
        default="",
        metadata={
            "comment": (
                "Optional. The ARM API version used to create the Microsoft.Compute/images resource.\n"
                "Delete if not required."
            )
        }
    )
    def validate(self):
        """Validate the configuration."""
        if not self.version:
            raise ValidationError("Artifact version must be set")
        if "." not in self.version or "-" in self.version:
            raise ValidationError(
                "Config validation error. VHD image artifact version should be in"
                " format A.B.C"
            )
        if self.blob_sas_url and self.file_path:
            raise ValidationError("Only one of file_path or blob_sas_url may be set for vhd.")
        if not (self.blob_sas_url or self.file_path):
            raise ValidationError("One of file_path or sas_blob_url must be set for vhd.")


@dataclass
class OnboardingVNFInputConfig(OnboardingNFDBaseInputConfig):
    """Input configuration for onboarding VNFs."""

    blob_artifact_store_name: str | None = field(
        default="",
        metadata={
            "comment": (
                "Optional. Name of the storage account Artifact Store resource. \n"
                "Will be created if it does not exist (with a default name if none is supplied)."
            )
        }
    )
    image_name_parameter: str = field(
        default="",
        metadata={
            "comment": (
                "The parameter name in the VM ARM template which "
                "specifies the name of the image to use for the VM."
            )
        }
    )

    # TODO: Add better comments
    arm_templates: [ArmTemplatePropertiesConfig] = field(
        default_factory=lambda: [ArmTemplatePropertiesConfig()],
        metadata={"comment": "ARM template configuration."},
    )

    vhd: [VhdImageConfig] = field(
        default_factory=lambda: [VhdImageConfig()],
        metadata={"comment": "VHD image configuration."})

    def __post_init__(self):
        arm_list = []
        for arm_template in self.arm_templates:
            if arm_template and isinstance(arm_template, dict):
                arm_list.append(ArmTemplatePropertiesConfig(**arm_template))
            else:
                arm_list.append(arm_template)
        self.arm_templates = arm_list
        
        vhd_list = []
        for vhd in self.vhd:
            if vhd and isinstance(vhd, dict):
                vhd_list.append(VhdImageConfig(**vhd))
            else:
                vhd_list.append(vhd)
        self.vhd = vhd_list

    def validate(self):
        """Validate the configuration."""
        super().validate()

        if not self.image_name_parameter:
            raise ValidationError("image_name_parameter must be set")
        if not self.arm_templates:
            raise ValidationError("arm_template must be set")
        if not self.vhd:
            raise ValidationError("vhd must be set")
        if not self.arm_templates:
            raise ValidationError("You must include at least one arm template")
        for arm_template in self.arm_templates:
            arm_template.validate()
        for vhd in self.vhd:
            vhd.validate()