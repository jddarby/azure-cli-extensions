# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass

# Config is sometimes used as an argument to cached functions. These
# arguments must be hashable, so we need to use frozen dataclasses.
# This is fine because we shouldn't be changing this initial input anyway.
@dataclass(frozen=True)
class BaseCommonParametersConfig(ABC):
    """Base common parameters configuration."""

    location: str
    publisher_name: str
    publisher_resource_group_name: str
    acr_artifact_store_name: str
    acr_manifest_name: str


@dataclass(frozen=True)
class NFDCommonParametersConfig(BaseCommonParametersConfig):
    """Common parameters configuration for NFs."""

    nf_definition_group: str
    nf_definition_version: str


@dataclass(frozen=True)
class VNFCommonParametersConfig(NFDCommonParametersConfig):
    """Common parameters configuration for VNFs."""

    sa_artifact_store_name: str
    sa_manifest_name: str


@dataclass(frozen=True)
class CNFCommonParametersConfig(NFDCommonParametersConfig):
    """Common parameters configuration for VNFs."""


@dataclass(frozen=True)
class NSDCommonParametersConfig(BaseCommonParametersConfig):
    """Common parameters configuration for NSDs."""

    ns_definition_group: str
