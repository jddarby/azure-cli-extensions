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
    "devcenter admin catalog update",
)
class Update(AAZCommand):
    """Update a catalog.

    :example: Update
        az devcenter admin catalog update --git-hub path="/environments" --name "CentralCatalog" --dev-center-name "Contoso" --resource-group "rg1"
    """

    _aaz_info = {
        "version": "2023-06-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.devcenter/devcenters/{}/catalogs/{}", "2023-06-01-preview"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    AZ_SUPPORT_GENERIC_UPDATE = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.catalog_name = AAZStrArg(
            options=["-n", "--name", "--catalog-name"],
            help="The name of the catalog.",
            required=True,
            id_part="child_name_1",
        )
        _args_schema.dev_center_name = AAZStrArg(
            options=["-d", "--dev-center", "--dev-center-name"],
            help="The name of the dev center. Use `az configure -d dev-center=<dev_center_name>` to configure a default.",
            required=True,
            id_part="name",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.ado_git = AAZObjectArg(
            options=["--ado-git"],
            arg_group="Properties",
            help="Properties for an Azure DevOps catalog type.",
            nullable=True,
        )
        cls._build_args_git_catalog_update(_args_schema.ado_git)
        _args_schema.git_hub = AAZObjectArg(
            options=["--git-hub"],
            arg_group="Properties",
            help="Properties for a GitHub catalog type.",
            nullable=True,
        )
        cls._build_args_git_catalog_update(_args_schema.git_hub)
        return cls._args_schema

    _args_git_catalog_update = None

    @classmethod
    def _build_args_git_catalog_update(cls, _schema):
        if cls._args_git_catalog_update is not None:
            _schema.branch = cls._args_git_catalog_update.branch
            _schema.path = cls._args_git_catalog_update.path
            _schema.secret_identifier = cls._args_git_catalog_update.secret_identifier
            _schema.uri = cls._args_git_catalog_update.uri
            return

        cls._args_git_catalog_update = AAZObjectArg(
            nullable=True,
        )

        git_catalog_update = cls._args_git_catalog_update
        git_catalog_update.branch = AAZStrArg(
            options=["branch"],
            help="Git branch.",
            nullable=True,
        )
        git_catalog_update.path = AAZStrArg(
            options=["path"],
            help="The folder where the catalog items can be found inside the repository.",
            nullable=True,
        )
        git_catalog_update.secret_identifier = AAZStrArg(
            options=["secret-identifier"],
            help="A reference to the Key Vault secret containing a security token to authenticate to a Git repository.",
            nullable=True,
        )
        git_catalog_update.uri = AAZStrArg(
            options=["uri"],
            help="Git URI.",
            nullable=True,
        )

        _schema.branch = cls._args_git_catalog_update.branch
        _schema.path = cls._args_git_catalog_update.path
        _schema.secret_identifier = cls._args_git_catalog_update.secret_identifier
        _schema.uri = cls._args_git_catalog_update.uri

    def _execute_operations(self):
        self.pre_operations()
        self.CatalogsGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.CatalogsCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    @register_callback
    def pre_instance_update(self, instance):
        pass

    @register_callback
    def post_instance_update(self, instance):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class CatalogsGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevCenter/devcenters/{devCenterName}/catalogs/{catalogName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "catalogName", self.ctx.args.catalog_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "devCenterName", self.ctx.args.dev_center_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-06-01-preview",
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

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _UpdateHelper._build_schema_catalog_read(cls._schema_on_200)

            return cls._schema_on_200

    class CatalogsCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevCenter/devcenters/{devCenterName}/catalogs/{catalogName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "catalogName", self.ctx.args.catalog_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "devCenterName", self.ctx.args.dev_center_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-06-01-preview",
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
                value=self.ctx.vars.instance,
            )

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
            _UpdateHelper._build_schema_catalog_read(cls._schema_on_201)

            return cls._schema_on_201

    class InstanceUpdateByJson(AAZJsonInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance(self.ctx.vars.instance)

        def _update_instance(self, instance):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=instance,
                typ=AAZObjectType
            )
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                _UpdateHelper._build_schema_git_catalog_update(properties.set_prop("adoGit", AAZObjectType, ".ado_git"))
                _UpdateHelper._build_schema_git_catalog_update(properties.set_prop("gitHub", AAZObjectType, ".git_hub"))

            return _instance_value

    class InstanceUpdateByGeneric(AAZGenericInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance_by_generic(
                self.ctx.vars.instance,
                self.ctx.generic_update_args
            )


class _UpdateHelper:
    """Helper class for Update"""

    @classmethod
    def _build_schema_git_catalog_update(cls, _builder):
        if _builder is None:
            return
        _builder.set_prop("branch", AAZStrType, ".branch")
        _builder.set_prop("path", AAZStrType, ".path")
        _builder.set_prop("secretIdentifier", AAZStrType, ".secret_identifier")
        _builder.set_prop("uri", AAZStrType, ".uri")

    _schema_catalog_read = None

    @classmethod
    def _build_schema_catalog_read(cls, _schema):
        if cls._schema_catalog_read is not None:
            _schema.id = cls._schema_catalog_read.id
            _schema.name = cls._schema_catalog_read.name
            _schema.properties = cls._schema_catalog_read.properties
            _schema.system_data = cls._schema_catalog_read.system_data
            _schema.type = cls._schema_catalog_read.type
            return

        cls._schema_catalog_read = _schema_catalog_read = AAZObjectType()

        catalog_read = _schema_catalog_read
        catalog_read.id = AAZStrType(
            flags={"read_only": True},
        )
        catalog_read.name = AAZStrType(
            flags={"read_only": True},
        )
        catalog_read.properties = AAZObjectType(
            flags={"client_flatten": True},
        )
        catalog_read.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        catalog_read.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_catalog_read.properties
        properties.ado_git = AAZObjectType(
            serialized_name="adoGit",
        )
        cls._build_schema_git_catalog_read(properties.ado_git)
        properties.connection_state = AAZStrType(
            serialized_name="connectionState",
            flags={"read_only": True},
        )
        properties.git_hub = AAZObjectType(
            serialized_name="gitHub",
        )
        cls._build_schema_git_catalog_read(properties.git_hub)
        properties.last_connection_time = AAZStrType(
            serialized_name="lastConnectionTime",
            flags={"read_only": True},
        )
        properties.last_sync_time = AAZStrType(
            serialized_name="lastSyncTime",
            flags={"read_only": True},
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.sync_state = AAZStrType(
            serialized_name="syncState",
            flags={"read_only": True},
        )

        system_data = _schema_catalog_read.system_data
        system_data.created_at = AAZStrType(
            serialized_name="createdAt",
        )
        system_data.created_by = AAZStrType(
            serialized_name="createdBy",
        )
        system_data.created_by_type = AAZStrType(
            serialized_name="createdByType",
        )
        system_data.last_modified_at = AAZStrType(
            serialized_name="lastModifiedAt",
        )
        system_data.last_modified_by = AAZStrType(
            serialized_name="lastModifiedBy",
        )
        system_data.last_modified_by_type = AAZStrType(
            serialized_name="lastModifiedByType",
        )

        _schema.id = cls._schema_catalog_read.id
        _schema.name = cls._schema_catalog_read.name
        _schema.properties = cls._schema_catalog_read.properties
        _schema.system_data = cls._schema_catalog_read.system_data
        _schema.type = cls._schema_catalog_read.type

    _schema_git_catalog_read = None

    @classmethod
    def _build_schema_git_catalog_read(cls, _schema):
        if cls._schema_git_catalog_read is not None:
            _schema.branch = cls._schema_git_catalog_read.branch
            _schema.path = cls._schema_git_catalog_read.path
            _schema.secret_identifier = cls._schema_git_catalog_read.secret_identifier
            _schema.uri = cls._schema_git_catalog_read.uri
            return

        cls._schema_git_catalog_read = _schema_git_catalog_read = AAZObjectType()

        git_catalog_read = _schema_git_catalog_read
        git_catalog_read.branch = AAZStrType()
        git_catalog_read.path = AAZStrType()
        git_catalog_read.secret_identifier = AAZStrType(
            serialized_name="secretIdentifier",
        )
        git_catalog_read.uri = AAZStrType()

        _schema.branch = cls._schema_git_catalog_read.branch
        _schema.path = cls._schema_git_catalog_read.path
        _schema.secret_identifier = cls._schema_git_catalog_read.secret_identifier
        _schema.uri = cls._schema_git_catalog_read.uri


__all__ = ["Update"]
