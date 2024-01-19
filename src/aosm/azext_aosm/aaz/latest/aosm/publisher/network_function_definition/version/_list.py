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
    "aosm publisher network-function-definition version list",
    is_preview=True,
)
class List(AAZCommand):
    """List information about a list of network function definition versions under a network function definition group.
    """

    _aaz_info = {
        "version": "2023-09-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.hybridnetwork/publishers/{}/networkfunctiondefinitiongroups/{}/networkfunctiondefinitionversions", "2023-09-01"],
        ]
    }

    AZ_SUPPORT_PAGINATION = True

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
        _args_schema.group_name = AAZStrArg(
            options=["-n", "--group-name"],
            help="The name of the network function definition group.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9][a-zA-Z0-9_-]*$",
                max_length=64,
            ),
        )
        _args_schema.publisher_name = AAZStrArg(
            options=["--publisher-name"],
            help="The name of the publisher.",
            required=True,
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
        self.NetworkFunctionDefinitionVersionsListByNetworkFunctionDefinitionGroup(ctx=self.ctx)()
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

    class NetworkFunctionDefinitionVersionsListByNetworkFunctionDefinitionGroup(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridNetwork/publishers/{publisherName}/networkFunctionDefinitionGroups/{networkFunctionDefinitionGroupName}/networkFunctionDefinitionVersions",
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
                    "networkFunctionDefinitionGroupName", self.ctx.args.group_name,
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
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
                flags={"read_only": True},
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
            _element.properties = AAZObjectType()
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.deploy_parameters = AAZStrType(
                serialized_name="deployParameters",
            )
            properties.description = AAZStrType()
            properties.network_function_type = AAZStrType(
                serialized_name="networkFunctionType",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.version_state = AAZStrType(
                serialized_name="versionState",
            )

            disc_containerized_network_function = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction")
            disc_containerized_network_function.network_function_template = AAZObjectType(
                serialized_name="networkFunctionTemplate",
            )

            network_function_template = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template
            network_function_template.nfvi_type = AAZStrType(
                serialized_name="nfviType",
                flags={"required": True},
            )

            disc_azure_arc_kubernetes = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes")
            disc_azure_arc_kubernetes.network_function_applications = AAZListType(
                serialized_name="networkFunctionApplications",
            )

            network_function_applications = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications
            network_function_applications.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element
            _element.artifact_type = AAZStrType(
                serialized_name="artifactType",
                flags={"required": True},
            )
            _element.depends_on_profile = AAZObjectType(
                serialized_name="dependsOnProfile",
            )
            _ListHelper._build_schema_depends_on_profile_read(_element.depends_on_profile)
            _element.name = AAZStrType()

            disc_helm_package = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage")
            disc_helm_package.artifact_profile = AAZObjectType(
                serialized_name="artifactProfile",
            )
            disc_helm_package.deploy_parameters_mapping_rule_profile = AAZObjectType(
                serialized_name="deployParametersMappingRuleProfile",
            )

            artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").artifact_profile
            artifact_profile.artifact_store = AAZObjectType(
                serialized_name="artifactStore",
            )
            _ListHelper._build_schema_referenced_resource_read(artifact_profile.artifact_store)
            artifact_profile.helm_artifact_profile = AAZObjectType(
                serialized_name="helmArtifactProfile",
            )

            helm_artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").artifact_profile.helm_artifact_profile
            helm_artifact_profile.helm_package_name = AAZStrType(
                serialized_name="helmPackageName",
            )
            helm_artifact_profile.helm_package_version_range = AAZStrType(
                serialized_name="helmPackageVersionRange",
            )
            helm_artifact_profile.image_pull_secrets_values_paths = AAZListType(
                serialized_name="imagePullSecretsValuesPaths",
            )
            helm_artifact_profile.registry_values_paths = AAZListType(
                serialized_name="registryValuesPaths",
            )

            image_pull_secrets_values_paths = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").artifact_profile.helm_artifact_profile.image_pull_secrets_values_paths
            image_pull_secrets_values_paths.Element = AAZStrType()

            registry_values_paths = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").artifact_profile.helm_artifact_profile.registry_values_paths
            registry_values_paths.Element = AAZStrType()

            deploy_parameters_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").deploy_parameters_mapping_rule_profile
            deploy_parameters_mapping_rule_profile.application_enablement = AAZStrType(
                serialized_name="applicationEnablement",
            )
            deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile = AAZObjectType(
                serialized_name="helmMappingRuleProfile",
            )

            helm_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile
            helm_mapping_rule_profile.helm_package_version = AAZStrType(
                serialized_name="helmPackageVersion",
            )
            helm_mapping_rule_profile.options = AAZObjectType()
            helm_mapping_rule_profile.release_name = AAZStrType(
                serialized_name="releaseName",
            )
            helm_mapping_rule_profile.release_namespace = AAZStrType(
                serialized_name="releaseNamespace",
            )
            helm_mapping_rule_profile.values = AAZStrType()

            options = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile.options
            options.install_options = AAZObjectType(
                serialized_name="installOptions",
            )
            options.upgrade_options = AAZObjectType(
                serialized_name="upgradeOptions",
            )

            install_options = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile.options.install_options
            install_options.atomic = AAZStrType()
            install_options.timeout = AAZStrType()
            install_options.wait = AAZStrType()

            upgrade_options = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "ContainerizedNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureArcKubernetes").network_function_applications.Element.discriminate_by("artifact_type", "HelmPackage").deploy_parameters_mapping_rule_profile.helm_mapping_rule_profile.options.upgrade_options
            upgrade_options.atomic = AAZStrType()
            upgrade_options.timeout = AAZStrType()
            upgrade_options.wait = AAZStrType()

            disc_virtual_network_function = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction")
            disc_virtual_network_function.network_function_template = AAZObjectType(
                serialized_name="networkFunctionTemplate",
            )

            network_function_template = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template
            network_function_template.nfvi_type = AAZStrType(
                serialized_name="nfviType",
                flags={"required": True},
            )

            disc_azure_core = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore")
            disc_azure_core.network_function_applications = AAZListType(
                serialized_name="networkFunctionApplications",
            )

            network_function_applications = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications
            network_function_applications.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element
            _element.artifact_type = AAZStrType(
                serialized_name="artifactType",
                flags={"required": True},
            )
            _element.depends_on_profile = AAZObjectType(
                serialized_name="dependsOnProfile",
            )
            _ListHelper._build_schema_depends_on_profile_read(_element.depends_on_profile)
            _element.name = AAZStrType()

            disc_arm_template = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "ArmTemplate")
            disc_arm_template.artifact_profile = AAZObjectType(
                serialized_name="artifactProfile",
            )
            disc_arm_template.deploy_parameters_mapping_rule_profile = AAZObjectType(
                serialized_name="deployParametersMappingRuleProfile",
            )

            artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "ArmTemplate").artifact_profile
            artifact_profile.artifact_store = AAZObjectType(
                serialized_name="artifactStore",
            )
            _ListHelper._build_schema_referenced_resource_read(artifact_profile.artifact_store)
            artifact_profile.template_artifact_profile = AAZObjectType(
                serialized_name="templateArtifactProfile",
            )
            _ListHelper._build_schema_arm_template_artifact_profile_read(artifact_profile.template_artifact_profile)

            deploy_parameters_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "ArmTemplate").deploy_parameters_mapping_rule_profile
            deploy_parameters_mapping_rule_profile.application_enablement = AAZStrType(
                serialized_name="applicationEnablement",
            )
            deploy_parameters_mapping_rule_profile.template_mapping_rule_profile = AAZObjectType(
                serialized_name="templateMappingRuleProfile",
            )
            _ListHelper._build_schema_arm_template_mapping_rule_profile_read(deploy_parameters_mapping_rule_profile.template_mapping_rule_profile)

            disc_vhd_image_file = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "VhdImageFile")
            disc_vhd_image_file.artifact_profile = AAZObjectType(
                serialized_name="artifactProfile",
            )
            disc_vhd_image_file.deploy_parameters_mapping_rule_profile = AAZObjectType(
                serialized_name="deployParametersMappingRuleProfile",
            )

            artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "VhdImageFile").artifact_profile
            artifact_profile.artifact_store = AAZObjectType(
                serialized_name="artifactStore",
            )
            _ListHelper._build_schema_referenced_resource_read(artifact_profile.artifact_store)
            artifact_profile.vhd_artifact_profile = AAZObjectType(
                serialized_name="vhdArtifactProfile",
            )

            vhd_artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "VhdImageFile").artifact_profile.vhd_artifact_profile
            vhd_artifact_profile.vhd_name = AAZStrType(
                serialized_name="vhdName",
            )
            vhd_artifact_profile.vhd_version = AAZStrType(
                serialized_name="vhdVersion",
            )

            deploy_parameters_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "VhdImageFile").deploy_parameters_mapping_rule_profile
            deploy_parameters_mapping_rule_profile.application_enablement = AAZStrType(
                serialized_name="applicationEnablement",
            )
            deploy_parameters_mapping_rule_profile.vhd_image_mapping_rule_profile = AAZObjectType(
                serialized_name="vhdImageMappingRuleProfile",
            )

            vhd_image_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureCore").network_function_applications.Element.discriminate_by("artifact_type", "VhdImageFile").deploy_parameters_mapping_rule_profile.vhd_image_mapping_rule_profile
            vhd_image_mapping_rule_profile.user_configuration = AAZStrType(
                serialized_name="userConfiguration",
            )

            disc_azure_operator_nexus = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus")
            disc_azure_operator_nexus.network_function_applications = AAZListType(
                serialized_name="networkFunctionApplications",
            )

            network_function_applications = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications
            network_function_applications.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element
            _element.artifact_type = AAZStrType(
                serialized_name="artifactType",
                flags={"required": True},
            )
            _element.depends_on_profile = AAZObjectType(
                serialized_name="dependsOnProfile",
            )
            _ListHelper._build_schema_depends_on_profile_read(_element.depends_on_profile)
            _element.name = AAZStrType()

            disc_arm_template = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ArmTemplate")
            disc_arm_template.artifact_profile = AAZObjectType(
                serialized_name="artifactProfile",
            )
            disc_arm_template.deploy_parameters_mapping_rule_profile = AAZObjectType(
                serialized_name="deployParametersMappingRuleProfile",
            )

            artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ArmTemplate").artifact_profile
            artifact_profile.artifact_store = AAZObjectType(
                serialized_name="artifactStore",
            )
            _ListHelper._build_schema_referenced_resource_read(artifact_profile.artifact_store)
            artifact_profile.template_artifact_profile = AAZObjectType(
                serialized_name="templateArtifactProfile",
            )
            _ListHelper._build_schema_arm_template_artifact_profile_read(artifact_profile.template_artifact_profile)

            deploy_parameters_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ArmTemplate").deploy_parameters_mapping_rule_profile
            deploy_parameters_mapping_rule_profile.application_enablement = AAZStrType(
                serialized_name="applicationEnablement",
            )
            deploy_parameters_mapping_rule_profile.template_mapping_rule_profile = AAZObjectType(
                serialized_name="templateMappingRuleProfile",
            )
            _ListHelper._build_schema_arm_template_mapping_rule_profile_read(deploy_parameters_mapping_rule_profile.template_mapping_rule_profile)

            disc_image_file = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ImageFile")
            disc_image_file.artifact_profile = AAZObjectType(
                serialized_name="artifactProfile",
            )
            disc_image_file.deploy_parameters_mapping_rule_profile = AAZObjectType(
                serialized_name="deployParametersMappingRuleProfile",
            )

            artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ImageFile").artifact_profile
            artifact_profile.artifact_store = AAZObjectType(
                serialized_name="artifactStore",
            )
            _ListHelper._build_schema_referenced_resource_read(artifact_profile.artifact_store)
            artifact_profile.image_artifact_profile = AAZObjectType(
                serialized_name="imageArtifactProfile",
            )

            image_artifact_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ImageFile").artifact_profile.image_artifact_profile
            image_artifact_profile.image_name = AAZStrType(
                serialized_name="imageName",
            )
            image_artifact_profile.image_version = AAZStrType(
                serialized_name="imageVersion",
            )

            deploy_parameters_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ImageFile").deploy_parameters_mapping_rule_profile
            deploy_parameters_mapping_rule_profile.application_enablement = AAZStrType(
                serialized_name="applicationEnablement",
            )
            deploy_parameters_mapping_rule_profile.image_mapping_rule_profile = AAZObjectType(
                serialized_name="imageMappingRuleProfile",
            )

            image_mapping_rule_profile = cls._schema_on_200.value.Element.properties.discriminate_by("network_function_type", "VirtualNetworkFunction").network_function_template.discriminate_by("nfvi_type", "AzureOperatorNexus").network_function_applications.Element.discriminate_by("artifact_type", "ImageFile").deploy_parameters_mapping_rule_profile.image_mapping_rule_profile
            image_mapping_rule_profile.user_configuration = AAZStrType(
                serialized_name="userConfiguration",
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

    _schema_arm_template_artifact_profile_read = None

    @classmethod
    def _build_schema_arm_template_artifact_profile_read(cls, _schema):
        if cls._schema_arm_template_artifact_profile_read is not None:
            _schema.template_name = cls._schema_arm_template_artifact_profile_read.template_name
            _schema.template_version = cls._schema_arm_template_artifact_profile_read.template_version
            return

        cls._schema_arm_template_artifact_profile_read = _schema_arm_template_artifact_profile_read = AAZObjectType()

        arm_template_artifact_profile_read = _schema_arm_template_artifact_profile_read
        arm_template_artifact_profile_read.template_name = AAZStrType(
            serialized_name="templateName",
        )
        arm_template_artifact_profile_read.template_version = AAZStrType(
            serialized_name="templateVersion",
        )

        _schema.template_name = cls._schema_arm_template_artifact_profile_read.template_name
        _schema.template_version = cls._schema_arm_template_artifact_profile_read.template_version

    _schema_arm_template_mapping_rule_profile_read = None

    @classmethod
    def _build_schema_arm_template_mapping_rule_profile_read(cls, _schema):
        if cls._schema_arm_template_mapping_rule_profile_read is not None:
            _schema.template_parameters = cls._schema_arm_template_mapping_rule_profile_read.template_parameters
            return

        cls._schema_arm_template_mapping_rule_profile_read = _schema_arm_template_mapping_rule_profile_read = AAZObjectType()

        arm_template_mapping_rule_profile_read = _schema_arm_template_mapping_rule_profile_read
        arm_template_mapping_rule_profile_read.template_parameters = AAZStrType(
            serialized_name="templateParameters",
        )

        _schema.template_parameters = cls._schema_arm_template_mapping_rule_profile_read.template_parameters

    _schema_depends_on_profile_read = None

    @classmethod
    def _build_schema_depends_on_profile_read(cls, _schema):
        if cls._schema_depends_on_profile_read is not None:
            _schema.install_depends_on = cls._schema_depends_on_profile_read.install_depends_on
            _schema.uninstall_depends_on = cls._schema_depends_on_profile_read.uninstall_depends_on
            _schema.update_depends_on = cls._schema_depends_on_profile_read.update_depends_on
            return

        cls._schema_depends_on_profile_read = _schema_depends_on_profile_read = AAZObjectType()

        depends_on_profile_read = _schema_depends_on_profile_read
        depends_on_profile_read.install_depends_on = AAZListType(
            serialized_name="installDependsOn",
        )
        depends_on_profile_read.uninstall_depends_on = AAZListType(
            serialized_name="uninstallDependsOn",
        )
        depends_on_profile_read.update_depends_on = AAZListType(
            serialized_name="updateDependsOn",
        )

        install_depends_on = _schema_depends_on_profile_read.install_depends_on
        install_depends_on.Element = AAZStrType()

        uninstall_depends_on = _schema_depends_on_profile_read.uninstall_depends_on
        uninstall_depends_on.Element = AAZStrType()

        update_depends_on = _schema_depends_on_profile_read.update_depends_on
        update_depends_on.Element = AAZStrType()

        _schema.install_depends_on = cls._schema_depends_on_profile_read.install_depends_on
        _schema.uninstall_depends_on = cls._schema_depends_on_profile_read.uninstall_depends_on
        _schema.update_depends_on = cls._schema_depends_on_profile_read.update_depends_on

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


__all__ = ["List"]
