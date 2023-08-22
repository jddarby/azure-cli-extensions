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
    "amlfs update",
)
class Update(AAZCommand):
    """Update an AML file system.

    :example: Update amlfs
        az amlfs update -n name -g rg --tags "{tag:test}"
    """

    _aaz_info = {
        "version": "2023-05-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.storagecache/amlfilesystems/{}", "2023-05-01"],
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
        _args_schema.aml_filesystem_name = AAZStrArg(
            options=["-n", "--name", "--aml-filesystem-name"],
            help="Name for the AML file system. Allows alphanumerics, underscores, and hyphens. Start and end with alphanumeric.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^[0-9a-zA-Z][-0-9a-zA-Z_]{0,78}[0-9a-zA-Z]$",
                max_length=80,
                min_length=2,
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "AmlFilesystem"

        _args_schema = cls._args_schema
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="AmlFilesystem",
            help="Resource tags.",
            nullable=True,
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg(
            nullable=True,
        )

        # define Arg Group "EncryptionSettings"

        _args_schema = cls._args_schema
        _args_schema.encryption_setting = AAZObjectArg(
            options=["--encryption-setting"],
            arg_group="EncryptionSettings",
            help="Specifies the location of the encryption key in Key Vault.",
            nullable=True,
        )

        encryption_setting = cls._args_schema.encryption_setting
        encryption_setting.key_url = AAZStrArg(
            options=["key-url"],
            help="The URL referencing a key encryption key in key vault.",
        )
        encryption_setting.source_vault = AAZObjectArg(
            options=["source-vault"],
            help="Describes a resource Id to source key vault.",
        )

        source_vault = cls._args_schema.encryption_setting.source_vault
        source_vault.id = AAZStrArg(
            options=["id"],
            help="Resource Id.",
            nullable=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.maintenance_window = AAZObjectArg(
            options=["--maintenance-window"],
            arg_group="Properties",
            help="Start time of a 30-minute weekly maintenance window.",
        )

        maintenance_window = cls._args_schema.maintenance_window
        maintenance_window.day_of_week = AAZStrArg(
            options=["day-of-week"],
            help="Day of the week on which the maintenance window will occur.",
            nullable=True,
            enum={"Friday": "Friday", "Monday": "Monday", "Saturday": "Saturday", "Sunday": "Sunday", "Thursday": "Thursday", "Tuesday": "Tuesday", "Wednesday": "Wednesday"},
        )
        maintenance_window.time_of_day_utc = AAZStrArg(
            options=["time-of-day-utc"],
            help="The time of day (in UTC) to start the maintenance window.",
            nullable=True,
            fmt=AAZStrArgFormat(
                pattern="^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$",
            ),
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.AmlFilesystemsGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.AmlFilesystemsCreateOrUpdate(ctx=self.ctx)()
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

    class AmlFilesystemsGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorageCache/amlFilesystems/{amlFilesystemName}",
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
                    "amlFilesystemName", self.ctx.args.aml_filesystem_name,
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
                    "api-version", "2023-05-01",
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
            _UpdateHelper._build_schema_aml_filesystem_read(cls._schema_on_200)

            return cls._schema_on_200

    class AmlFilesystemsCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorageCache/amlFilesystems/{amlFilesystemName}",
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
                    "amlFilesystemName", self.ctx.args.aml_filesystem_name,
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
                    "api-version", "2023-05-01",
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

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()
            _UpdateHelper._build_schema_aml_filesystem_read(cls._schema_on_200_201)

            return cls._schema_on_200_201

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
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("encryptionSettings", AAZObjectType)
                properties.set_prop("maintenanceWindow", AAZObjectType, ".maintenance_window", typ_kwargs={"flags": {"required": True}})

            encryption_settings = _builder.get(".properties.encryptionSettings")
            if encryption_settings is not None:
                encryption_settings.set_prop("keyEncryptionKey", AAZObjectType, ".encryption_setting")

            key_encryption_key = _builder.get(".properties.encryptionSettings.keyEncryptionKey")
            if key_encryption_key is not None:
                key_encryption_key.set_prop("keyUrl", AAZStrType, ".key_url", typ_kwargs={"flags": {"required": True}})
                key_encryption_key.set_prop("sourceVault", AAZObjectType, ".source_vault", typ_kwargs={"flags": {"required": True}})

            source_vault = _builder.get(".properties.encryptionSettings.keyEncryptionKey.sourceVault")
            if source_vault is not None:
                source_vault.set_prop("id", AAZStrType, ".id")

            maintenance_window = _builder.get(".properties.maintenanceWindow")
            if maintenance_window is not None:
                maintenance_window.set_prop("dayOfWeek", AAZStrType, ".day_of_week")
                maintenance_window.set_prop("timeOfDayUTC", AAZStrType, ".time_of_day_utc")

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

            return _instance_value

    class InstanceUpdateByGeneric(AAZGenericInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance_by_generic(
                self.ctx.vars.instance,
                self.ctx.generic_update_args
            )


class _UpdateHelper:
    """Helper class for Update"""

    _schema_aml_filesystem_read = None

    @classmethod
    def _build_schema_aml_filesystem_read(cls, _schema):
        if cls._schema_aml_filesystem_read is not None:
            _schema.id = cls._schema_aml_filesystem_read.id
            _schema.identity = cls._schema_aml_filesystem_read.identity
            _schema.location = cls._schema_aml_filesystem_read.location
            _schema.name = cls._schema_aml_filesystem_read.name
            _schema.properties = cls._schema_aml_filesystem_read.properties
            _schema.sku = cls._schema_aml_filesystem_read.sku
            _schema.system_data = cls._schema_aml_filesystem_read.system_data
            _schema.tags = cls._schema_aml_filesystem_read.tags
            _schema.type = cls._schema_aml_filesystem_read.type
            _schema.zones = cls._schema_aml_filesystem_read.zones
            return

        cls._schema_aml_filesystem_read = _schema_aml_filesystem_read = AAZObjectType()

        aml_filesystem_read = _schema_aml_filesystem_read
        aml_filesystem_read.id = AAZStrType(
            flags={"read_only": True},
        )
        aml_filesystem_read.identity = AAZObjectType()
        aml_filesystem_read.location = AAZStrType(
            flags={"required": True},
        )
        aml_filesystem_read.name = AAZStrType(
            flags={"read_only": True},
        )
        aml_filesystem_read.properties = AAZObjectType(
            flags={"client_flatten": True},
        )
        aml_filesystem_read.sku = AAZObjectType()
        aml_filesystem_read.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        aml_filesystem_read.tags = AAZDictType()
        aml_filesystem_read.type = AAZStrType(
            flags={"read_only": True},
        )
        aml_filesystem_read.zones = AAZListType()

        identity = _schema_aml_filesystem_read.identity
        identity.principal_id = AAZStrType(
            serialized_name="principalId",
            flags={"read_only": True},
        )
        identity.tenant_id = AAZStrType(
            serialized_name="tenantId",
            flags={"read_only": True},
        )
        identity.type = AAZStrType()
        identity.user_assigned_identities = AAZDictType(
            serialized_name="userAssignedIdentities",
        )

        user_assigned_identities = _schema_aml_filesystem_read.identity.user_assigned_identities
        user_assigned_identities.Element = AAZObjectType()

        _element = _schema_aml_filesystem_read.identity.user_assigned_identities.Element
        _element.client_id = AAZStrType(
            serialized_name="clientId",
            flags={"read_only": True},
        )
        _element.principal_id = AAZStrType(
            serialized_name="principalId",
            flags={"read_only": True},
        )

        properties = _schema_aml_filesystem_read.properties
        properties.client_info = AAZObjectType(
            serialized_name="clientInfo",
            flags={"read_only": True},
        )
        properties.encryption_settings = AAZObjectType(
            serialized_name="encryptionSettings",
        )
        properties.filesystem_subnet = AAZStrType(
            serialized_name="filesystemSubnet",
            flags={"required": True},
        )
        properties.health = AAZObjectType(
            flags={"read_only": True},
        )
        properties.hsm = AAZObjectType()
        properties.maintenance_window = AAZObjectType(
            serialized_name="maintenanceWindow",
            flags={"required": True},
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.storage_capacity_ti_b = AAZFloatType(
            serialized_name="storageCapacityTiB",
            flags={"required": True},
        )
        properties.throughput_provisioned_m_bps = AAZIntType(
            serialized_name="throughputProvisionedMBps",
            flags={"read_only": True},
        )

        client_info = _schema_aml_filesystem_read.properties.client_info
        client_info.container_storage_interface = AAZObjectType(
            serialized_name="containerStorageInterface",
            flags={"read_only": True},
        )
        client_info.lustre_version = AAZStrType(
            serialized_name="lustreVersion",
            flags={"read_only": True},
        )
        client_info.mgs_address = AAZStrType(
            serialized_name="mgsAddress",
            flags={"read_only": True},
        )
        client_info.mount_command = AAZStrType(
            serialized_name="mountCommand",
            flags={"read_only": True},
        )

        container_storage_interface = _schema_aml_filesystem_read.properties.client_info.container_storage_interface
        container_storage_interface.persistent_volume = AAZStrType(
            serialized_name="persistentVolume",
            flags={"read_only": True},
        )
        container_storage_interface.persistent_volume_claim = AAZStrType(
            serialized_name="persistentVolumeClaim",
            flags={"read_only": True},
        )
        container_storage_interface.storage_class = AAZStrType(
            serialized_name="storageClass",
            flags={"read_only": True},
        )

        encryption_settings = _schema_aml_filesystem_read.properties.encryption_settings
        encryption_settings.key_encryption_key = AAZObjectType(
            serialized_name="keyEncryptionKey",
        )

        key_encryption_key = _schema_aml_filesystem_read.properties.encryption_settings.key_encryption_key
        key_encryption_key.key_url = AAZStrType(
            serialized_name="keyUrl",
            flags={"required": True},
        )
        key_encryption_key.source_vault = AAZObjectType(
            serialized_name="sourceVault",
            flags={"required": True},
        )

        source_vault = _schema_aml_filesystem_read.properties.encryption_settings.key_encryption_key.source_vault
        source_vault.id = AAZStrType()

        health = _schema_aml_filesystem_read.properties.health
        health.state = AAZStrType()
        health.status_code = AAZStrType(
            serialized_name="statusCode",
        )
        health.status_description = AAZStrType(
            serialized_name="statusDescription",
        )

        hsm = _schema_aml_filesystem_read.properties.hsm
        hsm.archive_status = AAZListType(
            serialized_name="archiveStatus",
            flags={"read_only": True},
        )
        hsm.settings = AAZObjectType()

        archive_status = _schema_aml_filesystem_read.properties.hsm.archive_status
        archive_status.Element = AAZObjectType(
            flags={"read_only": True},
        )

        _element = _schema_aml_filesystem_read.properties.hsm.archive_status.Element
        _element.filesystem_path = AAZStrType(
            serialized_name="filesystemPath",
            flags={"read_only": True},
        )
        _element.status = AAZObjectType(
            flags={"read_only": True},
        )

        status = _schema_aml_filesystem_read.properties.hsm.archive_status.Element.status
        status.error_code = AAZStrType(
            serialized_name="errorCode",
            flags={"read_only": True},
        )
        status.error_message = AAZStrType(
            serialized_name="errorMessage",
            flags={"read_only": True},
        )
        status.last_completion_time = AAZStrType(
            serialized_name="lastCompletionTime",
            flags={"read_only": True},
        )
        status.last_started_time = AAZStrType(
            serialized_name="lastStartedTime",
            flags={"read_only": True},
        )
        status.percent_complete = AAZIntType(
            serialized_name="percentComplete",
            flags={"read_only": True},
        )
        status.state = AAZStrType(
            flags={"read_only": True},
        )

        settings = _schema_aml_filesystem_read.properties.hsm.settings
        settings.container = AAZStrType(
            flags={"required": True},
        )
        settings.import_prefix = AAZStrType(
            serialized_name="importPrefix",
        )
        settings.logging_container = AAZStrType(
            serialized_name="loggingContainer",
            flags={"required": True},
        )

        maintenance_window = _schema_aml_filesystem_read.properties.maintenance_window
        maintenance_window.day_of_week = AAZStrType(
            serialized_name="dayOfWeek",
        )
        maintenance_window.time_of_day_utc = AAZStrType(
            serialized_name="timeOfDayUTC",
        )

        sku = _schema_aml_filesystem_read.sku
        sku.name = AAZStrType()

        system_data = _schema_aml_filesystem_read.system_data
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

        tags = _schema_aml_filesystem_read.tags
        tags.Element = AAZStrType()

        zones = _schema_aml_filesystem_read.zones
        zones.Element = AAZStrType()

        _schema.id = cls._schema_aml_filesystem_read.id
        _schema.identity = cls._schema_aml_filesystem_read.identity
        _schema.location = cls._schema_aml_filesystem_read.location
        _schema.name = cls._schema_aml_filesystem_read.name
        _schema.properties = cls._schema_aml_filesystem_read.properties
        _schema.sku = cls._schema_aml_filesystem_read.sku
        _schema.system_data = cls._schema_aml_filesystem_read.system_data
        _schema.tags = cls._schema_aml_filesystem_read.tags
        _schema.type = cls._schema_aml_filesystem_read.type
        _schema.zones = cls._schema_aml_filesystem_read.zones


__all__ = ["Update"]
