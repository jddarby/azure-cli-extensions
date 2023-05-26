// Copyright (c) Microsoft Corporation. All rights reserved.
// Highly Confidential Material
//
// The template that the NSD invokes to create the Network Function from a published NFDV. 

@description('Publisher where the NFD is published')
param publisherName string

@description('NFD Group name for the Network Function')
param networkFunctionDefinitionGroupName string

@description('NFD version')
param networkFunctionDefinitionVersion string

@description('Offering location for the Network Function')
param networkFunctionDefinitionOfferingLocation string

param resourceGroupId string = resourceGroup().id
param location string

param simplVmName string
param simplVmUserAssignedIdentityResourceId string
param vmSizeSku string
param imageName string
param existingPersistentDiskResourceName string
param existingPersistentDiskResourceGroup string
param azureDeployLocation string
param vnetName string
param vnetResourceGroup string
param subnetName string
param managementIp string
param sshPublicKeyAdmin string
param sshPublicKeySecretsMgmt string
param sshPublicKeyLifecycleMgmt string
param osDiskEncryptionSetName string
param osDiskEncryptionSetRG string
param simplVmTagName string
param simplVmTagValue string
param remoteSyslogServerAddress string
param remoteSyslogServerPort string
param simonMgmtIp string
param fluentdServerSingleAddress string
param nfAgentServiceBusNamespace string
param nfAgentUserAssignedIdentityResourceId string


var deploymentValues = {
    simplVmName: simplVmName
  simplVmUserAssignedIdentityResourceId: simplVmUserAssignedIdentityResourceId
  vmSizeSku: vmSizeSku
  imageName: imageName
  existingPersistentDiskResourceName: existingPersistentDiskResourceName
  existingPersistentDiskResourceGroup: existingPersistentDiskResourceGroup
  azureDeployLocation: azureDeployLocation
  vnetName: vnetName
  vnetResourceGroup: vnetResourceGroup
  subnetName: subnetName
  managementIp: managementIp
  sshPublicKeyAdmin: sshPublicKeyAdmin
  sshPublicKeySecretsMgmt: sshPublicKeySecretsMgmt
  sshPublicKeyLifecycleMgmt: sshPublicKeyLifecycleMgmt
  osDiskEncryptionSetName: osDiskEncryptionSetName
  osDiskEncryptionSetRG: osDiskEncryptionSetRG
  simplVmTagName: simplVmTagName
  simplVmTagValue: simplVmTagValue
  remoteSyslogServerAddress: remoteSyslogServerAddress
  remoteSyslogServerPort: remoteSyslogServerPort
  simonMgmtIp: simonMgmtIp
  fluentdServerSingleAddress: fluentdServerSingleAddress
  nfAgentServiceBusNamespace: nfAgentServiceBusNamespace
  nfAgentUserAssignedIdentityResourceId: nfAgentUserAssignedIdentityResourceId

}

resource nf_resource 'Microsoft.HybridNetwork/networkFunctions@2023-04-01-preview' = {
  name: 'simplVM_NF'
  location: location
  properties: {
    publisherName: publisherName
    publisherScope: 'Private'
    networkFunctionDefinitionGroupName: networkFunctionDefinitionGroupName
    networkFunctionDefinitionVersion: networkFunctionDefinitionVersion
    networkFunctionDefinitionOfferingLocation: networkFunctionDefinitionOfferingLocation//
    nfviType: 'AzureCore'
    nfviId: resourceGroupId
    allowSoftwareUpdate: true
    deploymentValues: string(deploymentValues)
  }
}