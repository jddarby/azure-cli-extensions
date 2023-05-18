# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""Constants used across aosm cli extension."""

# The types of definition that can be generated
VNF = "vnf"
CNF = "cnf"
NSD = "nsd"

# Names of files used in the repo
VNF_DEFINITION_BICEP_SOURCE_TEMPLATE = "vnfdefinition.bicep"
VNF_MANIFEST_BICEP_SOURCE_TEMPLATE = "vnfartifactmanifests.bicep"
VNF_DEFINITION_OUTPUT_BICEP_PREFIX = "nfd-bicep-"
CNF_DEFINITION_JINJA2_SOURCE_TEMPLATE = "cnfdefinition.bicep.j2"
CNF_MANIFEST_JINJA2_SOURCE_TEMPLATE = "cnfartifactmanifest.bicep.j2"
CNF_DEFINITION_BICEP_TEMPLATE = "cnfdefinition.bicep"
CNF_MANIFEST_BICEP_TEMPLATE = "cnfartifactmanifest.bicep"

IMAGE_LINE_REGEX = r"image: \{\{ .Values.(.+?) \}\}/(.+?):(\d+\.\d+\.\d+(-\w+)?(\.\d+)?)"
IMAGE_PULL_SECRET_LINE_REGEX = r"imagePullSecrets: \[name: \{\{ .Values.(.+?) \}\}\]"
DEPLOYMENT_PARAMETER_MAPPING_REGEX = r"\{deployParameters.(.+?)\}"
