// Copyright (c) Microsoft Corporation.

// This file creates an NF definition for a CNF
param location string
@description('Name of an existing publisher, expected to be in the resource group where you deploy the template')
param publisherName string
@description('Name of an existing ACR-backed Artifact Store, deployed under the publisher.')
param acrArtifactStoreName string
@description('Name of an existing Network Function Definition Group')
param nfDefinitionGroup string
@description('The version of the NFDV you want to deploy, in format A.B.C')
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
          name: 'fed-crds'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-crds'
              helmPackageVersionRange: '4.2.0-43-rel-4-2-0'
              registryValuesPaths: []
              imagePullSecretsValuesPaths: []
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-crds'
              releaseName: 'fed-crds'
              helmPackageVersion: '4.2.0-43-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-crds-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-rbac'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-rbac'
              helmPackageVersionRange: '4.2.0-42-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-rbac'
              releaseName: 'fed-rbac'
              helmPackageVersion: '4.2.0-42-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-rbac-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-kube_addons'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-kube_addons'
              helmPackageVersionRange: '4.2.0-48-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-kube_addons'
              releaseName: 'fed-kube_addons'
              helmPackageVersion: '4.2.0-48-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-kube_addons-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-opa'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-opa'
              helmPackageVersionRange: '4.2.0-46-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-opa'
              releaseName: 'fed-opa'
              helmPackageVersion: '4.2.0-46-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-opa-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-paas_helpers'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-paas_helpers'
              helmPackageVersionRange: '4.2.0-52-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-paas_helpers'
              releaseName: 'fed-paas_helpers'
              helmPackageVersion: '4.2.0-52-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-paas_helpers-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-istio'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-istio'
              helmPackageVersionRange: '4.2.0-52-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-istio'
              releaseName: 'fed-istio'
              helmPackageVersion: '4.2.0-52-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-istio-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-service_reg'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-service_reg'
              helmPackageVersionRange: '4.2.0-52-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-service_reg'
              releaseName: 'fed-service_reg'
              helmPackageVersion: '4.2.0-52-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-service_reg-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-grafana'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-grafana'
              helmPackageVersionRange: '4.2.0-51-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-grafana'
              releaseName: 'fed-grafana'
              helmPackageVersion: '4.2.0-51-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-grafana-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-prometheus'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-prometheus'
              helmPackageVersionRange: '4.2.0-51-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-prometheus'
              releaseName: 'fed-prometheus'
              helmPackageVersion: '4.2.0-51-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-prometheus-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-db_etcd'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-db_etcd'
              helmPackageVersionRange: '4.2.0-45-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-db_etcd'
              releaseName: 'fed-db_etcd'
              helmPackageVersion: '4.2.0-45-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-db_etcd-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-redis_operator'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-redis_operator'
              helmPackageVersionRange: '4.2.0-42-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-redis_operator'
              releaseName: 'fed-redis_operator'
              helmPackageVersion: '4.2.0-42-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-redis_operator-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-redis_cluster'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-redis_cluster'
              helmPackageVersionRange: '4.2.0-54-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-redis_cluster'
              releaseName: 'fed-redis_cluster'
              helmPackageVersion: '4.2.0-54-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-redis_cluster-mappings.json'))
            }
          }
        }
        {
          artifactType: 'HelmPackage'
          name: 'fed-smf'
          dependsOnProfile: {
            installDependsOn: []
          }
          artifactProfile: {
            artifactStore: {
              id: acrArtifactStore.id
            }
            helmArtifactProfile: {
              helmPackageName: 'fed-smf'
              helmPackageVersionRange: '4.2.0-56-rel-4-2-0'
              registryValuesPaths: ['global.registry.docker.repoPath']
              imagePullSecretsValuesPaths: ['global.registry.docker.imagePullSecrets', 'global.registry.docker.imagePullSecret']
            }
          }
          deployParametersMappingRuleProfile: {
            applicationEnablement: 'Enabled'
            helmMappingRuleProfile: {
              releaseNamespace: 'fed-smf'
              releaseName: 'fed-smf'
              helmPackageVersion: '4.2.0-56-rel-4-2-0'
              values: string(loadJsonContent('configMappings/fed-smf-mappings.json'))
            }
          }
        }
      ]
    }
  }
}