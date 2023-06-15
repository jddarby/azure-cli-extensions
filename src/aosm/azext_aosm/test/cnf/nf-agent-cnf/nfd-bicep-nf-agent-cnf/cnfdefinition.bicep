// Copyright (c) Microsoft Corporation.

// This file creates an NF definition for a CNF
param location string
@description('Name of an existing publisher, expected to be in the resource group where you deploy the template')
param publisherName string
@description('Name of an existing ACR-backed Artifact Store, deployed under the publisher.')
param acrArtifactStoreName string
@description('Name of an existing Network Function Definition Group')
param nfDefinitionGroup string
@description('The version of the NFDV you want to deploy, in format A-B-C')
param nfDefinitionVersion string

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

// Created by the az aosm definition publish command before the template is deployed
resource nfdg 'Microsoft.Hybridnetwork/publishers/networkfunctiondefinitiongroups@2023-04-01-preview' existing = {
  parent: publisher
  name: nfDefinitionGroup
}

resource nfdv 'Microsoft.Hybridnetwork/publishers/networkfunctiondefinitiongroups/networkfunctiondefinitionversions@2023-04-01-preview' = {
  parent: nfdg
  name: nfDefinitionVersion
  location: location
  properties: {
    // versionState should be changed to 'Active' once it is finalized.
    versionState: 'Preview'
    deployParameters: string(loadJsonContent('schemas/deploymentParameters.json'))
    networkFunctionType: 'ContainerizedNetworkFunction'
    networkFunctionTemplate: {
      nfviType: 'AzureArcKubernetes'
      networkFunctionApplications: [
        {
          artifactType: 'HelmPackage'
          name: 'nf-agent-cnf'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'nf-agent-cnf'
              helmPackageVersionRange: '0.1.0'
              registryValuesPaths: [
                'image.repository'
              ]
              imagePullSecretsValuesPaths: [
                'imagePullSecrets'
              ]
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'nf-agent-cnf'
              releaseName: 'nf-agent-cnf'
              helmPackageVersion: '0.1.0'
              values: string(loadJsonContent('configMappings/nf-agent-cnf-mappings.json'))
            }
          }
        }
      ]
    }
  }
}
