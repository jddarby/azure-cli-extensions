// Copyright (c) Microsoft Corporation.

// This file creates an Artifact Manifest for a NSD
param location string
@description('Name of an existing publisher, expected to be in the resource group where you deploy the template')
param publisherName string
@description('Name of an existing ACR-backed Artifact Store, deployed under the publisher.')
param acrArtifactStoreName string
@description('Objects representing the NF ARM template and ARM templates in the NSD. Each must have an acrManifestName, which is the name of the manifest to deploy for the ACR-backed Artifact Store (Recommended to have the NSD version as a suffix), and an armTemplateName, which is the name under which to store the ARM template in the NSD.')
param armTemplateConfig array
@description('The version that you want to name the template artifacts, in format A.B.C. e.g. 6.13.0. If testing for development, you can use any numbers you like.')
param armTemplateVersion string

resource publisher 'Microsoft.HybridNetwork/publishers@2023-09-01' existing = {
  name: publisherName
  scope: resourceGroup()
}

resource acrArtifactStore 'Microsoft.HybridNetwork/publishers/artifactStores@2023-09-01' existing = {
  parent: publisher
  name: acrArtifactStoreName
}

// This creates a separate artifact manifest for each ARM template in the NSD (including the NF ARM template)
// This is not required by AOSM but makes things simpler for the CLI.
resource acrArtifactManifests 'Microsoft.Hybridnetwork/publishers/artifactStores/artifactManifests@2023-09-01' = [for armTemplate in armTemplateConfig: {
  parent: acrArtifactStore
  name: armTemplate.acrManifestName
  location: location
  properties: {
    artifacts: [
      {
        artifactName: armTemplate.armTemplateName
        artifactType: 'ArmTemplate'
        artifactVersion: armTemplateVersion
      }
    ]
  }
}]
