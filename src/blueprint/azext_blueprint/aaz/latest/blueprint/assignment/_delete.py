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
    "blueprint assignment delete",
    is_preview=True,
    confirmation="Are you sure you want to perform this operation?",
)
class Delete(AAZCommand):
    """Delete a blueprint assignment.

    :example: Delete an assignment
        az blueprint assignment delete --subscription MySubscription --name MyBlueprintAssignment
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
        _args_schema.delete_behavior = AAZStrArg(
            options=["--delete-behavior"],
            help="When deleteBehavior=all, the resources that were created by the blueprint assignment will be deleted.",
            enum={"all": "all", "none": "none"},
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.AssignmentsDelete(ctx=self.ctx)()
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

    class AssignmentsDelete(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.on_202(session)
            if session.http_response.status_code in [204]:
                return self.on_204(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/{resourceScope}/providers/Microsoft.Blueprint/blueprintAssignments/{assignmentName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "DELETE"

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
                    "deleteBehavior", self.ctx.args.delete_behavior,
                ),
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
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_202(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_202
            )

        _schema_on_202 = None

        @classmethod
        def _build_schema_on_202(cls):
            if cls._schema_on_202 is not None:
                return cls._schema_on_202

            cls._schema_on_202 = AAZObjectType()

            _schema_on_202 = cls._schema_on_202
            _schema_on_202.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_202.identity = AAZObjectType(
                flags={"required": True},
            )
            _schema_on_202.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_202.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_202.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_202.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_202.identity
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

            user_assigned_identities = cls._schema_on_202.identity.user_assigned_identities
            user_assigned_identities.Element = AAZObjectType()

            _element = cls._schema_on_202.identity.user_assigned_identities.Element
            _element.client_id = AAZStrType(
                serialized_name="clientId",
            )
            _element.principal_id = AAZStrType(
                serialized_name="principalId",
            )

            properties = cls._schema_on_202.properties
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

            locks = cls._schema_on_202.properties.locks
            locks.excluded_actions = AAZListType(
                serialized_name="excludedActions",
            )
            locks.excluded_principals = AAZListType(
                serialized_name="excludedPrincipals",
            )
            locks.mode = AAZStrType()

            excluded_actions = cls._schema_on_202.properties.locks.excluded_actions
            excluded_actions.Element = AAZStrType()

            excluded_principals = cls._schema_on_202.properties.locks.excluded_principals
            excluded_principals.Element = AAZStrType()

            parameters = cls._schema_on_202.properties.parameters
            parameters.Element = AAZObjectType()

            _element = cls._schema_on_202.properties.parameters.Element
            _element.reference = AAZObjectType()

            reference = cls._schema_on_202.properties.parameters.Element.reference
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

            key_vault = cls._schema_on_202.properties.parameters.Element.reference.key_vault
            key_vault.id = AAZStrType(
                flags={"required": True},
            )

            resource_groups = cls._schema_on_202.properties.resource_groups
            resource_groups.Element = AAZObjectType()

            _element = cls._schema_on_202.properties.resource_groups.Element
            _element.location = AAZStrType()
            _element.name = AAZStrType()

            status = cls._schema_on_202.properties.status
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

            managed_resources = cls._schema_on_202.properties.status.managed_resources
            managed_resources.Element = AAZStrType()

            return cls._schema_on_202

        def on_204(self, session):
            pass


class _DeleteHelper:
    """Helper class for Delete"""


__all__ = ["Delete"]
