#!/bin/bash
# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material

# Script for downloading Helm charts from an ACR.
# Requires the following CLI tools:
#   - helm v3 (install instructions are here https://helm.sh/docs/intro/install/)
#   - az (install instructions are here https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)

### PRE-REQUISITES ###
# You have appropriate access rights and logged into Azure using:
#     az login

### ASSUMPTIONS ###
# This script assumes that:
# - Your default Azure subscription for `az` commands is the one relevant to these
#   commands, containing the repositories and storage accounts to upload to.

# Note on the behaviour of this script.
#   This script downloads all artifacts found in a repo where the mediaType in the manifest contains application/vnd.cncf.helm

set -e
shopt -s nullglob

#ACR_NAME=xybiceppublisher4xybicepartifactstore4d907d600ba35

print_usage() {
    echo "Usage: ${0} -n ACR_NAME"
    echo
    echo "  -n    [Required] : The name of the destination ACR to upload helm charts and docker images to."
    echo "                     Optionally include the '.azurecr.io' suffix."
    echo "  -h               : Print this help text and exit."
}

# Parse arguments
while getopts 'n:h' option; do
    case "${option}" in
    n)
        ACR_NAME="${OPTARG,,}" # Must be lowercase.
        ACR_NAME="${ACR_NAME%.azurecr.io}" # Strip the suffix if provided.
        ;;
    h)
        print_usage
        exit
        ;;
    \?)
        echo "Invalid option: -$OPTARG"
        echo
        print_usage
        exit 1
        ;;
    :)
        echo "Option -$OPTARG requires an argument"
        echo
        print_usage
        exit 1
        ;;
    *)
        print_usage
        exit 1
        ;;
    esac
done

# Check arguments.
if [ -z "$ACR_NAME" ]; then
    echo "Missing required argument: -n ACR_NAME"
    echo
    print_usage
    exit 1
fi


# Check required tools are installed.
helm version
az --version

# Ensure we run upload logic from the root of the release package.
echo "Downloading helm chart artifacts from $ACR_NAME"

# Log in to ACRs.
echo "Logging in to ACR $ACR_NAME"

# Login with the docker client.
az acr login --name "$ACR_NAME"

# Login with helm. This first requires another `az acr login` with flags set to get a token, which results in not
# using the docker client and therefore doesn't function as a docker login.
ACR_TOKEN=$(az acr login --name "$ACR_NAME" --expose-token --output tsv --query accessToken)
echo "Logging in using helm registry login"
helm registry login "${ACR_NAME}.azurecr.io" --username 00000000-0000-0000-0000-000000000000 \
                                            --password-stdin <<< "$ACR_TOKEN"

# List all the repositories in the ACR
REPO_LIST_ACR=$(az acr repository list --name "$ACR_NAME" --output tsv --query "[]")

echo "The list of repos is $REPO_LIST_ACR"

for REPO in $REPO_LIST_ACR
do
    # TEMPORARY - TODO change later
    if [[ $REPO == "fed"* ]]; then
        echo "Looking for helm charts in $REPO"
        REPO_TAGS=$(az acr repository show-tags --name "$ACR_NAME" --repository "$REPO" --output tsv --query "[]")

        for TAG in $REPO_TAGS
        do
            echo "Checking if $TAG is a helm chart"
            MANIFEST_TYPE=$(az acr manifest show -r "$ACR_NAME" -n "$REPO:$TAG" --query "config.mediaType")
            if [[ $MANIFEST_TYPE == *"application/vnd.cncf.helm"* ]]; then
                echo "helm repo found as manifest type is $MANIFEST_TYPE which contains application/vnd.cncf.helm"
                echo "Downloading helm chart with tag $TAG from $REPO"
                # helm pull oci://xybiceppublisher4xybicepartifactstore4d907d600ba35.azurecr.io/fed-crds --version 4.2.0-43-rel-4-2-0
                HELM_CHART_SOURCE="oci://${ACR_NAME}.azurecr.io/${REPO}"
                helm pull "${HELM_CHART_SOURCE}" --version "$TAG"
            else
                echo "helm repo not found as manifest type is $MANIFEST_TYPE"
            fi
        done
    fi
done

# Seems a good idea to logout
echo "Logout from registry"
helm registry logout "${ACR_NAME}.azurecr.io"
