// Copyright (c) Microsoft Corporation.

// This file creates an Artifact Manifest for a NSD
param location string
@description('Name of an existing publisher, expected to be in the resource group where you deploy the template')
param publisherName string 
@description('Name of an existing ACR-backed Artifact Store, deployed under the publisher.')
param acrArtifactStoreName string
@description('Name of the manifest to deploy for the ACR-backed Artifact Store')
param acrManifestName string
@description('The version that you want to name the NF template artifact, in format A-B-C. e.g. 6-13-0. Suggestion that this matches as best possible the SIMPL released version. If testing for development, you can use any numbers you like.')
param nfAgentarmTemplateVersion string = '0.1.0'
@description('Name of the NF template artifact')
var nfAgentarmTemplateName = 'nf-agent-cnf-nfdg_nfd_artifact'
@description('The version that you want to name the NF template artifact, in format A-B-C. e.g. 6-13-0. Suggestion that this matches as best possible the SIMPL released version. If testing for development, you can use any numbers you like.')
param nginxarmTemplateVersion string = '0.1.0'
@description('Name of the NF template artifact')
var nginxarmTemplateName = 'nginx-basic-test-nfdg_nfd_artifact'
@description('The version that you want to name the NF template artifact, in format A-B-C. e.g. 6-13-0. Suggestion that this matches as best possible the SIMPL released version. If testing for development, you can use any numbers you like.')
param deploymentScriptarmTemplateVersion string = '0.1.0'
@description('Name of the NF template artifact')
var deploymentScriptarmTemplateName = 'deployment_script_artifact'
param configHandlebarTemplateName string = 'confighandlebartemplate-artifact'
param configHandlebarTemplateVersion string = '0.1.0'

resource publisher 'Microsoft.HybridNetwork/publishers@2023-04-01-preview' existing = {
  name: publisherName
  scope: resourceGroup()
}

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
        artifactName: nfAgentarmTemplateName
        artifactType: 'ArmTemplate'
        artifactVersion: nfAgentarmTemplateVersion
      }
      {
        artifactName: nginxarmTemplateName
        artifactType: 'ArmTemplate'
        artifactVersion: nginxarmTemplateVersion
      }
      {
        artifactName: deploymentScriptarmTemplateName
        artifactType: 'ArmTemplate'
        artifactVersion: deploymentScriptarmTemplateVersion
      }
      {
        artifactName: configHandlebarTemplateName
        artifactType: 'OCIArtifact'
        artifactVersion: configHandlebarTemplateVersion
      }
    ]
  }
}
