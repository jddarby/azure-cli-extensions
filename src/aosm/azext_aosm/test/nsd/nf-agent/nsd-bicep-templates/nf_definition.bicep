// Copyright (c) Microsoft Corporation. All rights reserved.
// Highly Confidential Material
//
// The template that the NSD invokes to create the Network Function from a published NFDV. 

@description('Publisher where the NFD is published')
param publisherName string = 'sunnyclipub'

@description('NFD Group name for the Network Function')
param networkFunctionDefinitionGroupName string = 'nf-agent-cnf-nfdg'

@description('NFD version')
param networkFunctionDefinitionVersion string = '0.1.0'

@description('Offering location for the Network Function')
param networkFunctionDefinitionOfferingLocation string = 'uksouth'

param location string = 'uksouth'

param resourceGroupId string = resourceGroup().id

param nfAgentServiceBusNamespace string
param nfAgentUserAssignedIdentityResourceId string
param nfagent_topic string


var deploymentValues = {
  nfAgentServiceBusNamespace: nfAgentServiceBusNamespace
  nfAgentUserAssignedIdentityResourceId: nfAgentUserAssignedIdentityResourceId
  nfagent_topic: nfagent_topic
  
}

resource nf_resource 'Microsoft.HybridNetwork/networkFunctions@2023-04-01-preview' = {
  name: 'nfagent-nsdg_NF'
  location: location
  properties: {
    publisherName: publisherName
    publisherScope: 'Private'
    networkFunctionDefinitionGroupName: networkFunctionDefinitionGroupName
    networkFunctionDefinitionVersion: networkFunctionDefinitionVersion
    networkFunctionDefinitionOfferingLocation: networkFunctionDefinitionOfferingLocation
    nfviType: 'AzureCore'
    nfviId: resourceGroupId
    allowSoftwareUpdate: true
    deploymentValues: string(deploymentValues)
  }
}