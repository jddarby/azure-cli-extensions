# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class ActionType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum. Indicates the action type. "Internal" refers to actions that are for internal only APIs."""

    INTERNAL = "Internal"


class ApplicationEnablement(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The application enablement."""

    UNKNOWN = "Unknown"
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ArtifactManifestState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact manifest state."""

    UNKNOWN = "Unknown"
    UPLOADING = "Uploading"
    UPLOADED = "Uploaded"
    VALIDATING = "Validating"
    VALIDATION_FAILED = "ValidationFailed"
    SUCCEEDED = "Succeeded"


class ArtifactReplicationStrategy(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The replication strategy."""

    UNKNOWN = "Unknown"
    SINGLE_REPLICATION = "SingleReplication"


class ArtifactState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact state."""

    UNKNOWN = "Unknown"
    PREVIEW = "Preview"
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"


class ArtifactStoreType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact store type."""

    UNKNOWN = "Unknown"
    AZURE_CONTAINER_REGISTRY = "AzureContainerRegistry"
    AZURE_STORAGE_ACCOUNT = "AzureStorageAccount"


class ArtifactType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact type."""

    UNKNOWN = "Unknown"
    OCI_ARTIFACT = "OCIArtifact"
    VHD_IMAGE_FILE = "VhdImageFile"
    ARM_TEMPLATE = "ArmTemplate"
    IMAGE_FILE = "ImageFile"


class AzureArcKubernetesArtifactType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact type."""

    UNKNOWN = "Unknown"
    HELM_PACKAGE = "HelmPackage"


class AzureCoreArtifactType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact type."""

    UNKNOWN = "Unknown"
    VHD_IMAGE_FILE = "VhdImageFile"
    ARM_TEMPLATE = "ArmTemplate"


class AzureOperatorNexusArtifactType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The artifact type."""

    UNKNOWN = "Unknown"
    IMAGE_FILE = "ImageFile"
    ARM_TEMPLATE = "ArmTemplate"


class ConfigurationGenerationType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The configuration generation type."""

    UNKNOWN = "Unknown"
    HANDLEBAR_TEMPLATE = "HandlebarTemplate"


class CreatedByType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity that created the resource."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class CredentialType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The credential type."""

    UNKNOWN = "Unknown"
    AZURE_CONTAINER_REGISTRY_SCOPED_TOKEN = "AzureContainerRegistryScopedToken"
    AZURE_STORAGE_ACCOUNT_TOKEN = "AzureStorageAccountToken"


class HttpMethod(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The http method of the request."""

    UNKNOWN = "Unknown"
    POST = "Post"
    PUT = "Put"
    GET = "Get"
    PATCH = "Patch"
    DELETE = "Delete"


class ManagedServiceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of managed service identity (where both SystemAssigned and UserAssigned types are
    allowed).
    """

    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned,UserAssigned"


class NetworkFunctionPublisherArtifactType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Network Function publisher artifact type."""

    UNKNOWN = "Unknown"
    HELM_PACKAGE = "HelmPackage"
    VHD_IMAGE_FILE = "VhdImageFile"
    ARM_TEMPLATE = "ArmTemplate"
    IMAGE_FILE = "ImageFile"


class NetworkFunctionType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The network function type."""

    UNKNOWN = "Unknown"
    VIRTUAL_NETWORK_FUNCTION = "VirtualNetworkFunction"
    CONTAINERIZED_NETWORK_FUNCTION = "ContainerizedNetworkFunction"


class NFVIType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The NFVI type."""

    UNKNOWN = "Unknown"
    AZURE_ARC_KUBERNETES = "AzureArcKubernetes"
    AZURE_CORE = "AzureCore"
    AZURE_OPERATOR_NEXUS = "AzureOperatorNexus"


class Origin(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The intended executor of the operation; as in Resource Based Access Control (RBAC) and audit
    logs UX. Default value is "user,system".
    """

    USER = "user"
    SYSTEM = "system"
    USER_SYSTEM = "user,system"


class PodEventType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of pod event."""

    NORMAL = "Normal"
    WARNING = "Warning"


class PodStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The status of a Pod."""

    UNKNOWN = "Unknown"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    RUNNING = "Running"
    PENDING = "Pending"
    TERMINATING = "Terminating"
    NOT_READY = "NotReady"


class ProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The current provisioning state."""

    UNKNOWN = "Unknown"
    SUCCEEDED = "Succeeded"
    ACCEPTED = "Accepted"
    DELETING = "Deleting"
    FAILED = "Failed"
    CANCELED = "Canceled"
    DELETED = "Deleted"
    CONVERGING = "Converging"


class PublisherScope(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Publisher Scope."""

    UNKNOWN = "Unknown"
    PUBLIC = "Public"
    PRIVATE = "Private"


class SkuName(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Name of this Sku."""

    BASIC = "Basic"
    STANDARD = "Standard"


class SkuTier(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The SKU tier based on the SKU name."""

    BASIC = "Basic"
    STANDARD = "Standard"


class Status(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The component resource deployment status."""

    UNKNOWN = "Unknown"
    DEPLOYED = "Deployed"
    UNINSTALLED = "Uninstalled"
    SUPERSEDED = "Superseded"
    FAILED = "Failed"
    UNINSTALLING = "Uninstalling"
    PENDING_INSTALL = "Pending-Install"
    PENDING_UPGRADE = "Pending-Upgrade"
    PENDING_ROLLBACK = "Pending-Rollback"
    DOWNLOADING = "Downloading"
    INSTALLING = "Installing"
    REINSTALLING = "Reinstalling"
    ROLLINGBACK = "Rollingback"
    UPGRADING = "Upgrading"


class TemplateType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The template type."""

    UNKNOWN = "Unknown"
    ARM_TEMPLATE = "ArmTemplate"


class Type(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The resource element template type."""

    UNKNOWN = "Unknown"
    ARM_RESOURCE_DEFINITION = "ArmResourceDefinition"
    NETWORK_FUNCTION_DEFINITION = "NetworkFunctionDefinition"


class VersionState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The configuration group schema state."""

    UNKNOWN = "Unknown"
    PREVIEW = "Preview"
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"
    VALIDATING = "Validating"
    VALIDATION_FAILED = "ValidationFailed"
