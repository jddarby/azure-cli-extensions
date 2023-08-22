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
    "networkfabric l3domain list",
)
class List(AAZCommand):
    """List all L3 Isolation Domains in the provided resource group or subscription

    :example: List the L3 Isolation Domains for Resource Group
        az networkfabric l3domain list --resource-group "example-rg"

    :example: List the L3 Isolation Domains for Subscription
        az networkfabric l3domain list --subscription "<subscriptionId>"
    """

    _aaz_info = {
        "version": "2023-06-15",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.managednetworkfabric/l3isolationdomains", "2023-06-15"],
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.managednetworkfabric/l3isolationdomains", "2023-06-15"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_paging(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            help="Name of the resource group",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        condition_0 = has_value(self.ctx.args.resource_group) and has_value(self.ctx.subscription_id)
        condition_1 = has_value(self.ctx.subscription_id) and has_value(self.ctx.args.resource_group) is not True
        if condition_0:
            self.L3IsolationDomainsListByResourceGroup(ctx=self.ctx)()
        if condition_1:
            self.L3IsolationDomainsListBySubscription(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance.value, client_flatten=True)
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)
        return result, next_link

    class L3IsolationDomainsListByResourceGroup(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetworkFabric/l3IsolationDomains",
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
                    "api-version", "2023-06-15",
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
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType()

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.administrative_state = AAZStrType(
                serialized_name="administrativeState",
                flags={"read_only": True},
            )
            properties.aggregate_route_configuration = AAZObjectType(
                serialized_name="aggregateRouteConfiguration",
            )
            properties.annotation = AAZStrType()
            properties.configuration_state = AAZStrType(
                serialized_name="configurationState",
                flags={"read_only": True},
            )
            properties.connected_subnet_route_policy = AAZObjectType(
                serialized_name="connectedSubnetRoutePolicy",
            )
            properties.network_fabric_id = AAZStrType(
                serialized_name="networkFabricId",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.redistribute_connected_subnets = AAZStrType(
                serialized_name="redistributeConnectedSubnets",
            )
            properties.redistribute_static_routes = AAZStrType(
                serialized_name="redistributeStaticRoutes",
            )

            aggregate_route_configuration = cls._schema_on_200.value.Element.properties.aggregate_route_configuration
            aggregate_route_configuration.ipv4_routes = AAZListType(
                serialized_name="ipv4Routes",
            )
            aggregate_route_configuration.ipv6_routes = AAZListType(
                serialized_name="ipv6Routes",
            )

            ipv4_routes = cls._schema_on_200.value.Element.properties.aggregate_route_configuration.ipv4_routes
            ipv4_routes.Element = AAZObjectType()
            _ListHelper._build_schema_aggregate_route_read(ipv4_routes.Element)

            ipv6_routes = cls._schema_on_200.value.Element.properties.aggregate_route_configuration.ipv6_routes
            ipv6_routes.Element = AAZObjectType()
            _ListHelper._build_schema_aggregate_route_read(ipv6_routes.Element)

            connected_subnet_route_policy = cls._schema_on_200.value.Element.properties.connected_subnet_route_policy
            connected_subnet_route_policy.export_route_policy = AAZObjectType(
                serialized_name="exportRoutePolicy",
            )
            connected_subnet_route_policy.export_route_policy_id = AAZStrType(
                serialized_name="exportRoutePolicyId",
            )

            export_route_policy = cls._schema_on_200.value.Element.properties.connected_subnet_route_policy.export_route_policy
            export_route_policy.export_ipv4_route_policy_id = AAZStrType(
                serialized_name="exportIpv4RoutePolicyId",
            )
            export_route_policy.export_ipv6_route_policy_id = AAZStrType(
                serialized_name="exportIpv6RoutePolicyId",
            )

            system_data = cls._schema_on_200.value.Element.system_data
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

            tags = cls._schema_on_200.value.Element.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200

    class L3IsolationDomainsListBySubscription(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/providers/Microsoft.ManagedNetworkFabric/l3IsolationDomains",
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
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-06-15",
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
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType()

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.administrative_state = AAZStrType(
                serialized_name="administrativeState",
                flags={"read_only": True},
            )
            properties.aggregate_route_configuration = AAZObjectType(
                serialized_name="aggregateRouteConfiguration",
            )
            properties.annotation = AAZStrType()
            properties.configuration_state = AAZStrType(
                serialized_name="configurationState",
                flags={"read_only": True},
            )
            properties.connected_subnet_route_policy = AAZObjectType(
                serialized_name="connectedSubnetRoutePolicy",
            )
            properties.network_fabric_id = AAZStrType(
                serialized_name="networkFabricId",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.redistribute_connected_subnets = AAZStrType(
                serialized_name="redistributeConnectedSubnets",
            )
            properties.redistribute_static_routes = AAZStrType(
                serialized_name="redistributeStaticRoutes",
            )

            aggregate_route_configuration = cls._schema_on_200.value.Element.properties.aggregate_route_configuration
            aggregate_route_configuration.ipv4_routes = AAZListType(
                serialized_name="ipv4Routes",
            )
            aggregate_route_configuration.ipv6_routes = AAZListType(
                serialized_name="ipv6Routes",
            )

            ipv4_routes = cls._schema_on_200.value.Element.properties.aggregate_route_configuration.ipv4_routes
            ipv4_routes.Element = AAZObjectType()
            _ListHelper._build_schema_aggregate_route_read(ipv4_routes.Element)

            ipv6_routes = cls._schema_on_200.value.Element.properties.aggregate_route_configuration.ipv6_routes
            ipv6_routes.Element = AAZObjectType()
            _ListHelper._build_schema_aggregate_route_read(ipv6_routes.Element)

            connected_subnet_route_policy = cls._schema_on_200.value.Element.properties.connected_subnet_route_policy
            connected_subnet_route_policy.export_route_policy = AAZObjectType(
                serialized_name="exportRoutePolicy",
            )
            connected_subnet_route_policy.export_route_policy_id = AAZStrType(
                serialized_name="exportRoutePolicyId",
            )

            export_route_policy = cls._schema_on_200.value.Element.properties.connected_subnet_route_policy.export_route_policy
            export_route_policy.export_ipv4_route_policy_id = AAZStrType(
                serialized_name="exportIpv4RoutePolicyId",
            )
            export_route_policy.export_ipv6_route_policy_id = AAZStrType(
                serialized_name="exportIpv6RoutePolicyId",
            )

            system_data = cls._schema_on_200.value.Element.system_data
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

            tags = cls._schema_on_200.value.Element.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _ListHelper:
    """Helper class for List"""

    _schema_aggregate_route_read = None

    @classmethod
    def _build_schema_aggregate_route_read(cls, _schema):
        if cls._schema_aggregate_route_read is not None:
            _schema.prefix = cls._schema_aggregate_route_read.prefix
            return

        cls._schema_aggregate_route_read = _schema_aggregate_route_read = AAZObjectType()

        aggregate_route_read = _schema_aggregate_route_read
        aggregate_route_read.prefix = AAZStrType(
            flags={"required": True},
        )

        _schema.prefix = cls._schema_aggregate_route_read.prefix


__all__ = ["List"]
