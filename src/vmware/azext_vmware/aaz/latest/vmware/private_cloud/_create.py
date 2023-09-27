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
    "vmware private-cloud create",
    confirmation="LEGAL TERMS\n\nAzure VMware Solution (\"AVS\") is an Azure Service licensed to you as part of your Azure subscription and subject to the terms and conditions of the agreement under which you obtained your Azure subscription (https://azure.microsoft.com/support/legal/). The following additional terms also apply to your use of AVS:\n\nDATA RETENTION. AVS does not currently support retention or extraction of data stored in AVS Clusters. Once an AVS Cluster is deleted, the data cannot be recovered as it terminates all running workloads, components, and destroys all Cluster data and configuration settings, including public IP addresses.\n\nPROFESSIONAL SERVICES DATA TRANSFER TO VMWARE. In the event that you contact Microsoft for technical support relating to Azure VMware Solution and Microsoft must engage VMware for assistance with the issue, Microsoft will transfer the Professional Services Data and the Personal Data contained in the support case to VMware. The transfer is made subject to the terms of the Support Transfer Agreement between VMware and Microsoft, which establishes Microsoft and VMware as independent processors of the Professional Services Data. Before any transfer of Professional Services Data to VMware will occur, Microsoft will obtain and record consent from you for the transfer.\n\nVMWARE DATA PROCESSING AGREEMENT. Once Professional Services Data is transferred to VMware (pursuant to the above section), the processing of Professional Services Data, including the Personal Data contained the support case, by VMware as an independent processor will be governed by the VMware Data Processing Agreement for Microsoft AVS Customers Transferred for L3 Support (the \"VMware Data Processing Agreement\") between you and VMware (located at https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/privacy/vmware-data-processing-agreement.pdf). You also give authorization to allow your representative(s) who request technical support for Azure VMware Solution to provide consent on your behalf to Microsoft for the transfer of the Professional Services Data to VMware.\n\nACCEPTANCE OF LEGAL TERMS. By continuing, you agree to the above additional Legal Terms for AVS. If you are an individual accepting these terms on behalf of an entity, you also represent that you have the legal authority to enter into these additional terms on that entity's behalf.\n\nDo you agree to the above additional terms for AVS?",
)
class Create(AAZCommand):
    """Create a private cloud
    """

    _aaz_info = {
        "version": "2022-05-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.avs/privateclouds/{}", "2022-05-01"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

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
        _args_schema.private_cloud_name = AAZStrArg(
            options=["-n", "--name", "--private-cloud-name"],
            help="Name of the private cloud",
            required=True,
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Availability"

        _args_schema = cls._args_schema
        _args_schema.secondary_zone = AAZIntArg(
            options=["--secondary-zone"],
            arg_group="Availability",
            help="The secondary availability zone for the private cloud",
        )
        _args_schema.strategy = AAZStrArg(
            options=["--strategy"],
            arg_group="Availability",
            help="The availability strategy for the private cloud",
            enum={"DualZone": "DualZone", "SingleZone": "SingleZone"},
        )
        _args_schema.zone = AAZIntArg(
            options=["--zone"],
            arg_group="Availability",
            help="The primary availability zone for the private cloud",
        )

        # define Arg Group "ManagementCluster"

        _args_schema = cls._args_schema
        _args_schema.cluster_size = AAZIntArg(
            options=["--cluster-size"],
            arg_group="ManagementCluster",
            help="Number of hosts for the default management cluster. Minimum of 3 and maximum of 16.",
            required=True,
        )

        # define Arg Group "PrivateCloud"

        _args_schema = cls._args_schema
        _args_schema.identity = AAZObjectArg(
            options=["--identity"],
            arg_group="PrivateCloud",
            help="The identity of the private cloud, if configured.",
        )
        _args_schema.location = AAZResourceLocationArg(
            arg_group="PrivateCloud",
            help="Resource location",
            required=True,
            fmt=AAZResourceLocationArgFormat(
                resource_group_arg="resource_group",
            ),
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="PrivateCloud",
            help="Resource tags",
        )

        identity = cls._args_schema.identity
        identity.type = AAZStrArg(
            options=["type"],
            help="The type of identity used for the private cloud. The type 'SystemAssigned' refers to an implicitly created identity. The type 'None' will remove any identities from the Private Cloud.",
            enum={"None": "None", "SystemAssigned": "SystemAssigned"},
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg()

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.internet = AAZStrArg(
            options=["--internet"],
            arg_group="Properties",
            help="Connectivity to internet is enabled or disabled",
            default="Disabled",
            enum={"Disabled": "Disabled", "Enabled": "Enabled"},
        )
        _args_schema.network_block = AAZStrArg(
            options=["--network-block"],
            arg_group="Properties",
            help="The block of addresses should be unique across VNet in your subscription as well as on-premise. Make sure the CIDR format is conformed to (A.B.C.D/X) where A,B,C,D are between 0 and 255, and X is between 0 and 22",
            required=True,
        )
        _args_schema.nsxt_password = AAZPasswordArg(
            options=["--nsxt-password"],
            arg_group="Properties",
            help="NSX-T Manager password when the private cloud is created",
            blank=AAZPromptPasswordInput(
                msg="NSX-T Manager Password:",
                confirm=True,
            ),
        )
        _args_schema.vcenter_password = AAZPasswordArg(
            options=["--vcenter-password"],
            arg_group="Properties",
            help="vCenter admin password when the private cloud is created",
            blank=AAZPromptPasswordInput(
                msg="vCenter Admin Password:",
                confirm=True,
            ),
        )

        # define Arg Group "Sku"

        _args_schema = cls._args_schema
        _args_schema.sku = AAZStrArg(
            options=["--sku"],
            arg_group="Sku",
            help="The name of the SKU.",
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.PrivateCloudsCreateOrUpdate(ctx=self.ctx)()
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

    class PrivateCloudsCreateOrUpdate(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.AVS/privateClouds/{privateCloudName}",
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
                    "privateCloudName", self.ctx.args.private_cloud_name,
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
                    "api-version", "2022-05-01",
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
            _builder.set_prop("identity", AAZObjectType, ".identity")
            _builder.set_prop("location", AAZStrType, ".location", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})
            _builder.set_prop("sku", AAZObjectType, ".", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            identity = _builder.get(".identity")
            if identity is not None:
                identity.set_prop("type", AAZStrType, ".type")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("availability", AAZObjectType)
                properties.set_prop("internet", AAZStrType, ".internet")
                properties.set_prop("managementCluster", AAZObjectType, ".", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("networkBlock", AAZStrType, ".network_block", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("nsxtPassword", AAZStrType, ".nsxt_password", typ_kwargs={"flags": {"secret": True}})
                properties.set_prop("vcenterPassword", AAZStrType, ".vcenter_password", typ_kwargs={"flags": {"secret": True}})

            availability = _builder.get(".properties.availability")
            if availability is not None:
                availability.set_prop("secondaryZone", AAZIntType, ".secondary_zone")
                availability.set_prop("strategy", AAZStrType, ".strategy")
                availability.set_prop("zone", AAZIntType, ".zone")

            management_cluster = _builder.get(".properties.managementCluster")
            if management_cluster is not None:
                management_cluster.set_prop("clusterSize", AAZIntType, ".cluster_size", typ_kwargs={"flags": {"required": True}})

            sku = _builder.get(".sku")
            if sku is not None:
                sku.set_prop("name", AAZStrType, ".sku", typ_kwargs={"flags": {"required": True}})

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

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

            _schema_on_200_201 = cls._schema_on_200_201
            _schema_on_200_201.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.identity = AAZObjectType()
            _schema_on_200_201.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200_201.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_200_201.sku = AAZObjectType(
                flags={"required": True},
            )
            _schema_on_200_201.tags = AAZDictType()
            _schema_on_200_201.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_200_201.identity
            identity.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )
            identity.tenant_id = AAZStrType(
                serialized_name="tenantId",
                flags={"read_only": True},
            )
            identity.type = AAZStrType()

            properties = cls._schema_on_200_201.properties
            properties.availability = AAZObjectType()
            properties.circuit = AAZObjectType()
            _CreateHelper._build_schema_circuit_read(properties.circuit)
            properties.encryption = AAZObjectType()
            properties.endpoints = AAZObjectType()
            properties.external_cloud_links = AAZListType(
                serialized_name="externalCloudLinks",
                flags={"read_only": True},
            )
            properties.identity_sources = AAZListType(
                serialized_name="identitySources",
            )
            properties.internet = AAZStrType()
            properties.management_cluster = AAZObjectType(
                serialized_name="managementCluster",
                flags={"required": True},
            )
            properties.management_network = AAZStrType(
                serialized_name="managementNetwork",
                flags={"read_only": True},
            )
            properties.network_block = AAZStrType(
                serialized_name="networkBlock",
                flags={"required": True},
            )
            properties.nsx_public_ip_quota_raised = AAZStrType(
                serialized_name="nsxPublicIpQuotaRaised",
                flags={"read_only": True},
            )
            properties.nsxt_certificate_thumbprint = AAZStrType(
                serialized_name="nsxtCertificateThumbprint",
                flags={"read_only": True},
            )
            properties.nsxt_password = AAZStrType(
                serialized_name="nsxtPassword",
                flags={"secret": True},
            )
            properties.provisioning_network = AAZStrType(
                serialized_name="provisioningNetwork",
                flags={"read_only": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.secondary_circuit = AAZObjectType(
                serialized_name="secondaryCircuit",
            )
            _CreateHelper._build_schema_circuit_read(properties.secondary_circuit)
            properties.vcenter_certificate_thumbprint = AAZStrType(
                serialized_name="vcenterCertificateThumbprint",
                flags={"read_only": True},
            )
            properties.vcenter_password = AAZStrType(
                serialized_name="vcenterPassword",
                flags={"secret": True},
            )
            properties.vmotion_network = AAZStrType(
                serialized_name="vmotionNetwork",
                flags={"read_only": True},
            )

            availability = cls._schema_on_200_201.properties.availability
            availability.secondary_zone = AAZIntType(
                serialized_name="secondaryZone",
            )
            availability.strategy = AAZStrType()
            availability.zone = AAZIntType()

            encryption = cls._schema_on_200_201.properties.encryption
            encryption.key_vault_properties = AAZObjectType(
                serialized_name="keyVaultProperties",
            )
            encryption.status = AAZStrType()

            key_vault_properties = cls._schema_on_200_201.properties.encryption.key_vault_properties
            key_vault_properties.auto_detected_key_version = AAZStrType(
                serialized_name="autoDetectedKeyVersion",
                flags={"read_only": True},
            )
            key_vault_properties.key_name = AAZStrType(
                serialized_name="keyName",
            )
            key_vault_properties.key_state = AAZStrType(
                serialized_name="keyState",
                flags={"read_only": True},
            )
            key_vault_properties.key_vault_url = AAZStrType(
                serialized_name="keyVaultUrl",
            )
            key_vault_properties.key_version = AAZStrType(
                serialized_name="keyVersion",
            )
            key_vault_properties.version_type = AAZStrType(
                serialized_name="versionType",
                flags={"read_only": True},
            )

            endpoints = cls._schema_on_200_201.properties.endpoints
            endpoints.hcx_cloud_manager = AAZStrType(
                serialized_name="hcxCloudManager",
                flags={"read_only": True},
            )
            endpoints.nsxt_manager = AAZStrType(
                serialized_name="nsxtManager",
                flags={"read_only": True},
            )
            endpoints.vcsa = AAZStrType(
                flags={"read_only": True},
            )

            external_cloud_links = cls._schema_on_200_201.properties.external_cloud_links
            external_cloud_links.Element = AAZStrType()

            identity_sources = cls._schema_on_200_201.properties.identity_sources
            identity_sources.Element = AAZObjectType()

            _element = cls._schema_on_200_201.properties.identity_sources.Element
            _element.alias = AAZStrType(
                flags={"required": True},
            )
            _element.base_group_dn = AAZStrType(
                serialized_name="baseGroupDN",
                flags={"required": True},
            )
            _element.base_user_dn = AAZStrType(
                serialized_name="baseUserDN",
                flags={"required": True},
            )
            _element.domain = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"required": True},
            )
            _element.password = AAZStrType(
                flags={"secret": True},
            )
            _element.primary_server = AAZStrType(
                serialized_name="primaryServer",
                flags={"required": True},
            )
            _element.secondary_server = AAZStrType(
                serialized_name="secondaryServer",
            )
            _element.ssl = AAZStrType()
            _element.username = AAZStrType(
                flags={"secret": True},
            )

            management_cluster = cls._schema_on_200_201.properties.management_cluster
            management_cluster.cluster_id = AAZIntType(
                serialized_name="clusterId",
                flags={"read_only": True},
            )
            management_cluster.cluster_size = AAZIntType(
                serialized_name="clusterSize",
                flags={"required": True},
            )
            management_cluster.hosts = AAZListType()
            management_cluster.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )

            hosts = cls._schema_on_200_201.properties.management_cluster.hosts
            hosts.Element = AAZStrType()

            sku = cls._schema_on_200_201.sku
            sku.name = AAZStrType(
                flags={"required": True},
            )

            tags = cls._schema_on_200_201.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200_201


class _CreateHelper:
    """Helper class for Create"""

    _schema_circuit_read = None

    @classmethod
    def _build_schema_circuit_read(cls, _schema):
        if cls._schema_circuit_read is not None:
            _schema.express_route_id = cls._schema_circuit_read.express_route_id
            _schema.express_route_private_peering_id = cls._schema_circuit_read.express_route_private_peering_id
            _schema.primary_subnet = cls._schema_circuit_read.primary_subnet
            _schema.secondary_subnet = cls._schema_circuit_read.secondary_subnet
            return

        cls._schema_circuit_read = _schema_circuit_read = AAZObjectType()

        circuit_read = _schema_circuit_read
        circuit_read.express_route_id = AAZStrType(
            serialized_name="expressRouteID",
            flags={"read_only": True},
        )
        circuit_read.express_route_private_peering_id = AAZStrType(
            serialized_name="expressRoutePrivatePeeringID",
            flags={"read_only": True},
        )
        circuit_read.primary_subnet = AAZStrType(
            serialized_name="primarySubnet",
            flags={"read_only": True},
        )
        circuit_read.secondary_subnet = AAZStrType(
            serialized_name="secondarySubnet",
            flags={"read_only": True},
        )

        _schema.express_route_id = cls._schema_circuit_read.express_route_id
        _schema.express_route_private_peering_id = cls._schema_circuit_read.express_route_private_peering_id
        _schema.primary_subnet = cls._schema_circuit_read.primary_subnet
        _schema.secondary_subnet = cls._schema_circuit_read.secondary_subnet


__all__ = ["Create"]
