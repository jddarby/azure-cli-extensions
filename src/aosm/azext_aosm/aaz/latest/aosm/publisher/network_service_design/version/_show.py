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
    "aosm publisher network-service-design version show",
    is_preview=True,
)
class Show(AAZCommand):
    """Get information about a network service design version.
    """

    _aaz_info = {
        "version": "2023-09-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.hybridnetwork/publishers/{}/networkservicedesigngroups/{}/networkservicedesignversions/{}", "2023-09-01"],
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
        _args_schema.group_name = AAZStrArg(
            options=["-n", "--group-name"],
            help="The name of the network service design group.",
            required=True,
            id_part="child_name_1",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9][a-zA-Z0-9_-]*$",
                max_length=64,
            ),
        )
        _args_schema.version_name = AAZStrArg(
            options=["--version-name"],
            help="The name of the network service design version. The name should conform to the SemVer 2.0.0 specification: https://semver.org/spec/v2.0.0.html.",
            required=True,
            id_part="child_name_2",
            fmt=AAZStrArgFormat(
                pattern="^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
                max_length=64,
            ),
        )
        _args_schema.publisher_name = AAZStrArg(
            options=["--publisher-name"],
            help="The name of the publisher.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9][a-zA-Z0-9_-]*$",
                max_length=64,
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.NetworkServiceDesignVersionsGet(ctx=self.ctx)()
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

    class NetworkServiceDesignVersionsGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridNetwork/publishers/{publisherName}/networkServiceDesignGroups/{networkServiceDesignGroupName}/networkServiceDesignVersions/{networkServiceDesignVersionName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "networkServiceDesignGroupName", self.ctx.args.group_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "networkServiceDesignVersionName", self.ctx.args.version_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "publisherName", self.ctx.args.publisher_name,
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
                    "api-version", "2023-09-01",
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

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType()
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.configuration_group_schema_references = AAZDictType(
                serialized_name="configurationGroupSchemaReferences",
            )
            properties.description = AAZStrType()
            properties.nfvis_from_site = AAZDictType(
                serialized_name="nfvisFromSite",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.resource_element_templates = AAZListType(
                serialized_name="resourceElementTemplates",
            )
            properties.version_state = AAZStrType(
                serialized_name="versionState",
            )

            configuration_group_schema_references = cls._schema_on_200.properties.configuration_group_schema_references
            configuration_group_schema_references.Element = AAZObjectType()
            _ShowHelper._build_schema_referenced_resource_read(configuration_group_schema_references.Element)

            nfvis_from_site = cls._schema_on_200.properties.nfvis_from_site
            nfvis_from_site.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.nfvis_from_site.Element
            _element.name = AAZStrType()
            _element.type = AAZStrType()

            resource_element_templates = cls._schema_on_200.properties.resource_element_templates
            resource_element_templates.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.resource_element_templates.Element
            _element.depends_on_profile = AAZObjectType(
                serialized_name="dependsOnProfile",
            )
            _element.name = AAZStrType()
            _element.type = AAZStrType(
                flags={"required": True},
            )

            depends_on_profile = cls._schema_on_200.properties.resource_element_templates.Element.depends_on_profile
            depends_on_profile.install_depends_on = AAZListType(
                serialized_name="installDependsOn",
            )
            depends_on_profile.uninstall_depends_on = AAZListType(
                serialized_name="uninstallDependsOn",
            )
            depends_on_profile.update_depends_on = AAZListType(
                serialized_name="updateDependsOn",
            )

            install_depends_on = cls._schema_on_200.properties.resource_element_templates.Element.depends_on_profile.install_depends_on
            install_depends_on.Element = AAZStrType()

            uninstall_depends_on = cls._schema_on_200.properties.resource_element_templates.Element.depends_on_profile.uninstall_depends_on
            uninstall_depends_on.Element = AAZStrType()

            update_depends_on = cls._schema_on_200.properties.resource_element_templates.Element.depends_on_profile.update_depends_on
            update_depends_on.Element = AAZStrType()

            disc_arm_resource_definition = cls._schema_on_200.properties.resource_element_templates.Element.discriminate_by("type", "ArmResourceDefinition")
            disc_arm_resource_definition.configuration = AAZObjectType()
            _ShowHelper._build_schema_arm_resource_definition_resource_element_template_read(disc_arm_resource_definition.configuration)

            disc_network_function_definition = cls._schema_on_200.properties.resource_element_templates.Element.discriminate_by("type", "NetworkFunctionDefinition")
            disc_network_function_definition.configuration = AAZObjectType()
            _ShowHelper._build_schema_arm_resource_definition_resource_element_template_read(disc_network_function_definition.configuration)

            system_data = cls._schema_on_200.system_data
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

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _ShowHelper:
    """Helper class for Show"""

    _schema_arm_resource_definition_resource_element_template_read = None

    @classmethod
    def _build_schema_arm_resource_definition_resource_element_template_read(cls, _schema):
        if cls._schema_arm_resource_definition_resource_element_template_read is not None:
            _schema.artifact_profile = cls._schema_arm_resource_definition_resource_element_template_read.artifact_profile
            _schema.parameter_values = cls._schema_arm_resource_definition_resource_element_template_read.parameter_values
            _schema.template_type = cls._schema_arm_resource_definition_resource_element_template_read.template_type
            return

        cls._schema_arm_resource_definition_resource_element_template_read = _schema_arm_resource_definition_resource_element_template_read = AAZObjectType()

        arm_resource_definition_resource_element_template_read = _schema_arm_resource_definition_resource_element_template_read
        arm_resource_definition_resource_element_template_read.artifact_profile = AAZObjectType(
            serialized_name="artifactProfile",
        )
        arm_resource_definition_resource_element_template_read.parameter_values = AAZStrType(
            serialized_name="parameterValues",
        )
        arm_resource_definition_resource_element_template_read.template_type = AAZStrType(
            serialized_name="templateType",
        )

        artifact_profile = _schema_arm_resource_definition_resource_element_template_read.artifact_profile
        artifact_profile.artifact_name = AAZStrType(
            serialized_name="artifactName",
        )
        artifact_profile.artifact_store_reference = AAZObjectType(
            serialized_name="artifactStoreReference",
        )
        cls._build_schema_referenced_resource_read(artifact_profile.artifact_store_reference)
        artifact_profile.artifact_version = AAZStrType(
            serialized_name="artifactVersion",
        )

        _schema.artifact_profile = cls._schema_arm_resource_definition_resource_element_template_read.artifact_profile
        _schema.parameter_values = cls._schema_arm_resource_definition_resource_element_template_read.parameter_values
        _schema.template_type = cls._schema_arm_resource_definition_resource_element_template_read.template_type

    _schema_referenced_resource_read = None

    @classmethod
    def _build_schema_referenced_resource_read(cls, _schema):
        if cls._schema_referenced_resource_read is not None:
            _schema.id = cls._schema_referenced_resource_read.id
            return

        cls._schema_referenced_resource_read = _schema_referenced_resource_read = AAZObjectType()

        referenced_resource_read = _schema_referenced_resource_read
        referenced_resource_read.id = AAZStrType()

        _schema.id = cls._schema_referenced_resource_read.id


__all__ = ["Show"]
