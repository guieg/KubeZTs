from src.kubezts.k8s.k8s import Cluster_k8s
from report import Report


class AdmissionControl:

    def __init__(self):
        super()

    def check_namespaces_resource_quota(self):
        cluster = Cluster_k8s()
        namespaces = cluster.list_namespaces()
        report = Report()
        namespaces_without_resource = []
        for namespace in namespaces:
            if len(cluster.get_namespaced_resource_quota(namespace)) == 0:
                namespaces_without_resource.append(namespace)

        report.append_to_report("Foram encontrados namespaces sem resourceQuota")
        report.append_to_report(str(namespaces_without_resource))

        return len(namespaces_without_resource) == 0

    def check_namespaces_limit_ranges(self):
        cluster = Cluster_k8s()
        namespaces = cluster.list_namespaces()
        report = Report()
        namespaces_without_limit_ranges = []
        for namespace in namespaces:
            if len(cluster.get_namespaced_limit_range(namespace)) == 0:
                namespaces_without_limit_ranges.append(namespace)

        report.append_to_report("Foram encontrados namespaces sem limit range")
        report.append_to_report(str(namespaces_without_limit_ranges))
        return len(namespaces_without_limit_ranges) == 0