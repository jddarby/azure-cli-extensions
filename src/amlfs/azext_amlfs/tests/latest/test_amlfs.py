# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import *


class AmlfsScenario(ScenarioTest):
    @ResourceGroupPreparer(location='eastus')
    def test_amlfs(self):
        email = self.cmd('account show').get_output_in_json()['user']['name']
        self.kwargs.update({
            'vnet': self.create_random_name('vnet', 10),
            'subnet': self.create_random_name('subnet', 15),
            'amlfs': self.create_random_name('sys', 10),
            'id_name': self.create_random_name('id', 10)
        })
        identity_id = self.cmd('identity create -g {rg} -n {id_name} ').get_output_in_json()['id']
        self.cmd('network vnet create -n {vnet} -g {rg} --address-prefix 20.0.0.0/24')
        subnet_id = self.cmd('network vnet subnet create -n {subnet} -g {rg} --address-prefix 20.0.0.0/24 --vnet-name {vnet} --delegations Qumulo.Storage/fileSystems').get_output_in_json()['id']
        self.kwargs.update({
            'identity_id': identity_id,
            'subnet_id': subnet_id
        })
        self.cmd("amlfs create -n {amlfs} -g {rg} --sku AMLFS-Durable-Premium-250 --storage-capacity 16 --zones [1] --maintenance-window dayOfWeek=friday timeOfDayUtc=22:00 --filesystem-subnet {subnet_id} --mi-user-assigned {id_name}", checks=[
            self.check('name', '{amlfs}'),
            self.check('sku.name', 'AMLFS-Durable-Premium-250'),
            self.check('storageCapacityTiB', 16.0),
            self.check('zones', ['1']),
            self.check('maintenanceWindow.dayOfWeek', 'Friday'),
            self.check('maintenanceWindow.timeOfDayUTC', '22:00'),
            self.check('filesystemSubnet', '{subnet_id}'),
            self.check('health.state', 'Available'),
            self.check('identity.type', 'UserAssigned'),
            self.exists('identity.userAssignedIdentities')
        ])
        self.cmd('amlfs update -n {amlfs} -g {rg} --tags {{tag:test}}', checks=[
            self.check('name', '{amlfs}'),
            self.check('sku.name', 'AMLFS-Durable-Premium-250'),
            self.check('storageCapacityTiB', 16.0),
            self.check('zones', ['1']),
            self.check('maintenanceWindow.dayOfWeek', 'Friday'),
            self.check('maintenanceWindow.timeOfDayUTC', '22:00'),
            self.check('filesystemSubnet', '{subnet_id}'),
            self.check('health.state', 'Available'),
            self.check('tags.tag', 'test'),
            self.check('identity.type', 'UserAssigned'),
            self.exists('identity.userAssignedIdentities')
        ])
        self.cmd('amlfs show -n {amlfs} -g {rg}', checks=[
            self.check('name', '{amlfs}'),
            self.check('sku.name', 'AMLFS-Durable-Premium-250'),
            self.check('storageCapacityTiB', 16.0),
            self.check('zones', ['1']),
            self.check('maintenanceWindow.dayOfWeek', 'Friday'),
            self.check('maintenanceWindow.timeOfDayUTC', '22:00'),
            self.check('filesystemSubnet', '{subnet_id}'),
            self.check('health.state', 'Available'),
            self.check('tags.tag', 'test'),
            self.check('identity.type', 'UserAssigned'),
            self.exists('identity.userAssignedIdentities')
        ])
        self.cmd('amlfs list -g {rg}', checks=[
            self.check('[0].name', '{amlfs}'),
            self.check('[0].sku.name', 'AMLFS-Durable-Premium-250'),
            self.check('[0].storageCapacityTiB', 16.0),
            self.check('[0].zones', ['1']),
            self.check('[0].maintenanceWindow.dayOfWeek', 'Friday'),
            self.check('[0].maintenanceWindow.timeOfDayUTC', '22:00'),
            self.check('[0].filesystemSubnet', '{subnet_id}'),
            self.check('[0].health.state', 'Available'),
            self.check('[0].tags.tag', 'test'),
            self.check('[0].identity.type', 'UserAssigned'),
            self.exists('[0].identity.userAssignedIdentities')
        ])
        self.cmd('amlfs delete -n {amlfs} -g {rg} -y')
