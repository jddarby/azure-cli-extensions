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

@description('Custom location ID for the Network Function')
param customLocationId string = '/subscriptions/c7bd9d96-70dd-4f61-af56-6e0abd8d80b5/resourcegroups/sunny-uksouth/providers/microsoft.extendedlocation/customlocations/nfagent-custom-location'

param location string = 'uksouth'

param nfAgentServiceBusNamespace string
param nfAgentUserAssignedIdentityClientId string
param nfagent_topic string


var deploymentValues = {
  nfAgentServiceBusNamespace: nfAgentServiceBusNamespace
  nfAgentUserAssignedIdentityClientId: nfAgentUserAssignedIdentityClientId
  nfagent_topic: nfagent_topic
  
}

resource nf_resource 'Microsoft.HybridNetwork/networkFunctions@2023-04-01-preview' = {
  name: 'nfagent-nsdg_NF2'
  location: location
  properties: {
    publisherName: publisherName
    publisherScope: 'Private'
    networkFunctionDefinitionGroupName: networkFunctionDefinitionGroupName
    networkFunctionDefinitionVersion: networkFunctionDefinitionVersion
    networkFunctionDefinitionOfferingLocation: networkFunctionDefinitionOfferingLocation
    nfviType: 'AzureArcKubernetes'
    nfviId: customLocationId
    allowSoftwareUpdate: true
    deploymentValues: string(deploymentValues)
  }
}
