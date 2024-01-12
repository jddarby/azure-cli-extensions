# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseCommonParametersConfig(ABC):
    """Base common parameters configuration."""

    location: str
    publisherName: str
    publisherResourceGroupName: str
    acrArtifactStoreName: str
    acrManifestName: str


@dataclass
class NFDCommonParametersConfig(BaseCommonParametersConfig):
    """Common parameters configuration for NFs."""
    nfDefinitionGroup: str
    nfDefinitionVersion: str


@dataclass
class VNFCommonParametersConfig(NFDCommonParametersConfig):
    """Common parameters configuration for VNFs."""

    saArtifactStoreName: str
    saManifestName: str


@dataclass
class CNFCommonParametersConfig(NFDCommonParametersConfig):
    """Common parameters configuration for VNFs."""


@dataclass
class NSDCommonParametersConfig(BaseCommonParametersConfig):
    """ Common parameters configuration for NSDs"""
