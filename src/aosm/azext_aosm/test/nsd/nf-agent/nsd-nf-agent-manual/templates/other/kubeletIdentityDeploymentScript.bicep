param aksClusterName string
param aksClusterRGName string
param nfAgentMagicUAMIId string
param scriptRunnerUAMIId string
param location string = 'uksouth'
param utcValue string = utcNow()
param roleGuid string = newGuid()

// We have an AKS cluster already
// That cluster has a control plane UAMI
// We need to assign that control plane UAMI the Managed Identity Operator role over the kubelet UAMI (nfAgentMagicUAMIId)
// Then we need to assign the control plane UAMI and the kubelet UAMI to the cluster using the script
// So. We need another UAMI for the script to run as. This is created up front.
// AOSM will run this ARM template, therefore we need to pass the script UAMI to AOSM (How?) This is the one that the AOSM RP is using.
// So the script/AOSM UAMI needs the following permissions:
// 1. Contributor over the cluster
// 2. Managed Identity Operator over itself
// 3. Managed Identity Operator over the control UAMI
//
// Gave script runner UAMI the following permissions:
// 1. Owner over the cluster - a billion permissions, need to work out which ones needed
// 2. Managed Identity Operator over the magic UAMI - which means we are stuck
//
// Gave AOSM surrogates the following permissions:
// 1. Contributor over the cluster
// 2. Managed Identity Operator over script runner UAMI

var splitId = split(nfAgentMagicUAMIId, '/')
var nfAgentMagicUAMIName = splitId[8]


// This should be in the managed RG so still here
resource nfAgentMagicIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' existing = {
  name: nfAgentMagicUAMIName
}

var nfMagicIdentityClientID = nfAgentMagicIdentity.properties.clientId

// Find the existing control plane UAMI of the cluster. The cluster must have been set up with one already
// or else this will fail. It is not by default so write instructions later.
resource aks_cluster 'Microsoft.ContainerService/managedClusters@2021-07-01' existing = {
  name: aksClusterName
  scope: resourceGroup(aksClusterRGName)
}
var controlPlanePrincipalId = items(aks_cluster.identity.userAssignedIdentities)[0].value.principalId


// @description('Managed identity operator role. See https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#network-contributor')
// resource managedIdentityOperatorRole 'Microsoft.Authorization/roleDefinitions@2018-01-01-preview' existing = {
//   scope: subscription()
//   name: 'f1a07417-d97a-45cb-824c-7a7467783830'
// }

// // Assign the cluster control plane UAMI the Managed Identity Operator role over the kubelet UAMI
// resource assignmiOperatorRoleOverKubeletUAMIToControlPlaneUAMI 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
//   name: guid(resourceGroup().id) // Need to work out how to redo this - what is correct. I think if we use the same magic identity and the same guid then re-put on the SNS will work. guid('${NF.name}-${resourceGroup().id}-network-contributor')
//   scope: nfAgentMagicIdentity
//   properties: {
//     roleDefinitionId: managedIdentityOperatorRole.id
//     principalId: controlPlanePrincipalId
//     principalType: 'ServicePrincipal'
//   }
// }

resource AssignKubeletIdentityToCluster_script 'Microsoft.Resources/deploymentScripts@2020-10-01'= {
  name: 'AssignKubeletIdentityToCluster_script'
  location: location
  kind: 'AzureCLI'
  identity: {
    type: 'UserAssigned'
    // Run as the scriptRunnerUAMIId - this must have the right permissions over the cluster already and have also been passed to AOSM
    userAssignedIdentities: {
      '${scriptRunnerUAMIId}': {}
    }
  }
  properties: {
    forceUpdateTag: utcValue
    azCliVersion: '2.42.0'
    timeout: 'PT30M'
    environmentVariables: [
      {
        name: 'RESOURCE_GROUP_NAME'
        value: aksClusterRGName
      }
      {
        name: 'CLUSTER_NAME'
        value: aksClusterName
      }
      {
        name: 'KUBELET_UAMI_ID'
        value: nfAgentMagicIdentity.id
      }
    ]
    scriptContent: '''
      set -e
      shopt -s nullglob

      az account set --subscription c7bd9d96-70dd-4f61-af56-6e0abd8d80b5
      
      echo "Getting cluster credentials for ${CLUSTER_NAME}."
      az aks get-credentials --resource-group ${RESOURCE_GROUP_NAME} --name ${CLUSTER_NAME} --admin
      
      echo "Finding existing control identity of cluster."
      IDENTITY_JSON=$(az aks show -g ${RESOURCE_GROUP_NAME} --name ${CLUSTER_NAME} --query "identity")
      echo "Found identity: ${IDENTITY_JSON}"
      CONTROL_UAMI_ID=$(echo $IDENTITY_JSON | jq -r '.userAssignedIdentities | keys[0]')
      echo "Found control identity: ${CONTROL_UAMI_ID}"
      
      echo "Updating cluster kubelet identity"
      az aks update -g ${RESOURCE_GROUP_NAME} --name ${CLUSTER_NAME} --enable-managed-identity --assign-identity ${CONTROL_UAMI_ID} --assign-kubelet-identity ${KUBELET_UAMI_ID}  --yes
      
      echo "${CLUSTER_NAME} is now ready for NFM to install a NF-Agent on it."
    '''
    cleanupPreference: 'Always'
    retentionInterval: 'P1D'
  }
}

output uamiName string = nfAgentMagicUAMIName
output uamiClientID string = nfMagicIdentityClientID
