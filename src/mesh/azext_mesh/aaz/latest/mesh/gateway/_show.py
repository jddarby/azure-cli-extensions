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
    "mesh gateway show",
    is_preview=True,
)
class Show(AAZCommand):
    """Get the details of a gateway.
    """

    _aaz_info = {
        "version": "2018-09-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.servicefabricmesh/gateways/{}", "2018-09-01-preview"],
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
            help="The name of the gateway.",
            required=True,
            id_part="name",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.GatewayGet(ctx=self.ctx)()
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

    class GatewayGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ServiceFabricMesh/gateways/{gatewayResourceName}",
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
                    "gatewayResourceName", self.ctx.args.name,
                    skip_quote=True,
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
                    "api-version", "2018-09-01-preview",
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
            _schema_on_200.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.description = AAZStrType()
            properties.destination_network = AAZObjectType(
                serialized_name="destinationNetwork",
                flags={"required": True},
            )
            _ShowHelper._build_schema_network_ref_read(properties.destination_network)
            properties.http = AAZListType()
            properties.ip_address = AAZStrType(
                serialized_name="ipAddress",
                flags={"read_only": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.source_network = AAZObjectType(
                serialized_name="sourceNetwork",
                flags={"required": True},
            )
            _ShowHelper._build_schema_network_ref_read(properties.source_network)
            properties.status = AAZStrType()
            properties.status_details = AAZStrType(
                serialized_name="statusDetails",
                flags={"read_only": True},
            )
            properties.tcp = AAZListType()

            http = cls._schema_on_200.properties.http
            http.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.http.Element
            _element.hosts = AAZListType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"required": True},
            )
            _element.port = AAZIntType(
                flags={"required": True},
            )

            hosts = cls._schema_on_200.properties.http.Element.hosts
            hosts.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.http.Element.hosts.Element
            _element.name = AAZStrType(
                flags={"required": True},
            )
            _element.routes = AAZListType(
                flags={"required": True},
            )

            routes = cls._schema_on_200.properties.http.Element.hosts.Element.routes
            routes.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.http.Element.hosts.Element.routes.Element
            _element.destination = AAZObjectType(
                flags={"required": True},
            )
            _ShowHelper._build_schema_gateway_destination_read(_element.destination)
            _element.match = AAZObjectType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"required": True},
            )

            match = cls._schema_on_200.properties.http.Element.hosts.Element.routes.Element.match
            match.headers = AAZListType()
            match.path = AAZObjectType(
                flags={"required": True},
            )

            headers = cls._schema_on_200.properties.http.Element.hosts.Element.routes.Element.match.headers
            headers.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.http.Element.hosts.Element.routes.Element.match.headers.Element
            _element.name = AAZStrType(
                flags={"required": True},
            )
            _element.type = AAZStrType()
            _element.value = AAZStrType()

            path = cls._schema_on_200.properties.http.Element.hosts.Element.routes.Element.match.path
            path.rewrite = AAZStrType()
            path.type = AAZStrType(
                flags={"required": True},
            )
            path.value = AAZStrType(
                flags={"required": True},
            )

            tcp = cls._schema_on_200.properties.tcp
            tcp.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.tcp.Element
            _element.destination = AAZObjectType(
                flags={"required": True},
            )
            _ShowHelper._build_schema_gateway_destination_read(_element.destination)
            _element.name = AAZStrType(
                flags={"required": True},
            )
            _element.port = AAZIntType(
                flags={"required": True},
            )

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _ShowHelper:
    """Helper class for Show"""

    _schema_gateway_destination_read = None

    @classmethod
    def _build_schema_gateway_destination_read(cls, _schema):
        if cls._schema_gateway_destination_read is not None:
            _schema.application_name = cls._schema_gateway_destination_read.application_name
            _schema.endpoint_name = cls._schema_gateway_destination_read.endpoint_name
            _schema.service_name = cls._schema_gateway_destination_read.service_name
            return

        cls._schema_gateway_destination_read = _schema_gateway_destination_read = AAZObjectType()

        gateway_destination_read = _schema_gateway_destination_read
        gateway_destination_read.application_name = AAZStrType(
            serialized_name="applicationName",
            flags={"required": True},
        )
        gateway_destination_read.endpoint_name = AAZStrType(
            serialized_name="endpointName",
            flags={"required": True},
        )
        gateway_destination_read.service_name = AAZStrType(
            serialized_name="serviceName",
            flags={"required": True},
        )

        _schema.application_name = cls._schema_gateway_destination_read.application_name
        _schema.endpoint_name = cls._schema_gateway_destination_read.endpoint_name
        _schema.service_name = cls._schema_gateway_destination_read.service_name

    _schema_network_ref_read = None

    @classmethod
    def _build_schema_network_ref_read(cls, _schema):
        if cls._schema_network_ref_read is not None:
            _schema.endpoint_refs = cls._schema_network_ref_read.endpoint_refs
            _schema.name = cls._schema_network_ref_read.name
            return

        cls._schema_network_ref_read = _schema_network_ref_read = AAZObjectType()

        network_ref_read = _schema_network_ref_read
        network_ref_read.endpoint_refs = AAZListType(
            serialized_name="endpointRefs",
        )
        network_ref_read.name = AAZStrType()

        endpoint_refs = _schema_network_ref_read.endpoint_refs
        endpoint_refs.Element = AAZObjectType()

        _element = _schema_network_ref_read.endpoint_refs.Element
        _element.name = AAZStrType()

        _schema.endpoint_refs = cls._schema_network_ref_read.endpoint_refs
        _schema.name = cls._schema_network_ref_read.name


__all__ = ["Show"]
