# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import *
from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer

class HdinsightonaksClusterPoolScenario(ScenarioTest):
    location = 'westus3'
    
    def test_available_cluster_pool_list(self):
        self.kwargs.update({
            'loc': self.location
        })
        # List a list of available cluster pool versions.
        cluster_pool_version_list = self.cmd('az hdinsight-on-aks list-available-cluster-pool-version -l {loc}').get_output_in_json()
        assert len(cluster_pool_version_list) > 0

    # Uses 'rg' kwarg
    @ResourceGroupPreparer(name_prefix='hilocli-', location=location, random_name_length=12)
    def test_clusterpool_operations(self):
        self.kwargs.update({
            'loc': self.location,
            'poolName': self.create_random_name(prefix='hilopool-', length=18),
            'logAnalyticProfileWorkspaceId': "/subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/psgroup/providers/microsoft.operationalinsights/workspaces/testworkspace"
        })

        # create a cluster pool
        self.cmd('az hdinsight-on-aks clusterpool create -g {rg} -n {poolName} -l {loc} --workernode-size Standard_E4s_v3', checks=[
            self.check("name", '{poolName}'),
            self.check("location", '{loc}'),
            self.check("status", 'Running')
        ])

        # set cluster pool enable log analytics
        self.cmd('az hdinsight-on-aks clusterpool update -g {rg} -n {poolName} --enable-log-analytics --log-analytic-workspace-id {logAnalyticProfileWorkspaceId}', checks=[
            self.check("name", '{poolName}'),
            self.check("location", '{loc}'),
            self.check("logAnalyticsProfile.enabled", True)
        ])

        # List the list of Cluster Pools within a resources group.
        cluster_pool_list = self.cmd('az hdinsight-on-aks clusterpool list -g {rg}').get_output_in_json()
        assert len(cluster_pool_list) > 0

        # Get a Cluster Pool.
        self.cmd('az hdinsight-on-aks clusterpool show -g {rg} -n {poolName}', checks=[
            self.check("name", '{poolName}'),
            self.check("location", '{loc}'),
            self.check("status", 'Running')
        ])

        # Delete a Cluster Pool.
        self.cmd('az hdinsight-on-aks clusterpool delete -g {rg} -n {poolName} --yes')
