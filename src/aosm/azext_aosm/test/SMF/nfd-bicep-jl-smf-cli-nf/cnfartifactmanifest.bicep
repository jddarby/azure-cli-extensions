// Copyright (c) Microsoft Corporation.

// This file creates an Artifact Manifest for a CNF
param location string
@description('Name of an existing publisher, expected to be in the resource group where you deploy the template')
param publisherName string 
@description('Name of an existing ACR-backed Artifact Store, deployed under the publisher.')
param acrArtifactStoreName string
@description('Name of the manifest to deploy for the ACR-backed Artifact Store')
param acrManifestName string

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

resource acrArtifactManifest 'Microsoft.Hybridnetwork/publishers/artifactStores/artifactManifests@2023-04-01-preview' = {
  parent: acrArtifactStore
  name: acrManifestName
  location: location
  properties: {
    artifacts: [
      {
        artifactName: 'fed-crds'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-43-rel-4-2-0'
      }
      {
        artifactName: 'fed-rbac'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-42-rel-4-2-0'
      }
      {
        artifactName: 'cna-rbac-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-19'
      }
      {
        artifactName: 'fed-kube_addons'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-48-rel-4-2-0'
      }
      {
        artifactName: 'cna-descheduler-descheduler-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-conntrack_clean-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-node_config-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-19'
      }
      {
        artifactName: 'cna-node_config-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-19'
      }
      {
        artifactName: 'fed-opa'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-46-rel-4-2-0'
      }
      {
        artifactName: 'cna-opa-opa-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-opa-kubemgmt-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-opa_gatekeeper-gatekeeper-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-opa_gatekeeper-gatekeeper-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'fed-paas_helpers'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-52-rel-4-2-0'
      }
      {
        artifactName: 'cna-grafana_operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-cores_mgr-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-elastalert_cfg-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-cert_ctrl-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-kargo-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-20'
      }
      {
        artifactName: 'cna-udsf_mgmt_op-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-20'
      }
      {
        artifactName: 'cna-istio_config-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-trace_exporter-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-trace_exporter-fluent_bit_1_9_0-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-capture_ss-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-24'
      }
      {
        artifactName: 'cna-fluentd_operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-fluentd_operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-fluentd_operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-jaeger_agent-jaeger_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-capture_mgr-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-etcd_monitor-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-41'
      }
      {
        artifactName: 'cna-k8s_event_logger-event_exporter-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-cert_manager-cert_manager_webhook-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-cert_manager-cert_manager_cainjector-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-cert_manager-cert_manager_controller-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'fed-istio'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-52-rel-4-2-0'
      }
      {
        artifactName: 'cna-redis-redis-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-redis-redis-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-redis-redis-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-istio-operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-16'
      }
      {
        artifactName: 'cna-istio-cni-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-16'
      }
      {
        artifactName: 'cna-istio-proxyv2-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-16'
      }
      {
        artifactName: 'cna-istio-proxyv2-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-16'
      }
      {
        artifactName: 'cna-istio-proxy_init_ubi8-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-16'
      }
      {
        artifactName: 'cna-istio-proxyv2-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-16'
      }
      {
        artifactName: 'fed-service_reg'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-52-rel-4-2-0'
      }
      {
        artifactName: 'cna-service_reg-service_reg-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-service_reg-service_reg-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'fed-grafana'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-51-rel-4-2-0'
      }
      {
        artifactName: 'cna-grafana-grafana-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'fed-prometheus'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-51-rel-4-2-0'
      }
      {
        artifactName: 'cna-thanos-thanos-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-prometheus-prometheus_operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: 'v2.0.0-17'
      }
      {
        artifactName: 'fed-db_etcd'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-45-rel-4-2-0'
      }
      {
        artifactName: 'cna-etcd_maint-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-etcd-etcd-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: 'v3.4.3-0-18'
      }
      {
        artifactName: 'cna-etcd_operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-19'
      }
      {
        artifactName: 'cna-etcd_operator-disk_mode-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-19'
      }
      {
        artifactName: 'fed-redis_operator'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-42-rel-4-2-0'
      }
      {
        artifactName: 'cna-redis_operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-21'
      }
      {
        artifactName: 'fed-redis_cluster'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-54-rel-4-2-0'
      }
      {
        artifactName: 'cna-redis_cluster-alpine-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-28'
      }
      {
        artifactName: 'cna-redis_cluster-redis_exporter-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-28'
      }
      {
        artifactName: 'cna-redis_cluster-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-28'
      }
      {
        artifactName: 'fed-smf'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-56-rel-4-2-0'
      }
      {
        artifactName: 'cna-radius_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-45'
      }
      {
        artifactName: 'cna-nginx-ingresscontroller-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-nginx-ingresscontroller-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-17'
      }
      {
        artifactName: 'cna-gtpc_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-49'
      }
      {
        artifactName: 'cna-gtpc_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-49'
      }
      {
        artifactName: 'cna-li_x1-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-52'
      }
      {
        artifactName: 'cna-oauth2proxy-oauth2proxy-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-18'
      }
      {
        artifactName: 'cna-cfgmgr-cfgmgr-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-37'
      }
      {
        artifactName: 'cna-chronos-operator-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-19'
      }
      {
        artifactName: 'cna-chronos-chronos-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-19'
      }
      {
        artifactName: 'cna-smf_monitor-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-41'
      }
      {
        artifactName: 'cna-li_x2-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-53'
      }
      {
        artifactName: 'cna-event_exposure-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-41'
      }
      {
        artifactName: 'cna-cdr_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-40'
      }
      {
        artifactName: 'cna-urm-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-41'
      }
      {
        artifactName: 'cna-istio_cfg_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-23'
      }
      {
        artifactName: 'cna-chf_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-46'
      }
      {
        artifactName: 'cna-nrf_agent-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-49'
      }
      {
        artifactName: 'cna-pfcp-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-44'
      }
      {
        artifactName: 'cna-inband_data_agt-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-41'
      }
      {
        artifactName: 'cna-kafka_rplay_agt-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-41'
      }
      {
        artifactName: 'cna-sub_analyzer-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-49'
      }
      {
        artifactName: 'cna-smfcc-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-64'
      }
      {
        artifactName: 'cna-fileserver-rel_4_2_0'
        artifactType: 'OCIArtifact'
        artifactVersion: '4.2.0-16'
      }
    ]
  }
}