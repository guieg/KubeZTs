#!/bin/bash
kubectl delete -f csu1-2.yml
kubectl delete -f csu3.yml
kubectl delete -f csu5.yml
kubectl apply -f csu6.yml -n default
kubectl apply -f csu6.yml -n kube-node-lease
kubectl apply -f csu6.yml -n kube-public
kubectl apply -f csu6.yml -n kube-system
kubectl apply -f csu7.yml -n default
kubectl apply -f csu7.yml -n kube-node-lease
kubectl apply -f csu7.yml -n kube-public
kubectl apply -f csu7.yml -n kube-system

vagrant ssh node1 -c "sudo kubeadm init phase control-plane apiserver"

vagrant ssh node1 -c "sudo mkdir -p /etc/kubernetes/policies"
vagrant ssh node1 -c "sudo cp /vagrant/tests/csu8.yml /etc/kubernetes/policies"

vagrant ssh node1 -c "sudo  sed -i 's#- kube-apiserver#- kube-apiserver\n    - --audit-policy-file=/etc/kubernetes/policies/csu8.yml\n    - --audit-log-path=/var/log/kubernetes/audit.log#g' /etc/kubernetes/manifests/kube-apiserver.yaml"
vagrant ssh node1 -c "sudo  sed -i 's#volumeMounts:#volumeMounts:\n    - mountPath: /etc/kubernetes/policies\n      name: polices\n      readOnly: true#g' /etc/kubernetes/manifests/kube-apiserver.yaml"
vagrant ssh node1 -c "sudo  sed -i 's#volumes:#volumes:\n  - hostPath:\n      path: /etc/kubernetes/policies\n      type: DirectoryOrCreate\n    name: polices#g' /etc/kubernetes/manifests/kube-apiserver.yaml"


vagrant ssh node1 -c "sudo systemctl restart kubelet"

