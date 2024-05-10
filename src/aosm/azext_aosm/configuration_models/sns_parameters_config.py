# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class NSDReference:
    publisherName: str
    publisherResourceGroupName: str
    nsdName: str
    nsdVersion: str

@dataclass(frozen=True)
class SNSCommonParametersConfig(ABC):
    """Base common parameters configuration."""

    location: str
    operatorResourceGroupName: str
    siteName: str
    nsdReference: NSDReference
    snsName: Optional[str] = None

