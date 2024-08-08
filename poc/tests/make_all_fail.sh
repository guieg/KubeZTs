#!/bin/bash
kubectl apply -f csu1-2.yml
kubectl apply -f csu3.yml
kubectl apply -f csu5.yml

vagrant ssh node1 -c "sudo mkdir -p /etc/kubernetes/policies"
vagrant ssh node1 -c 'sudo echo -e "{\"apiVersion\":\"abac.authorization.kubernetes.io/v1beta1\",\"kind\":\"Policy\",\"spec\":{\"user\":\"unauthorized-user\",\"namespace\":\"*\",\"resource\":\"*\",\"apiGroup\":\"*\",\"nonResourcePath\":\"*\",\"verb\":\"*\"}}" > abac_policy.json'
vagrant ssh node1 -c "sudo cp abac_policy.json /etc/kubernetes/policies/abac_policy.json"

vagrant ssh node1 -c "sudo sed -i 's#RBAC#RBAC,ABAC#g' /etc/kubernetes/manifests/kube-apiserver.yaml"
vagrant ssh node1 -c "sudo  sed -i 's#- kube-apiserver#- kube-apiserver\n    - --authorization-policy-file=/etc/kubernetes/policies/abac_policy.json#g' /etc/kubernetes/manifests/kube-apiserver.yaml"
vagrant ssh node1 -c "sudo  sed -i 's#volumeMounts:#volumeMounts:\n    - mountPath: /etc/kubernetes/policies\n      name: polices\n      readOnly: true#g' /etc/kubernetes/manifests/kube-apiserver.yaml"
vagrant ssh node1 -c "sudo  sed -i 's#volumes:#volumes:\n  - hostPath:\n      path: /etc/kubernetes/policies\n      type: DirectoryOrCreate\n    name: polices#g' /etc/kubernetes/manifests/kube-apiserver.yaml"


vagrant ssh node1 -c "sudo systemctl restart kubelet"



