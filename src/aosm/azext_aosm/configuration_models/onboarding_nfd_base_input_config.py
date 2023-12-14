# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from azure.cli.core.azclierror import ValidationError
from azext_aosm.configuration_models.onboarding_base_input_config import (
    OnboardingBaseInputConfig,
)


@dataclass
class OnboardingNFDBaseInputConfig(OnboardingBaseInputConfig):
    """Common input configuration for onboarding NFDs."""

    nf_name: str = field(default="", metadata={"comment": "Name of NF definition."})
    version: str = field(
        default="",
        metadata={"comment": "Version of the NF definition in A.B.C format."},
    )

    def validate(self):
        """Validate the configuration."""
        super().validate()
        if not self.nf_name:
            raise ValidationError("nf_name must be set")
        if not self.version:
            raise ValidationError("version must be set")
