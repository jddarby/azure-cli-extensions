# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from abc import ABC
from dataclasses import dataclass, field


@dataclass
class OnboardingBaseInputConfig(ABC):
    """Base input configuration for onboarding commands."""
    location: str = field(metadata={"comment": "The location of resources."})
    # TODO: Add more fields here as needed.
    # etc.
