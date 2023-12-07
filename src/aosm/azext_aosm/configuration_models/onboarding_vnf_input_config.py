# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

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
                "Delete if not required. Relative paths are relative to the configuration file. "
                "On Windows escape any backslash with another backslash."
            )
        }
    )
    blob_sas_url: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. SAS URL of the blob artifact you wish to copy to your Artifact Store. "
                "Delete if not required. "
                "On Windows escape any backslash with another backslash."
            )
        }
    )
    image_disk_size_GB: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. Specifies the size of empty data disks in gigabytes. "
                "This value cannot be larger than 1023 GB. Delete if not required."
            )
        }
    )
    image_hyper_v_generation: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. Specifies the HyperVGenerationType of the VirtualMachine created from the image. "
                "Valid values are V1 and V2. V1 is the default if not specified. Delete if not required."
            )
        }
    )
    image_api_version: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. The ARM API version used to create the Microsoft.Compute/images resource. "
                "Delete if not required."
            )
        }
    )


@dataclass
class OnboardingVNFInputConfig(OnboardingNFDBaseInputConfig):
    """Input configuration for onboarding VNFs."""

    blob_artifact_store_name: str = field(
        default="",
        metadata={
            "comment": (
                "Optional. Name of the storage account Artifact Store resource. "
                " Will be created if it does not exist (with a default name if none is supplied)."
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
    arm_template: [ArmTemplatePropertiesConfig] = field(
        default_factory=lambda: [ArmTemplatePropertiesConfig()],
        metadata={"comment": "ARM template configuration."},
    )

    vhd: [VhdImageConfig] = field(
        default_factory=lambda: [VhdImageConfig()],
        metadata={"comment": "VHD image configuration."})
