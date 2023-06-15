// Copyright (c) Microsoft Corporation. All rights reserved.
// Highly Confidential Material

// Bicep file to deploy a Site Network Service (SNS) using AOSM from a given
// published Network Service Design.
//
// The template assumes that the Publisher exists in a Resource Group in the same
// subscription as the SNS will be created.
//
param location string = resourceGroup().location
@description('The name of the Resource Group containing the publisher and NSD')
param publisherRg string = 'sunny-uksouth'
@description('The name of the publisher object where the CG Schema and nsdGroup are published')
param publisherName string = 'sunnyclipub'
@description('The version of the published NSD to use.')
param nsDesignVersion string = '0.1.0'

// # Parameters with default values, should not need to change
@description('The group that the NSDV is contained in, under the publisher.')
param nsdGroup string = 'nfagent-nsdg'
@description('The name of the existing config group schema, under the publisher')
param cgsName string = 'nfagent_nsdg_ConfigGroupSchema'
@description('The name of the nfvi site to be created. Must match the name that the designer of the NSD used.')
param nfviSiteName string = 'nfagent-nsdg_NFVI'
@description('The type of the nfvi site to be created. Must match the type that the designer of the NSD used.')
param nfviSiteType string = 'AzureCore'

// Loading the Config Group Values from file
var values = loadJsonContent('nfagent-cgv.json')

// ## Existing Resources ##
resource publisher 'Microsoft.HybridNetwork/publishers@2022-09-01-preview' existing = {
  name: publisherName
  scope: resourceGroup(publisherRg)
}

resource cgSchema 'Microsoft.Hybridnetwork/publishers/configurationGroupSchemas@2022-09-01-preview' existing = {
  parent: publisher
  name: cgsName
}

resource nsdg 'Microsoft.Hybridnetwork/publishers/networkservicedesigngroups@2022-09-01-preview' existing = {
  parent: publisher
  name: nsdGroup
}

resource nsdv 'Microsoft.Hybridnetwork/publishers/networkservicedesigngroups/networkservicedesignversions@2022-09-01-preview' existing = {
  parent: nsdg
  name: nsDesignVersion
}

// ## Creating Resources ##

// You should create as many CGV resources as appropriate for the NSD you are referencing
// resource cgValues 'Microsoft.HybridNetwork/configurationGroupValues@2022-09-01-preview' = {
//   name: 'nfagent-cgvs'

//   location: location
//   properties: {
//     configurationGroupValueSchemaReference: {
//       id: cgSchema.id
//     }
//     configurationValue: string(values)
//   }
// }

resource cgValues 'Microsoft.HybridNetwork/configurationGroupValues@2022-09-01-preview' = {
  name: 'nfagent-cgvs'
  location: location
  properties: {
    publisherName: publisherName
    publisherScope: 'Private'
    configurationGroupValueSchemaName: cgSchema.name
    configurationGroupSchemaOfferingLocation: location
    configurationValue: string(values)
  }
}

'

resource site 'Microsoft.HybridNetwork/sites@2022-09-01-preview' = {
  name: 'nfagent-site'
  location: location
  properties: {
    nfvis : [
      {
        name: nfviSiteName
        nfviType: nfviSiteType
        location: location
      }
    ]
  }
}

resource sns 'Microsoft.HybridNetwork/sitenetworkservices@2023-04-01-preview' = {
  name: 'nfagent-sns'
  location: location
  // identity: {
  //   type: 'UserAssigned'
  //   userAssignedIdentities: {
  //     '/subscriptions/c7bd9d96-70dd-4f61-af56-6e0abd8d80b5/resourcegroups/sunny-uksouth/providers/Microsoft.ManagedIdentity/userAssignedIdentities/nfagent-script-uami': {}
  //   }
  // }
  properties: {
    siteReference: {
      id: site.id
    }
    publisherName: publisherName
    publisherScope: 'Private'
    networkServiceDesignGroupName: nsdGroup
    networkServiceDesignVersionName: nsDesignVersion
    networkServiceDesignVersionOfferingLocation: location
    desiredStateConfigurationGroupValueReferences: {
      nfagent_nsdg_ConfigGroupSchema: {
        id: cgValues.id
      }
    }
  }
}
