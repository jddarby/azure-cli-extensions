# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "blueprint assignment create",
    is_preview=True,
)
class Create(AAZCommand):
    """Create a blueprint assignment.

    :example: Assignment with system-assigned managed identity
        az blueprint assignment create --subscription MySubscription --name MyBlueprintAssignment --location eastus --identity-type SystemAssigned --description "Enforce pre-defined MyBlueprint to this subscription." --blueprint-version "/providers/Microsoft.Management/managementGroups/ContosoOnlineGroup/providers/Microsoft.Blueprint/blueprints/MyBlueprint/versions/v2" --resource-group-value artifact_name=rg-art-1 name=rg1 location=westus --resource-group-value artifact_name=rg-art-2 name=rg2 location=eastus --parameters "path/to/parameter/file"

    :example: Assignment with user-assigned managed identity
        az lueprint assignment create --subscription MySubscription --name MyBlueprintAssignment --location eastus --identity-type UserAssigned --user-assigned-identity "/subscriptions/00000000-0000-0000-0000-000000000000 /resourcegroups/myResourceGroup/providers/Microsoft.ManagedIdentity/userAssignedIdentities/m yIdentity" --description "Enforce pre-defined MyBlueprint to this subscription." --blueprint-version "/providers/Microsoft.Management/managementGroups/ContosoOnlineGroup/providers/Microsoft.Blueprint/blueprints/MyBlueprint/versions/v2" --resource-group-value artifact_name=rg-art-1 name=rg1 location=eastus --parameters "path/to/parameter/file"
    """

    _aaz_info = {
        "version": "2018-11-01-preview",
        "resources": [
            ["mgmt-plane", "/{resourcescope}/providers/microsoft.blueprint/blueprintassignments/{}", "2018-11-01-preview"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.name = AAZStrArg(
            options=["-n", "--name"],
            help="Name of the blueprint assignment.",
            required=True,
        )
        _args_schema.resource_scope = AAZStrArg(
            options=["--resource-scope"],
            help="The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').",
            required=True,
        )

        # define Arg Group "Assignment"

        _args_schema = cls._args_schema
        _args_schema.identity = AAZObjectArg(
            options=["--identity"],
            arg_group="Assignment",
            help="Managed identity for this blueprint assignment.",
            required=True,
        )
        _args_schema.location = AAZResourceLocationArg(
            arg_group="Assignment",
            help="The location of this blueprint assignment.",
            required=True,
        )

        identity = cls._args_schema.identity
        identity.principal_id = AAZStrArg(
            options=["principal-id"],
            help="Azure Active Directory principal ID associated with this Identity.",
        )
        identity.tenant_id = AAZStrArg(
            options=["tenant-id"],
            help="ID of the Azure Active Directory.",
        )
        identity.type = AAZStrArg(
            options=["type"],
            help="Type of the managed identity.",
            required=True,
            enum={"None": "None", "SystemAssigned": "SystemAssigned", "UserAssigned": "UserAssigned"},
        )
        identity.user_assigned_identities = AAZDictArg(
            options=["user-assigned-identities"],
            help="The list of user-assigned managed identities associated with the resource. Key is the Azure resource Id of the managed identity.",
        )

        user_assigned_identities = cls._args_schema.identity.user_assigned_identities
        user_assigned_identities.Element = AAZObjectArg()

        _element = cls._args_schema.identity.user_assigned_identities.Element
        _element.client_id = AAZStrArg(
            options=["client-id"],
            help="Client App Id associated with this identity.",
        )
        _element.principal_id = AAZStrArg(
            options=["principal-id"],
            help="Azure Active Directory principal ID associated with this Identity.",
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.blueprint_id = AAZStrArg(
            options=["--blueprint-id"],
            arg_group="Properties",
            help="ID of the published version of a blueprint definition.",
        )
        _args_schema.description = AAZStrArg(
            options=["--description"],
            arg_group="Properties",
            help="Multi-line explain this resource.",
            fmt=AAZStrArgFormat(
                max_length=500,
            ),
        )
        _args_schema.display_name = AAZStrArg(
            options=["--display-name"],
            arg_group="Properties",
            help="One-liner string explain this resource.",
            fmt=AAZStrArgFormat(
                max_length=256,
            ),
        )
        _args_schema.locks = AAZObjectArg(
            options=["--locks"],
            arg_group="Properties",
            help="Defines how resources deployed by a blueprint assignment are locked.",
        )
        _args_schema.parameters = AAZDictArg(
            options=["--parameters"],
            arg_group="Properties",
            help="Blueprint assignment parameter values.",
            required=True,
        )
        _args_schema.resource_groups = AAZDictArg(
            options=["--resource-groups"],
            arg_group="Properties",
            help="Names and locations of resource group placeholders.",
            required=True,
        )
        _args_schema.scope = AAZStrArg(
            options=["--scope"],
            arg_group="Properties",
            help="The target subscription scope of the blueprint assignment (format: '/subscriptions/{subscriptionId}'). For management group level assignments, the property is required.",
        )

        locks = cls._args_schema.locks
        locks.excluded_actions = AAZListArg(
            options=["excluded-actions"],
            help="List of management operations that are excluded from blueprint locks. Up to 200 actions are permitted. If the lock mode is set to 'AllResourcesReadOnly', then the following actions are automatically appended to 'excludedActions': '*/read', 'Microsoft.Network/virtualNetworks/subnets/join/action' and 'Microsoft.Authorization/locks/delete'. If the lock mode is set to 'AllResourcesDoNotDelete', then the following actions are automatically appended to 'excludedActions': 'Microsoft.Authorization/locks/delete'. Duplicate actions will get removed.",
        )
        locks.excluded_principals = AAZListArg(
            options=["excluded-principals"],
            help="List of AAD principals excluded from blueprint locks. Up to 5 principals are permitted.",
        )
        locks.mode = AAZStrArg(
            options=["mode"],
            help="Lock mode.",
            enum={"AllResourcesDoNotDelete": "AllResourcesDoNotDelete", "AllResourcesReadOnly": "AllResourcesReadOnly", "None": "None"},
        )

        excluded_actions = cls._args_schema.locks.excluded_actions
        excluded_actions.Element = AAZStrArg()

        excluded_principals = cls._args_schema.locks.excluded_principals
        excluded_principals.Element = AAZStrArg()

        parameters = cls._args_schema.parameters
        parameters.Element = AAZObjectArg()

        _element = cls._args_schema.parameters.Element
        _element.reference = AAZObjectArg(
            options=["reference"],
            help="Parameter value as reference type.",
        )

        reference = cls._args_schema.parameters.Element.reference
        reference.key_vault = AAZObjectArg(
            options=["key-vault"],
            help="Specifies the reference to a given Azure Key Vault.",
            required=True,
        )
        reference.secret_name = AAZStrArg(
            options=["secret-name"],
            help="Name of the secret.",
            required=True,
        )
        reference.secret_version = AAZStrArg(
            options=["secret-version"],
            help="The version of the secret to use. If left blank, the latest version of the secret is used.",
        )

        key_vault = cls._args_schema.parameters.Element.reference.key_vault
        key_vault.id = AAZStrArg(
            options=["id"],
            help="Azure resource ID of the Key Vault.",
            required=True,
        )

        resource_groups = cls._args_schema.resource_groups
        resource_groups.Element = AAZObjectArg()

        _element = cls._args_schema.resource_groups.Element
        _element.location = AAZStrArg(
            options=["location"],
            help="Location of the resource group.",
        )
        _element.name = AAZStrArg(
            options=["name"],
            help="Name of the resource group.",
            fmt=AAZStrArgFormat(
                max_length=90,
                min_length=1,
            ),
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.AssignmentsCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class AssignmentsCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [201]:
                return self.on_201(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/{resourceScope}/providers/Microsoft.Blueprint/blueprintAssignments/{assignmentName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "assignmentName", self.ctx.args.name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceScope", self.ctx.args.resource_scope,
                    skip_quote=True,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2018-11-01-preview",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType,
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("identity", AAZObjectType, ".identity", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("location", AAZStrType, ".location", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})

            identity = _builder.get(".identity")
            if identity is not None:
                identity.set_prop("principalId", AAZStrType, ".principal_id")
                identity.set_prop("tenantId", AAZStrType, ".tenant_id")
                identity.set_prop("type", AAZStrType, ".type", typ_kwargs={"flags": {"required": True}})
                identity.set_prop("userAssignedIdentities", AAZDictType, ".user_assigned_identities")

            user_assigned_identities = _builder.get(".identity.userAssignedIdentities")
            if user_assigned_identities is not None:
                user_assigned_identities.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".identity.userAssignedIdentities{}")
            if _elements is not None:
                _elements.set_prop("clientId", AAZStrType, ".client_id")
                _elements.set_prop("principalId", AAZStrType, ".principal_id")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("blueprintId", AAZStrType, ".blueprint_id")
                properties.set_prop("description", AAZStrType, ".description")
                properties.set_prop("displayName", AAZStrType, ".display_name")
                properties.set_prop("locks", AAZObjectType, ".locks")
                properties.set_prop("parameters", AAZDictType, ".parameters", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("resourceGroups", AAZDictType, ".resource_groups", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("scope", AAZStrType, ".scope")

            locks = _builder.get(".properties.locks")
            if locks is not None:
                locks.set_prop("excludedActions", AAZListType, ".excluded_actions")
                locks.set_prop("excludedPrincipals", AAZListType, ".excluded_principals")
                locks.set_prop("mode", AAZStrType, ".mode")

            excluded_actions = _builder.get(".properties.locks.excludedActions")
            if excluded_actions is not None:
                excluded_actions.set_elements(AAZStrType, ".")

            excluded_principals = _builder.get(".properties.locks.excludedPrincipals")
            if excluded_principals is not None:
                excluded_principals.set_elements(AAZStrType, ".")

            parameters = _builder.get(".properties.parameters")
            if parameters is not None:
                parameters.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.parameters{}")
            if _elements is not None:
                _elements.set_prop("reference", AAZObjectType, ".reference")

            reference = _builder.get(".properties.parameters{}.reference")
            if reference is not None:
                reference.set_prop("keyVault", AAZObjectType, ".key_vault", typ_kwargs={"flags": {"required": True}})
                reference.set_prop("secretName", AAZStrType, ".secret_name", typ_kwargs={"flags": {"required": True}})
                reference.set_prop("secretVersion", AAZStrType, ".secret_version")

            key_vault = _builder.get(".properties.parameters{}.reference.keyVault")
            if key_vault is not None:
                key_vault.set_prop("id", AAZStrType, ".id", typ_kwargs={"flags": {"required": True}})

            resource_groups = _builder.get(".properties.resourceGroups")
            if resource_groups is not None:
                resource_groups.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.resourceGroups{}")
            if _elements is not None:
                _elements.set_prop("location", AAZStrType, ".location")
                _elements.set_prop("name", AAZStrType, ".name")

            return self.serialize_content(_content_value)

        def on_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_201
            )

        _schema_on_201 = None

        @classmethod
        def _build_schema_on_201(cls):
            if cls._schema_on_201 is not None:
                return cls._schema_on_201

            cls._schema_on_201 = AAZObjectType()

            _schema_on_201 = cls._schema_on_201
            _schema_on_201.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_201.identity = AAZObjectType(
                flags={"required": True},
            )
            _schema_on_201.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_201.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_201.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_201.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_201.identity
            identity.principal_id = AAZStrType(
                serialized_name="principalId",
            )
            identity.tenant_id = AAZStrType(
                serialized_name="tenantId",
            )
            identity.type = AAZStrType(
                flags={"required": True},
            )
            identity.user_assigned_identities = AAZDictType(
                serialized_name="userAssignedIdentities",
            )

            user_assigned_identities = cls._schema_on_201.identity.user_assigned_identities
            user_assigned_identities.Element = AAZObjectType()

            _element = cls._schema_on_201.identity.user_assigned_identities.Element
            _element.client_id = AAZStrType(
                serialized_name="clientId",
            )
            _element.principal_id = AAZStrType(
                serialized_name="principalId",
            )

            properties = cls._schema_on_201.properties
            properties.blueprint_id = AAZStrType(
                serialized_name="blueprintId",
            )
            properties.description = AAZStrType()
            properties.display_name = AAZStrType(
                serialized_name="displayName",
            )
            properties.locks = AAZObjectType()
            properties.parameters = AAZDictType(
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.resource_groups = AAZDictType(
                serialized_name="resourceGroups",
                flags={"required": True},
            )
            properties.scope = AAZStrType()
            properties.status = AAZObjectType()

            locks = cls._schema_on_201.properties.locks
            locks.excluded_actions = AAZListType(
                serialized_name="excludedActions",
            )
            locks.excluded_principals = AAZListType(
                serialized_name="excludedPrincipals",
            )
            locks.mode = AAZStrType()

            excluded_actions = cls._schema_on_201.properties.locks.excluded_actions
            excluded_actions.Element = AAZStrType()

            excluded_principals = cls._schema_on_201.properties.locks.excluded_principals
            excluded_principals.Element = AAZStrType()

            parameters = cls._schema_on_201.properties.parameters
            parameters.Element = AAZObjectType()

            _element = cls._schema_on_201.properties.parameters.Element
            _element.reference = AAZObjectType()

            reference = cls._schema_on_201.properties.parameters.Element.reference
            reference.key_vault = AAZObjectType(
                serialized_name="keyVault",
                flags={"required": True},
            )
            reference.secret_name = AAZStrType(
                serialized_name="secretName",
                flags={"required": True},
            )
            reference.secret_version = AAZStrType(
                serialized_name="secretVersion",
            )

            key_vault = cls._schema_on_201.properties.parameters.Element.reference.key_vault
            key_vault.id = AAZStrType(
                flags={"required": True},
            )

            resource_groups = cls._schema_on_201.properties.resource_groups
            resource_groups.Element = AAZObjectType()

            _element = cls._schema_on_201.properties.resource_groups.Element
            _element.location = AAZStrType()
            _element.name = AAZStrType()

            status = cls._schema_on_201.properties.status
            status.last_modified = AAZStrType(
                serialized_name="lastModified",
                flags={"read_only": True},
            )
            status.managed_resources = AAZListType(
                serialized_name="managedResources",
                flags={"read_only": True},
            )
            status.time_created = AAZStrType(
                serialized_name="timeCreated",
                flags={"read_only": True},
            )

            managed_resources = cls._schema_on_201.properties.status.managed_resources
            managed_resources.Element = AAZStrType()

            return cls._schema_on_201


class _CreateHelper:
    """Helper class for Create"""


__all__ = ["Create"]
