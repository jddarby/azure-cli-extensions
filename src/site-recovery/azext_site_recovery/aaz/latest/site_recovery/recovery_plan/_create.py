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
    "site-recovery recovery-plan create",
)
class Create(AAZCommand):
    """Create operation to create a recovery plan.

    :example: recovery-plan create A2A
        az site-recovery recovery-plan create -n recovery_plan_name -g rg --vault-name vault_name --groups '[{group-type:Boot,replication-protected-items:[{id:protected_item_id,virtual-machine-id:vm_id}]}]' --primary-fabric-id fabric1_id --recovery-fabric-id fabric2_id --failover-deployment-model ResourceManager

    :example: recovery-plan create hyper-v-replica-azure
        az site-recovery recovery-plan create -n "recovery_plan_name" -g "rg" --vault-name "vault_name" --groups '[{group-type:Boot,replication-protected-items:[{id:"protected_item_id",virtual-machine-id:"protectable_item_id"}]}]' --primary-fabric-id "fabric_id" --recovery-fabric-id \"Microsoft Azure\" --failover-deployment-model ResourceManager

    :example: recovery-plan create for v2arcm
        az site-recovery recovery-plan create -n "recovery_plan_name" -g "rg" --vault-name "vault_name" --groups '[{group-type:Boot,replication-protected-items:[{id:"protected_item_id",virtual-machine-id:"vm_id"}]}]' --primary-fabric-id "fabric_id" --recovery-fabric-id "Microsoft Azure" --failover-deployment-model ResourceManager
    """

    _aaz_info = {
        "version": "2022-08-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.recoveryservices/vaults/{}/replicationrecoveryplans/{}", "2022-08-01"],
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
        _args_schema.recovery_plan_name = AAZStrArg(
            options=["-n", "--name", "--recovery-plan-name"],
            help="Recovery plan name.",
            required=True,
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.vault_name = AAZStrArg(
            options=["--vault-name"],
            help="The name of the recovery services vault.",
            required=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.failover_deployment_model = AAZStrArg(
            options=["--failover-deploy-model", "--failover-deployment-model"],
            arg_group="Properties",
            help="The failover deployment model.",
            enum={"Classic": "Classic", "NotApplicable": "NotApplicable", "ResourceManager": "ResourceManager"},
        )
        _args_schema.groups = AAZListArg(
            options=["--groups"],
            arg_group="Properties",
            help="The recovery plan groups.",
            required=True,
        )
        _args_schema.primary_fabric_id = AAZStrArg(
            options=["--primary-fabric-id"],
            arg_group="Properties",
            help="The primary fabric Id.",
            required=True,
        )
        _args_schema.provider_specific_input = AAZListArg(
            options=["--provider-input", "--provider-specific-input"],
            arg_group="Properties",
            help="The provider specific input.",
        )
        _args_schema.recovery_fabric_id = AAZStrArg(
            options=["--recovery-fabric-id"],
            arg_group="Properties",
            help="The recovery fabric Id.",
            required=True,
        )

        groups = cls._args_schema.groups
        groups.Element = AAZObjectArg()

        _element = cls._args_schema.groups.Element
        _element.end_group_actions = AAZListArg(
            options=["end-group-actions"],
            help="The end group actions.",
        )
        _element.group_type = AAZStrArg(
            options=["group-type"],
            help="The group type.",
            required=True,
            enum={"Boot": "Boot", "Failover": "Failover", "Shutdown": "Shutdown"},
        )
        _element.replication_protected_items = AAZListArg(
            options=["replication-protected-items"],
            help="The list of protected items.",
        )
        _element.start_group_actions = AAZListArg(
            options=["start-group-actions"],
            help="The start group actions.",
        )

        end_group_actions = cls._args_schema.groups.Element.end_group_actions
        end_group_actions.Element = AAZObjectArg()
        cls._build_args_recovery_plan_action_create(end_group_actions.Element)

        replication_protected_items = cls._args_schema.groups.Element.replication_protected_items
        replication_protected_items.Element = AAZObjectArg()

        _element = cls._args_schema.groups.Element.replication_protected_items.Element
        _element.id = AAZStrArg(
            options=["id"],
            help="The ARM Id of the recovery plan protected item.",
        )
        _element.virtual_machine_id = AAZStrArg(
            options=["virtual-machine-id"],
            help="The virtual machine Id.",
        )

        start_group_actions = cls._args_schema.groups.Element.start_group_actions
        start_group_actions.Element = AAZObjectArg()
        cls._build_args_recovery_plan_action_create(start_group_actions.Element)

        provider_specific_input = cls._args_schema.provider_specific_input
        provider_specific_input.Element = AAZObjectArg()

        _element = cls._args_schema.provider_specific_input.Element
        _element.a2a = AAZObjectArg(
            options=["a2a"],
            help="a2a",
        )

        a2a = cls._args_schema.provider_specific_input.Element.a2a
        a2a.primary_extended_location = AAZObjectArg(
            options=["primary-extended-location"],
            help="The primary extended location.",
        )
        cls._build_args_extended_location_create(a2a.primary_extended_location)
        a2a.primary_zone = AAZStrArg(
            options=["primary-zone"],
            help="The primary zone.",
        )
        a2a.recovery_extended_location = AAZObjectArg(
            options=["recovery-extended-location"],
            help="The recovery extended location.",
        )
        cls._build_args_extended_location_create(a2a.recovery_extended_location)
        a2a.recovery_zone = AAZStrArg(
            options=["recovery-zone"],
            help="The recovery zone.",
        )
        return cls._args_schema

    _args_extended_location_create = None

    @classmethod
    def _build_args_extended_location_create(cls, _schema):
        if cls._args_extended_location_create is not None:
            _schema.name = cls._args_extended_location_create.name
            _schema.type = cls._args_extended_location_create.type
            return

        cls._args_extended_location_create = AAZObjectArg()

        extended_location_create = cls._args_extended_location_create
        extended_location_create.name = AAZStrArg(
            options=["name"],
            help="The name of the extended location.",
            required=True,
        )
        extended_location_create.type = AAZStrArg(
            options=["type"],
            help="The extended location type.",
            required=True,
            enum={"EdgeZone": "EdgeZone"},
        )

        _schema.name = cls._args_extended_location_create.name
        _schema.type = cls._args_extended_location_create.type

    _args_recovery_plan_action_create = None

    @classmethod
    def _build_args_recovery_plan_action_create(cls, _schema):
        if cls._args_recovery_plan_action_create is not None:
            _schema.action_name = cls._args_recovery_plan_action_create.action_name
            _schema.custom_details = cls._args_recovery_plan_action_create.custom_details
            _schema.failover_directions = cls._args_recovery_plan_action_create.failover_directions
            _schema.failover_types = cls._args_recovery_plan_action_create.failover_types
            return

        cls._args_recovery_plan_action_create = AAZObjectArg()

        recovery_plan_action_create = cls._args_recovery_plan_action_create
        recovery_plan_action_create.action_name = AAZStrArg(
            options=["action-name"],
            help="The action name.",
            required=True,
        )
        recovery_plan_action_create.custom_details = AAZObjectArg(
            options=["custom-details"],
            help="The custom details.",
            required=True,
        )
        recovery_plan_action_create.failover_directions = AAZListArg(
            options=["failover-directions"],
            help="The list of failover directions.",
            required=True,
        )
        recovery_plan_action_create.failover_types = AAZListArg(
            options=["failover-types"],
            help="The list of failover types.",
            required=True,
        )

        custom_details = cls._args_recovery_plan_action_create.custom_details
        custom_details.automation_runbook_action_details = AAZObjectArg(
            options=["automation-runbook-action-details"],
        )
        custom_details.manual_action_details = AAZObjectArg(
            options=["manual-action-details"],
        )
        custom_details.script_action_details = AAZObjectArg(
            options=["script-action-details"],
        )

        automation_runbook_action_details = cls._args_recovery_plan_action_create.custom_details.automation_runbook_action_details
        automation_runbook_action_details.fabric_location = AAZStrArg(
            options=["fabric-location"],
            help="The fabric location.",
            required=True,
            enum={"Primary": "Primary", "Recovery": "Recovery"},
        )
        automation_runbook_action_details.runbook_id = AAZStrArg(
            options=["runbook-id"],
            help="The runbook ARM Id.",
        )
        automation_runbook_action_details.timeout = AAZStrArg(
            options=["timeout"],
            help="The runbook timeout.",
        )

        manual_action_details = cls._args_recovery_plan_action_create.custom_details.manual_action_details
        manual_action_details.description = AAZStrArg(
            options=["description"],
            help="The manual action description.",
        )

        script_action_details = cls._args_recovery_plan_action_create.custom_details.script_action_details
        script_action_details.fabric_location = AAZStrArg(
            options=["fabric-location"],
            help="The fabric location.",
            required=True,
            enum={"Primary": "Primary", "Recovery": "Recovery"},
        )
        script_action_details.path = AAZStrArg(
            options=["path"],
            help="The script path.",
            required=True,
        )
        script_action_details.timeout = AAZStrArg(
            options=["timeout"],
            help="The script timeout.",
        )

        failover_directions = cls._args_recovery_plan_action_create.failover_directions
        failover_directions.Element = AAZStrArg(
            enum={"PrimaryToRecovery": "PrimaryToRecovery", "RecoveryToPrimary": "RecoveryToPrimary"},
        )

        failover_types = cls._args_recovery_plan_action_create.failover_types
        failover_types.Element = AAZStrArg(
            enum={"CancelFailover": "CancelFailover", "ChangePit": "ChangePit", "Commit": "Commit", "CompleteMigration": "CompleteMigration", "DisableProtection": "DisableProtection", "Failback": "Failback", "FinalizeFailback": "FinalizeFailback", "PlannedFailover": "PlannedFailover", "RepairReplication": "RepairReplication", "ReverseReplicate": "ReverseReplicate", "SwitchProtection": "SwitchProtection", "TestFailover": "TestFailover", "TestFailoverCleanup": "TestFailoverCleanup", "UnplannedFailover": "UnplannedFailover"},
        )

        _schema.action_name = cls._args_recovery_plan_action_create.action_name
        _schema.custom_details = cls._args_recovery_plan_action_create.custom_details
        _schema.failover_directions = cls._args_recovery_plan_action_create.failover_directions
        _schema.failover_types = cls._args_recovery_plan_action_create.failover_types

    def _execute_operations(self):
        self.pre_operations()
        yield self.ReplicationRecoveryPlansCreate(ctx=self.ctx)()
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

    class ReplicationRecoveryPlansCreate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.RecoveryServices/vaults/{resourceName}/replicationRecoveryPlans/{recoveryPlanName}",
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
                    "recoveryPlanName", self.ctx.args.recovery_plan_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceName", self.ctx.args.vault_name,
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
                    "api-version", "2022-08-01",
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
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("failoverDeploymentModel", AAZStrType, ".failover_deployment_model")
                properties.set_prop("groups", AAZListType, ".groups", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("primaryFabricId", AAZStrType, ".primary_fabric_id", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("providerSpecificInput", AAZListType, ".provider_specific_input")
                properties.set_prop("recoveryFabricId", AAZStrType, ".recovery_fabric_id", typ_kwargs={"flags": {"required": True}})

            groups = _builder.get(".properties.groups")
            if groups is not None:
                groups.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.groups[]")
            if _elements is not None:
                _elements.set_prop("endGroupActions", AAZListType, ".end_group_actions")
                _elements.set_prop("groupType", AAZStrType, ".group_type", typ_kwargs={"flags": {"required": True}})
                _elements.set_prop("replicationProtectedItems", AAZListType, ".replication_protected_items")
                _elements.set_prop("startGroupActions", AAZListType, ".start_group_actions")

            end_group_actions = _builder.get(".properties.groups[].endGroupActions")
            if end_group_actions is not None:
                _CreateHelper._build_schema_recovery_plan_action_create(end_group_actions.set_elements(AAZObjectType, "."))

            replication_protected_items = _builder.get(".properties.groups[].replicationProtectedItems")
            if replication_protected_items is not None:
                replication_protected_items.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.groups[].replicationProtectedItems[]")
            if _elements is not None:
                _elements.set_prop("id", AAZStrType, ".id")
                _elements.set_prop("virtualMachineId", AAZStrType, ".virtual_machine_id")

            start_group_actions = _builder.get(".properties.groups[].startGroupActions")
            if start_group_actions is not None:
                _CreateHelper._build_schema_recovery_plan_action_create(start_group_actions.set_elements(AAZObjectType, "."))

            provider_specific_input = _builder.get(".properties.providerSpecificInput")
            if provider_specific_input is not None:
                provider_specific_input.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.providerSpecificInput[]")
            if _elements is not None:
                _elements.set_const("instanceType", "A2A", AAZStrType, ".a2a", typ_kwargs={"flags": {"required": True}})
                _elements.discriminate_by("instanceType", "A2A")

            disc_a2_a = _builder.get(".properties.providerSpecificInput[]{instanceType:A2A}")
            if disc_a2_a is not None:
                _CreateHelper._build_schema_extended_location_create(disc_a2_a.set_prop("primaryExtendedLocation", AAZObjectType, ".a2a.primary_extended_location"))
                disc_a2_a.set_prop("primaryZone", AAZStrType, ".a2a.primary_zone")
                _CreateHelper._build_schema_extended_location_create(disc_a2_a.set_prop("recoveryExtendedLocation", AAZObjectType, ".a2a.recovery_extended_location"))
                disc_a2_a.set_prop("recoveryZone", AAZStrType, ".a2a.recovery_zone")

            return self.serialize_content(_content_value)

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
            _schema_on_200.location = AAZStrType()
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.allowed_operations = AAZListType(
                serialized_name="allowedOperations",
            )
            properties.current_scenario = AAZObjectType(
                serialized_name="currentScenario",
            )
            properties.current_scenario_status = AAZStrType(
                serialized_name="currentScenarioStatus",
            )
            properties.current_scenario_status_description = AAZStrType(
                serialized_name="currentScenarioStatusDescription",
            )
            properties.failover_deployment_model = AAZStrType(
                serialized_name="failoverDeploymentModel",
            )
            properties.friendly_name = AAZStrType(
                serialized_name="friendlyName",
            )
            properties.groups = AAZListType()
            properties.last_planned_failover_time = AAZStrType(
                serialized_name="lastPlannedFailoverTime",
            )
            properties.last_test_failover_time = AAZStrType(
                serialized_name="lastTestFailoverTime",
            )
            properties.last_unplanned_failover_time = AAZStrType(
                serialized_name="lastUnplannedFailoverTime",
            )
            properties.primary_fabric_friendly_name = AAZStrType(
                serialized_name="primaryFabricFriendlyName",
            )
            properties.primary_fabric_id = AAZStrType(
                serialized_name="primaryFabricId",
            )
            properties.provider_specific_details = AAZListType(
                serialized_name="providerSpecificDetails",
            )
            properties.recovery_fabric_friendly_name = AAZStrType(
                serialized_name="recoveryFabricFriendlyName",
            )
            properties.recovery_fabric_id = AAZStrType(
                serialized_name="recoveryFabricId",
            )
            properties.replication_providers = AAZListType(
                serialized_name="replicationProviders",
            )

            allowed_operations = cls._schema_on_200.properties.allowed_operations
            allowed_operations.Element = AAZStrType()

            current_scenario = cls._schema_on_200.properties.current_scenario
            current_scenario.job_id = AAZStrType(
                serialized_name="jobId",
            )
            current_scenario.scenario_name = AAZStrType(
                serialized_name="scenarioName",
            )
            current_scenario.start_time = AAZStrType(
                serialized_name="startTime",
            )

            groups = cls._schema_on_200.properties.groups
            groups.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.groups.Element
            _element.end_group_actions = AAZListType(
                serialized_name="endGroupActions",
            )
            _element.group_type = AAZStrType(
                serialized_name="groupType",
                flags={"required": True},
            )
            _element.replication_protected_items = AAZListType(
                serialized_name="replicationProtectedItems",
            )
            _element.start_group_actions = AAZListType(
                serialized_name="startGroupActions",
            )

            end_group_actions = cls._schema_on_200.properties.groups.Element.end_group_actions
            end_group_actions.Element = AAZObjectType()
            _CreateHelper._build_schema_recovery_plan_action_read(end_group_actions.Element)

            replication_protected_items = cls._schema_on_200.properties.groups.Element.replication_protected_items
            replication_protected_items.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.groups.Element.replication_protected_items.Element
            _element.id = AAZStrType()
            _element.virtual_machine_id = AAZStrType(
                serialized_name="virtualMachineId",
            )

            start_group_actions = cls._schema_on_200.properties.groups.Element.start_group_actions
            start_group_actions.Element = AAZObjectType()
            _CreateHelper._build_schema_recovery_plan_action_read(start_group_actions.Element)

            provider_specific_details = cls._schema_on_200.properties.provider_specific_details
            provider_specific_details.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.provider_specific_details.Element
            _element.instance_type = AAZStrType(
                serialized_name="instanceType",
                flags={"required": True},
            )

            disc_a2_a = cls._schema_on_200.properties.provider_specific_details.Element.discriminate_by("instance_type", "A2A")
            disc_a2_a.primary_zone = AAZStrType(
                serialized_name="primaryZone",
            )
            disc_a2_a.recovery_zone = AAZStrType(
                serialized_name="recoveryZone",
            )

            replication_providers = cls._schema_on_200.properties.replication_providers
            replication_providers.Element = AAZStrType()

            return cls._schema_on_200


class _CreateHelper:
    """Helper class for Create"""

    @classmethod
    def _build_schema_extended_location_create(cls, _builder):
        if _builder is None:
            return
        _builder.set_prop("name", AAZStrType, ".name", typ_kwargs={"flags": {"required": True}})
        _builder.set_prop("type", AAZStrType, ".type", typ_kwargs={"flags": {"required": True}})

    @classmethod
    def _build_schema_recovery_plan_action_create(cls, _builder):
        if _builder is None:
            return
        _builder.set_prop("actionName", AAZStrType, ".action_name", typ_kwargs={"flags": {"required": True}})
        _builder.set_prop("customDetails", AAZObjectType, ".custom_details", typ_kwargs={"flags": {"required": True}})
        _builder.set_prop("failoverDirections", AAZListType, ".failover_directions", typ_kwargs={"flags": {"required": True}})
        _builder.set_prop("failoverTypes", AAZListType, ".failover_types", typ_kwargs={"flags": {"required": True}})

        custom_details = _builder.get(".customDetails")
        if custom_details is not None:
            custom_details.set_const("instanceType", "AutomationRunbookActionDetails", AAZStrType, ".automation_runbook_action_details", typ_kwargs={"flags": {"required": True}})
            custom_details.set_const("instanceType", "ManualActionDetails", AAZStrType, ".manual_action_details", typ_kwargs={"flags": {"required": True}})
            custom_details.set_const("instanceType", "ScriptActionDetails", AAZStrType, ".script_action_details", typ_kwargs={"flags": {"required": True}})
            custom_details.discriminate_by("instanceType", "AutomationRunbookActionDetails")
            custom_details.discriminate_by("instanceType", "ManualActionDetails")
            custom_details.discriminate_by("instanceType", "ScriptActionDetails")

        disc_automation_runbook_action_details = _builder.get(".customDetails{instanceType:AutomationRunbookActionDetails}")
        if disc_automation_runbook_action_details is not None:
            disc_automation_runbook_action_details.set_prop("fabricLocation", AAZStrType, ".automation_runbook_action_details.fabric_location", typ_kwargs={"flags": {"required": True}})
            disc_automation_runbook_action_details.set_prop("runbookId", AAZStrType, ".automation_runbook_action_details.runbook_id")
            disc_automation_runbook_action_details.set_prop("timeout", AAZStrType, ".automation_runbook_action_details.timeout")

        disc_manual_action_details = _builder.get(".customDetails{instanceType:ManualActionDetails}")
        if disc_manual_action_details is not None:
            disc_manual_action_details.set_prop("description", AAZStrType, ".manual_action_details.description")

        disc_script_action_details = _builder.get(".customDetails{instanceType:ScriptActionDetails}")
        if disc_script_action_details is not None:
            disc_script_action_details.set_prop("fabricLocation", AAZStrType, ".script_action_details.fabric_location", typ_kwargs={"flags": {"required": True}})
            disc_script_action_details.set_prop("path", AAZStrType, ".script_action_details.path", typ_kwargs={"flags": {"required": True}})
            disc_script_action_details.set_prop("timeout", AAZStrType, ".script_action_details.timeout")

        failover_directions = _builder.get(".failoverDirections")
        if failover_directions is not None:
            failover_directions.set_elements(AAZStrType, ".")

        failover_types = _builder.get(".failoverTypes")
        if failover_types is not None:
            failover_types.set_elements(AAZStrType, ".")

    _schema_recovery_plan_action_read = None

    @classmethod
    def _build_schema_recovery_plan_action_read(cls, _schema):
        if cls._schema_recovery_plan_action_read is not None:
            _schema.action_name = cls._schema_recovery_plan_action_read.action_name
            _schema.custom_details = cls._schema_recovery_plan_action_read.custom_details
            _schema.failover_directions = cls._schema_recovery_plan_action_read.failover_directions
            _schema.failover_types = cls._schema_recovery_plan_action_read.failover_types
            return

        cls._schema_recovery_plan_action_read = _schema_recovery_plan_action_read = AAZObjectType()

        recovery_plan_action_read = _schema_recovery_plan_action_read
        recovery_plan_action_read.action_name = AAZStrType(
            serialized_name="actionName",
            flags={"required": True},
        )
        recovery_plan_action_read.custom_details = AAZObjectType(
            serialized_name="customDetails",
            flags={"required": True},
        )
        recovery_plan_action_read.failover_directions = AAZListType(
            serialized_name="failoverDirections",
            flags={"required": True},
        )
        recovery_plan_action_read.failover_types = AAZListType(
            serialized_name="failoverTypes",
            flags={"required": True},
        )

        custom_details = _schema_recovery_plan_action_read.custom_details
        custom_details.instance_type = AAZStrType(
            serialized_name="instanceType",
            flags={"required": True},
        )

        disc_automation_runbook_action_details = _schema_recovery_plan_action_read.custom_details.discriminate_by("instance_type", "AutomationRunbookActionDetails")
        disc_automation_runbook_action_details.fabric_location = AAZStrType(
            serialized_name="fabricLocation",
            flags={"required": True},
        )
        disc_automation_runbook_action_details.runbook_id = AAZStrType(
            serialized_name="runbookId",
        )
        disc_automation_runbook_action_details.timeout = AAZStrType()

        disc_manual_action_details = _schema_recovery_plan_action_read.custom_details.discriminate_by("instance_type", "ManualActionDetails")
        disc_manual_action_details.description = AAZStrType()

        disc_script_action_details = _schema_recovery_plan_action_read.custom_details.discriminate_by("instance_type", "ScriptActionDetails")
        disc_script_action_details.fabric_location = AAZStrType(
            serialized_name="fabricLocation",
            flags={"required": True},
        )
        disc_script_action_details.path = AAZStrType(
            flags={"required": True},
        )
        disc_script_action_details.timeout = AAZStrType()

        failover_directions = _schema_recovery_plan_action_read.failover_directions
        failover_directions.Element = AAZStrType()

        failover_types = _schema_recovery_plan_action_read.failover_types
        failover_types.Element = AAZStrType()

        _schema.action_name = cls._schema_recovery_plan_action_read.action_name
        _schema.custom_details = cls._schema_recovery_plan_action_read.custom_details
        _schema.failover_directions = cls._schema_recovery_plan_action_read.failover_directions
        _schema.failover_types = cls._schema_recovery_plan_action_read.failover_types


__all__ = ["Create"]
