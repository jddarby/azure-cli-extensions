// Copyright (c) Microsoft Corporation.

// This file creates the base AOSM resources for a CNF
param location string
@description('Name of a publisher, expected to be in the resource group where you deploy the template')
param publisherName string
param acrArtifactStoreName string
@description('Name of an Network Service Design Group')
param nsDesignGroup string

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

resource nsdGroup 'Microsoft.Hybridnetwork/publishers/networkservicedesigngroups@2023-09-01' = {
  parent: publisher
  name: nsDesignGroup
  location: location
}
