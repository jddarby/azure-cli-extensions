// Copyright (c) Microsoft Corporation. All rights reserved.
// Highly Confidential Material
//
// Bicep template for deploying SIMPL VM either using AOSM or using the ARM CLI.
// If using AOSM, this becomes the body of the SIMPL Network Function Definition.
//
// Parameters vary slightly depending on deployment method due to:
// - AOSM has a separate disk template to allow SIMPL upgrade without losing the CSAR 
//   disk - required because NFM blows away the whole NF on upgrade. So disk resource
//   expected to be provided as parameters if using AOSM
// - NFM currently only supports string, integer and bool parameters, although this is
//   being fixed.
@description('Unique name for the SIMPL VM')
param simplVmName string = 'SIMPL-VM'

@description('VM SKU. Must be available in the azure region and subscription you are deploying to.')
param vmSizeSku string = 'Standard_D2s_v3'

@description('Fully qualified resource ID for a user assigned managed identity which SIMPL VM will use to interact with ARM')
param simplVmUserAssignedIdentityResourceId string

@description('The name of the resource group that the SIMPL VM image exists in.')
param imageResourceGroup string = resourceGroup().name

// new default
@description('The name of the SIMPL VM image')
param imageName string = 'simpl-vm-image'

@description('(AOSM required) Existing persistent disk resource name. If not provided the disk will be created.')
param existingPersistentDiskResourceName string = ''

@description('(AOSM required) Existing persistent disk resource group name. If not provided the disk will be created.')
param existingPersistentDiskResourceGroup string = ''

@description('The size in GiB to make the persistent data disk on the SIMPL VM.')
param simplVmDiskSizeGiB int = 128

@description('Azure region to deploy SIMPL VM into. Valid values can be found using `az account list-locations` and then using the "name".')
param azureDeployLocation string = resourceGroup().location

@description('The name of the Resource Group containing the Virtual Network that this SIMPL VM will use.')
param vnetResourceGroup string = ''

@description('The name of the Virtual Network the SIMPL VM is going to use for its management network. It must exist within the vnetResourceGroup specified.')
param vnetName string = ''

// new default
@description('The name of the subnet the SIMPL VM is going to use for its management network, which must exist in the vnet specified by the vnetName parameter. e.g. mgmt-subnet-10-1-0-0-24')
param subnetName string = 'mgmt'

@description('The management IP address of the SIMPL VM, which must be an available address on the subnet referenced by the subnetName parameter.')
param managementIp string

@secure()
@description('The public key of the SSH key pair used for logging onto the VM as the admin user')
param sshPublicKeyAdmin string

@secure()
@description('The public key of the SSH key pair used for logging onto the VM as the secrets-mgmt user. If not provided there won\'t be a key added and you won\'t be able to ssh on as the secrets-mgmt user. You can add a key manually later as the admin user.')
param sshPublicKeySecretsMgmt string = ''

@secure()
@description('The public key of the SSH key pair used for logging onto the VM as the lifecycle-mgmt user. If not provided there won\'t be a key added and you won\'t be able to ssh on as the lifecycle-mgmt user. You can add a key manually later as the admin user.')
param sshPublicKeyLifecycleMgmt string = ''

@description('(Optional) The name of the disk encryption set to use for encrypting the CSAR disk with a customer managed encryption key. An empty string will default to using a platform managed key for the CSAR disk. Only use if a customer managed key is required. The customer will then own management of the key, for example key rotation. This can be the same as the OS disk encryption set.')
param persistentDiskEncryptionSetName string = ''

@description('(Optional) The resource group containing the disk encryption set to use if encrypting the external CSAR disk with a customer managed encryption key.')
param persistentDiskEncryptionSetRG string = ''

@description('(Optional) The name of the disk encryption set to use for encrypting the OS disk with a customer managed encryption key. An empty string will default to using a platform managed key for the OS disk. Only use if a customer managed key is required. The customer will then own management of the key, for example key rotation. This can be the same as the CSAR disk encryption set.')
param osDiskEncryptionSetName string = ''

@description('(Optional) The resource group containing the disk encryption set to use if encrypting the OS disk with a customer managed encryption key.')
param osDiskEncryptionSetRG string = ''

@description('(Optional) The FQDN or IP address of the remote syslog server.')
param remoteSyslogServerAddress string = ''

@description('(Optional) The port of the remote syslog server.')
param remoteSyslogServerPort string = ''

//AOSM doesn't support JSON objects. ARM CLI deploy does
@description('(Optional) (Non-AOSM only) tags to apply to the SIMPL VM Virtual Machine, NICs, and disks on creation. Tags are ARM objects containing key-value pairs, eg, {\'ExampleTag1\':\'ExampleValue1\',\'ExampleTag2\':\'ExampleValue2\'}')
param simplVmTags object = {
}

//AOSM doesn't support JSON objects. So for AOSM a tag can only be provided as a single key and value
@description('(Optional) (AOSM only) single tag name to apply to the SIMPL VM Virtual Machine, NICs, and disks on creation.')
param simplVmTagName string = ''
@description('(Optional) (AOSM only) single tag value to apply to the SIMPL VM Virtual Machine, NICs, and disks on creation.')
param simplVmTagValue string = ''

@description('(Optional) The IP of the SIMon instance used to monitor SIMPL VM.')
param simonMgmtIp string = ''

//AOSM doesn't support arrays. ARM CLI does and this makes the template back compatible
@description('(Optional) (Non-AOSM only) An array of remote fluentd log collector IP addresses.')
param fluentdServerAddresses array = []

//@@@ AOSM only
@description('(Optional) (AOSM only) A single remote fluentd log collector IP addresses.')
param fluentdServerSingleAddress string = ''

@description('(Optional) (AOSM only) The namespace of the Service Bus that the integrated NF Agent should connect to.')
param nfAgentServiceBusNamespace string = ''

@description('(Optional) (AOSM only) Fully qualified resource ID for a user assigned managed identity which the integrated NF Agent will use to interact with the Service Bus.')
param nfAgentUserAssignedIdentityResourceId string = ''

var managedIdentities = (simplVmUserAssignedIdentityResourceId == '' && nfAgentUserAssignedIdentityResourceId == '') ? null : {
  type: 'UserAssigned'
  userAssignedIdentities: union(
    (simplVmUserAssignedIdentityResourceId == '') ? {} : { '${simplVmUserAssignedIdentityResourceId}': {} },
    (nfAgentUserAssignedIdentityResourceId == '') ? {} : { '${nfAgentUserAssignedIdentityResourceId}': {} }
  )
}

// AOSM build up tags object
var simplVmObjectTags = (simplVmTags == {} && simplVmTagName != '')  ? {
  '${simplVmTagName}': simplVmTagValue
} : simplVmTags
// AOSM build up fluentdServer array
var fluentdServerAddressArray = (fluentdServerAddresses != []) ? fluentdServerAddresses : (fluentdServerSingleAddress != '') ? [fluentdServerSingleAddress] : []

var subnetId = '/subscriptions/${subscription().subscriptionId}/resourceGroups/${vnetResourceGroup}/providers/Microsoft.Network/virtualNetworks/${vnetName}/subnets/${subnetName}'

// Create the management nic
resource simplVmName_nic 'Microsoft.Network/networkInterfaces@2021-05-01' = {
  name: '${simplVmName}_nic'
  location: azureDeployLocation
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          privateIPAddress: managementIp
          privateIPAllocationMethod: 'Static'
          subnet: {
            id: subnetId
          }
          primary: true
          privateIPAddressVersion: 'IPv4'
        }
      }
    ]
  }
  tags: simplVmObjectTags
}

// Create the persistent disk unless an existing one has been passed in
resource simplVmName_persistent_disk 'Microsoft.Compute/disks@2021-12-01' = if (existingPersistentDiskResourceName == '') {
  name: '${simplVmName}_persistent_disk'
  location: azureDeployLocation
  sku: {
    name: 'Premium_LRS'
  }
  properties: {
    creationData: {
      createOption: 'Empty'
    }
    diskSizeGB: simplVmDiskSizeGiB
    encryption: ((persistentDiskEncryptionSetName == '') ? json('{"type": "EncryptionAtRestWithPlatformKey"}') : json('{"type": "EncryptionAtRestWithCustomerKey", "diskEncryptionSetId": "${extensionResourceId('/subscriptions/${subscription().subscriptionId}/resourceGroups/${persistentDiskEncryptionSetRG}', 'Microsoft.Compute/diskEncryptionSets', persistentDiskEncryptionSetName)}"}'))
  }
  tags: simplVmObjectTags
}

// AOSM case we expect the disk to exist already and be passed in as a resource name and RG
resource existing_disk 'Microsoft.Compute/disks@2021-12-01' existing = if ((existingPersistentDiskResourceName != '') && (existingPersistentDiskResourceGroup != '')) {
  scope: resourceGroup(existingPersistentDiskResourceGroup)
  name: existingPersistentDiskResourceName
}

// Create the VM, attaching the disk and nic
resource simplVmVirtualMachine 'Microsoft.Compute/virtualMachines@2021-07-01' = {
  name: simplVmName
  location: azureDeployLocation
  identity: managedIdentities
  properties: {
    hardwareProfile: {
      vmSize: vmSizeSku
    }
    storageProfile: {
      imageReference: {
        id: extensionResourceId('/subscriptions/${subscription().subscriptionId}/resourceGroups/${imageResourceGroup}', 'Microsoft.Compute/images', imageName)
      }
      osDisk: {
        osType: 'Linux'
        name: '${simplVmName}_disk'
        createOption: 'FromImage'
        caching: 'ReadWrite'
        writeAcceleratorEnabled: false
        managedDisk: ((osDiskEncryptionSetName == '') ? json('{"storageAccountType": "Premium_LRS"}') : json('{"storageAccountType": "Premium_LRS", "diskEncryptionSet": { "id": "${extensionResourceId('/subscriptions/${subscription().subscriptionId}/resourceGroups/${osDiskEncryptionSetRG}', 'Microsoft.Compute/diskEncryptionSets', osDiskEncryptionSetName)}"}}'))
        deleteOption: 'Delete'
        diskSizeGB: 30
      }
      dataDisks: [
        {
          lun: 1
          name: ((existingPersistentDiskResourceName == '') ? '${simplVmName}_persistent_disk' : existingPersistentDiskResourceName)
          createOption: 'Attach'
          caching: 'None'
          writeAcceleratorEnabled: false
          managedDisk: {
            id: ((existingPersistentDiskResourceName == '') ? simplVmName_persistent_disk.id : existing_disk.id)
          }
          deleteOption: 'Detach'
        }
      ]
    }
    osProfile: {
      computerName: simplVmName
      adminUsername: 'azureuser'
      linuxConfiguration: {
        disablePasswordAuthentication: true
        ssh: {
          publicKeys: [
            {
              path: '/home/azureuser/.ssh/authorized_keys'
              keyData: sshPublicKeyAdmin
            }
          ]
        }
        provisionVMAgent: true
        patchSettings: {
          patchMode: 'ImageDefault'
          assessmentMode: 'ImageDefault'
        }
      }
      secrets: []
      allowExtensionOperations: true
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: simplVmName_nic.id
        }
      ]
    }
    userData: base64('#cloud-config:\nusers:\n# Ensure we include the default centos user, this is specifically so that RADIUS authentication works if needed\n- default\n- name: centos\n  sudo: "ALL=(ALL) NOPASSWD: ALL"\n- name: secrets-mgmt\n  homedir: /home/secrets-mgmt\n  lock_passwd: False\n  gecos: secrets-mgmt\n  primary_group: admin\n- name: lifecycle-mgmt\n  homedir: /home/lifecycle-mgmt\n  lock_passwd: False\n  primary_group: admin\n  gecos: lifecycle-mgmt\nwrite_files:\n# This is used to set up networking\n- path: /etc/network_definitions.yaml\n  owner: root:root\n  permissions: "0644"\n  content: |\n        hostname: simpl-vm\n        networks:\n          mgmt:\n                hw_address: $MGMT_MAC_ADDRESS\n                default: True\n                ipv4:\n                  $VCLOUD_MANAGEMENT_ADDRESS_CFG\n                  $VCLOUD_MANAGEMENT_SUBNET_CFG\n                  $VCLOUD_MANAGEMENT_GW_CFG\n- path: /etc/vm_config.yaml\n  owner: root:root\n  # Make these readable only by root as they may contain sensitive information.\n  permissions: "0600"\n  content: |\n    dns:\n      nameservers: ["168.63.129.16"]\n    remote_syslog:\n        address: ${remoteSyslogServerAddress}\n        port: ${remoteSyslogServerPort}\n        filters: ["$syslogtag == \'/var/log/audit/audit.log:\'", "$syslogfacility-text == \'authpriv\'"]\n    volume_definitions:\n      csar: 1\n    logging:\n      elasticsearch:\n        host: ${simonMgmtIp}\n      fluentd:\n        server_addresses: ${fluentdServerAddressArray}\n- path: /etc/nfagent_config.yaml\n  owner: root:root\n  permissions: "0600"\n  content: |\n    nf_agent:\n      service_bus_namespace: ${nfAgentServiceBusNamespace}\n      identity_resource_id: ${((nfAgentUserAssignedIdentityResourceId == '') ? '' : reference(nfAgentUserAssignedIdentityResourceId, '2018-11-30').clientId)}\n- path: /home/admin/qsg_config.yaml\n  owner: msw-qss:secrets-mgmt\n  # Make these readable and writable by owner and group.\n  permissions: "0664"\n  content: |\n    secret_backends:\n        keys: Local\n        certs: Local\n        freeforms: Local\n        qls_backend:\n            qls_url: http://0.0.0.0:8090\n\nruncmd:\n# Force cloud-init to fail if any of these commands fail.\n- set -euo pipefail\n# If NF Agent parameters are set, prepare config and create the log directory.\n- if [[ "${nfAgentServiceBusNamespace}" != "" ]]; then\n- echo "Enabling NF Agent"\n- nf_agent_config_file=/etc/nfagent_config.yaml\n- mkdir -m 0775 -p /var/log/nf-agent/\n- chown -R admin /var/log/nf-agent/\n- chgrp -R admin /var/log/nf-agent/\n- else\n- nf_agent_config_file=""\n- fi\n# Generate config sets up DNS and Syslog for SIMPL, as well as the NF Agent if configured above\n- generate_config --settings /etc/vm_config.yaml /etc/network_definitions.yaml $nf_agent_config_file\n- set_audit_rules --enable-syslog --all-users; sudo systemctl restart rsyslog\n# Set up networking\n- echo "About to configure networks"\n- /usr/bin/configure_networks.py\n# Ensure the startup folder exists so we can create files in there later.\n- echo "Create directory /var/lib/startup for tracking progress"\n- mkdir -p /var/lib/startup\n# Run the VPNstart script - not on VMware this always runs\n- echo "Run VPNstart script"\n- sudo /etc/init.d/VPNstart\n# Allow the admin user to run docker\n- echo "Allow admin user to run docker"\n- usermod -aG docker admin\n# Handle the case where the id_rsa was already created, (which seems unlikely)\n# Delete the id_rsa so we can start afresh.\n- if [[ -f /home/admin/.ssh/id_rsa ]]; then\n- echo "Remove old id_rsa"\n- rm -f /home/admin/.ssh/id_rsa\n- fi\n- echo "Create SSH key"\n- ssh-keygen -t rsa -b 4096 -C "commissioning@metaswitch.com" -f /home/admin/.ssh/id_rsa -N ""\n- sudo chown admin:admin /home/admin/.ssh/id_rsa\n- sudo chown admin:admin /home/admin/.ssh/id_rsa.pub\n# Create a log directory for "csar" commands, and make sure admin can write to it\n- echo "Create directory /var/lib/startup for tracking progress"\n# Create a flag, and announce in the log stream, that tools setup is complete\n- touch /var/lib/startup/tools_setup_complete\n- echo "Add ssh key to authorized keys to log on"\n- mkdir -p /home/lifecycle-mgmt/.ssh\n- mkdir -p /home/secrets-mgmt/.ssh\n- echo ${sshPublicKeyAdmin} >> /home/admin/.ssh/authorized_keys\n- echo ${sshPublicKeyLifecycleMgmt} >> /home/lifecycle-mgmt/.ssh/authorized_keys\n- echo ${sshPublicKeySecretsMgmt} >> /home/secrets-mgmt/.ssh/authorized_keys\n\n- echo "Reached end of config-init startup for simpl-vm"\n')
  }
  tags: simplVmObjectTags
}
