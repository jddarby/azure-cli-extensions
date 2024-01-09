// Copyright (c) Microsoft Corporation.

// This file creates the base AOSM resources for a VNF
param location string
@description('Name of a publisher, expected to be in the resource group where you deploy the template')
param publisherName string
@description('Name of an ACR-backed Artifact Store, deployed under the publisher.')
param acrArtifactStoreName string
@description('Name of a Storage Account-backed Artifact Store, deployed under the publisher.')
param saArtifactStoreName string
@description('Name of a Network Function Definition Group')
param nfDefinitionGroup string

resource publisher 'Microsoft.HybridNetwork/publishers@2023-09-01' = {
  name: publisherName
  location: location
  properties: { scope: 'Private'}
}

resource acrArtifactStore 'Microsoft.HybridNetwork/publishers/artifactStores@2023-09-01' = {
  parent: publisher
  name: acrArtifactStoreName
  location: location
}

resource saArtifactStore 'Microsoft.HybridNetwork/publishers/artifactStores@2023-09-01' = {
  parent: publisher
  name: saArtifactStoreName
  location: location
}

resource nfdg 'Microsoft.Hybridnetwork/publishers/networkfunctiondefinitiongroups@2023-09-01' = {
  parent: publisher
  name: nfDefinitionGroup
  location: location
}
