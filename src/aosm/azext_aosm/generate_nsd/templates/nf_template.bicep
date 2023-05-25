// Copyright (c) Microsoft Corporation. All rights reserved.
// Highly Confidential Material
//
// The template that the NSD invokes to create the SIMPL NF from a published NFDV. 
// Should be built to ARM (json) and uploaded to the artifact store for the NSDV using the 
// artifact manifest
@description('Publisher where the SIMPL NFD is published')
param publisherName string

@description('NFD Group name for the SIMPL NFD')
param networkFunctionDefinitionGroupName string

@description('NFD version for the SIMPL NFDV')
param networkFunctionDefinitionVersion string

@description('Offering location for the SIMPL NF')
param networkFunctionDefinitionOfferingLocation string

param resourceGroupId string = resourceGroup().id
param location string = resourceGroup().location

{{bicep_params}}

// Defined in simpl-nfd/configMappings/simplTemplateParameters.json
var deploymentValues = {
  {{deploymentValues}}
}

// deploys single resource (NF which is SIMPL)
resource simpl_nf_resource 'Microsoft.HybridNetwork/networkFunctions@2022-09-01-preview' = {
  //TODO: this was different
  name: 'simplVMName-nf'
  location: location
  properties: {
    publisherName: publisherName
    publisherScope: 'Private'
    networkFunctionDefinitionGroupName: networkFunctionDefinitionGroupName
    networkFunctionDefinitionVersion: networkFunctionDefinitionVersion
    networkFunctionDefinitionOfferingLocation: networkFunctionDefinitionOfferingLocation//
    nfviType: 'AzureCore'
    nfviId: resourceGroupId//
    allowSoftwareUpdate: true
    deploymentValues: string(deploymentValues)
  }
}
