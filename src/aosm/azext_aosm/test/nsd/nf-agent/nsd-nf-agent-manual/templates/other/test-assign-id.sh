#bin/bash
set -e
shopt -s nullglob

echo "Getting cluster credentials for ${CLUSTER_NAME}."
az aks get-credentials --resource-group ${RESOURCE_GROUP_NAME} --name ${CLUSTER_NAME}

echo "Finding existing control identity of cluster."
IDENTITY_JSON=$(az aks show -g ${RESOURCE_GROUP_NAME} --name ${CLUSTER_NAME} --query "identity")
echo "Found identity: ${IDENTITY_JSON}"
CONTROL_UAMI_ID=$(echo $IDENTITY_JSON | jq -r '.userAssignedIdentities | keys[0]')
echo "Found control identity: ${CONTROL_UAMI_ID}"

echo "Updating cluster kubelet identity"
az aks update -g ${RESOURCE_GROUP_NAME} --name ${CLUSTER_NAME} --enable-managed-identity --assign-identity ${CONTROL_UAMI_ID} --assign-kubelet-identity ${KUBELET_IDENTITY_ID}  --yes

echo "${CLUSTER_NAME} is now ready for NFM to install a NF-Agent on it."
