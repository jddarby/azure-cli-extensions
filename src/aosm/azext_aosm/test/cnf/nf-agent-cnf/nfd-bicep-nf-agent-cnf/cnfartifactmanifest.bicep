// Copyright (c) Microsoft Corporation.

// This file creates an Artifact Manifest for a CNF
param location string
@description('Name of an existing publisher, expected to be in the resource group where you deploy the template')
param publisherName string 
@description('Name of an existing ACR-backed Artifact Store, deployed under the publisher.')
param acrArtifactStoreName string
@description('Name of the manifest to deploy for the ACR-backed Artifact Store')
param acrManifestName string

// Created by the az aosm definition publish command before the template is deployed
resource publisher 'Microsoft.HybridNetwork/publishers@2023-04-01-preview' existing = {
  name: publisherName
  scope: resourceGroup()
}

// Created by the az aosm definition publish command before the template is deployed
resource acrArtifactStore 'Microsoft.HybridNetwork/publishers/artifactStores@2023-04-01-preview' existing = {
  parent: publisher
  name: acrArtifactStoreName
}

resource acrArtifactManifest 'Microsoft.Hybridnetwork/publishers/artifactStores/artifactManifests@2023-04-01-preview' = {
  parent: acrArtifactStore
  name: acrManifestName
  location: location
  properties: {
    artifacts: [
      {
        artifactName: 'nf-agent-cnf'
        artifactType: 'OCIArtifact'
        artifactVersion: '0.1.0'
      }
      {
        artifactName: 'pez-nfagent'
        artifactType: 'OCIArtifact'
        artifactVersion: '879624'
      }
    ]
  }
}
