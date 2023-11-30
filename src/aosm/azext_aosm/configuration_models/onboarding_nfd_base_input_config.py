# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

from .onboarding_base_input_config import OnboardingBaseInputConfig


@dataclass
class OnboardingNFDBaseInputConfig(OnboardingBaseInputConfig):
    """Common input configuration for onboarding NFDs."""
    nf_name: str = field(
        default="",
        metadata={"comment": "Name of NF definition."}
    )
    version: str = field(
        default="",
        metadata={
            "comment:": "Version of the NF definition in A.B.C format."
        }
    )
