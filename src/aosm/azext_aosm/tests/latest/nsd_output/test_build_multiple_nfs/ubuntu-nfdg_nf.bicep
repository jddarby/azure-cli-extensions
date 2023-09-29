// Copyright (c) Microsoft Corporation. All rights reserved.
// Highly Confidential Material
//
// The template that the NSD invokes to create the Network Function from a published NFDV.

@description('Publisher where the NFD is published')
param publisherName string = 'reference-publisher'

@description('NFD Group name for the Network Function')
param networkFunctionDefinitionGroupName string = 'ubuntu-nfdg'

@description('NFD version')
param ubuntu_nfdg_nfd_version string

@description('Offering location for the Network Function')
param networkFunctionDefinitionOfferingLocation string = 'eastus'

@description('The managed identity that should be used to create the NF.')
param managedIdentity string

param location string = 'eastus'

param nfviType string = 'AzureCore'

param resourceGroupId string = resourceGroup().id

param deploymentParameters array

var identityObject = (managedIdentity == '')  ? {
  type: 'SystemAssigned'
} : {
  type: 'UserAssigned'
  userAssignedIdentities: {
    '${managedIdentity}': {}
  }
}

resource nf_resource 'Microsoft.HybridNetwork/networkFunctions@2023-09-01' = [for (values, i) in deploymentParameters: {
  name: 'ubuntu-nfdg${i}'
  location: location
  identity: identityObject
  properties: {
    publisherName: publisherName
    publisherScope: 'Private'
    networkFunctionDefinitionGroupName: networkFunctionDefinitionGroupName
    networkFunctionDefinitionVersion: ubuntu_nfdg_nfd_version
    networkFunctionDefinitionOfferingLocation: networkFunctionDefinitionOfferingLocation
    nfviType: nfviType
    nfviId: resourceGroupId
    allowSoftwareUpdate: true
    deploymentValues: string(values)
  }
}]