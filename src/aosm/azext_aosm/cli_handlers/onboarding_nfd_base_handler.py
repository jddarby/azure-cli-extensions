# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.azclierror import (
    ValidationError
)
from .onboarding_base_handler import OnboardingBaseCLIHandler


class OnboardingNFDBaseCLIHandler(OnboardingBaseCLIHandler):
    """Abstract base class for NFD CLI handlers."""

    # def validate(self):
    #     """Validate the configuration."""
    #     if not self.config.nf_name:
    #         raise ValidationError("nf_name must be set")
    #     if not self.config.version:
    #         raise ValidationError("version must be set")
    def build_base_bicep(self):
        # TODO: Implement
        pass
