#!/bin/bash
POLICY_FILE_PATH="/etc/kubernetes/policies/abac_policy.json"
KUBE_API_SERVER_MANIFEST="/etc/kubernetes/manifests/kube-apiserver.yaml"
# Update ABAC policy file
mkdir -p /etc/kubernetes/policies
cp /vagrant/tests/csu4.json $POLICY_FILE_PATH
# Trigger API server restart by touching the manifest file
touch $KUBE_API_SERVER_MANIFEST
echo "ABAC policy updated and API server restarted to apply changes."