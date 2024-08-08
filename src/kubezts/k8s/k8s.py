import os
import pathlib
from os.path import join
from dotenv import load_dotenv
from kubernetes import client, config

class Cluster_k8s:
    def __init__(self):
        dotenv_path = pathlib.Path(__file__).parent.parent.parent.resolve()
        dotenv_path = join(dotenv_path, '.env')
        load_dotenv(dotenv_path)
        env = os.environ.copy()

        self.config = config
        self.client = client

        if env['KUBECONFIG']:
            self.path = env['KUBECONFIG']
            self.config.load_kube_config(env['KUBECONFIG'])
        else:
            self.config.load_kube_config()

    def list_cluster_role_bindings(self):
        api = self.client.RbacAuthorizationV1Api()
        return api.list_cluster_role_binding()

    def list_role_bindings(self):
        api = self.client.RbacAuthorizationV1Api()
        return api.list_role_binding_for_all_namespaces()

    def list_cluster_roles(self):
        api = self.client.RbacAuthorizationV1Api()
        return api.list_cluster_role()

    def list_namespaced_roles(self, namespace: str):
        api = self.client.RbacAuthorizationV1Api()
        return api.list_namespaced_role(namespace)

    def list_namespaces(self):
        api = self.client.CoreV1Api()
        namespaces = api.list_namespace()
        namespaces_names = []
        for namespace in namespaces.items:
            namespaces_names.append(namespace.metadata.labels['kubernetes.io/metadata.name'])
        return namespaces_names

    def list_namespaces_with_data(self):
        api = self.client.CoreV1Api()
        namespaces = api.list_namespace()
        return namespaces.items

    def get_api_server(self):
        api = self.client.CoreV1Api()
        pods = api.list_pod_for_all_namespaces()
        apiserver = ''
        for pod in pods.items:
            if "apiserver" in pod.metadata.name:
                apiserver = pod.metadata.name

        return api.read_namespaced_pod(namespace="kube-system", name=apiserver)

    def get_namespaced_resource_quota(self, namespace: str):
        api = self.client.CoreV1Api()
        return api.list_namespaced_resource_quota(namespace).items

    def get_namespaced_limit_range(self, namespace: str):
        api = self.client.CoreV1Api()
        return api.list_namespaced_limit_range(namespace).items

    def list_services(self):
        api = self.client.CoreV1Api()
        return api.list_service_for_all_namespaces().items

    def select_random_pods_from_each_services(self):
        services = self.list_services()
        api = self.client.CoreV1Api()
        pods = api.list_pod_for_all_namespaces()
        target_names = set()
        for service in services:
            if hasattr(service.spec, 'selector') and isinstance(service.spec.selector, dict):
                for key in service.spec.selector:
                    target_names.add(service.spec.selector[key])

        target_pods = []
        while len(target_names) > 0:
            name = target_names.pop()
            for pod in pods.items:
                    if name in pod.metadata.name:
                        target_pods.append(pod.metadata.name)
                        break

        return target_pods