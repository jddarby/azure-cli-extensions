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
    "monitor app-insights component linked-storage unlink",
    confirmation="Are you sure you want to perform this operation?",
)
class Unlink(AAZCommand):
    """Unlink a storage account with an Application Insights component.
    """

    _aaz_info = {
        "version": "2020-03-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.insights/components/{}/linkedstorageaccounts/{}", "2020-03-01-preview"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return None

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.app = AAZStrArg(
            options=["-a", "--app"],
            help="GUID, app name, or fully-qualified Azure resource name of Application                           Insights component. The application GUID may be acquired from the API                           Access menu item on any Application Insights resource in the Azure portal.                           If using an application name, please specify resource group.",
            required=True,
            id_part="name",
        )
        _args_schema.storage_type = AAZStrArg(
            options=["--storage-type"],
            help="The type of the Application Insights component data source for the linked storage account.",
            required=True,
            id_part="child_name_1",
            default="ServiceProfiler",
            enum={"ServiceProfiler": "ServiceProfiler"},
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.ComponentLinkedStorageAccountsDelete(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    class ComponentLinkedStorageAccountsDelete(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)
            if session.http_response.status_code in [204]:
                return self.on_204(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/components/{resourceName}/linkedStorageAccounts/{storageType}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "DELETE"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceName", self.ctx.args.app,
                    required=True,
                ),
                **self.serialize_url_param(
                    "storageType", self.ctx.args.storage_type,
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
                    "api-version", "2020-03-01-preview",
                    required=True,
                ),
            }
            return parameters

        def on_200(self, session):
            pass

        def on_204(self, session):
            pass


class _UnlinkHelper:
    """Helper class for Unlink"""


__all__ = ["Unlink"]
