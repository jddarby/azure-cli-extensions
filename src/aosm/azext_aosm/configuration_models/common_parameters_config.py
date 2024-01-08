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
    publisher_name: str
    publisher_resource_group_name: str
    acr_artifact_store_name: str
    acr_manifest_name: str


@dataclass
class NFDCommonParametersConfig(BaseCommonParametersConfig):
    """Common parameters configuration for NFs."""
    nf_definition_group: str
    nf_definition_version: str


@dataclass
class VNFCommonParametersConfig(NFDCommonParametersConfig):
    """Common parameters configuration for VNFs."""

    sa_artifact_store_name: str
    sa_manifest_name: str
