from src.kubezts.k8s.k8s import Cluster_k8s
from report import  Report


class Auditing:

    def __init__(self):
        super()

    def check_auditing_activated(self):
        cluster = Cluster_k8s()
        apiserver = cluster.get_api_server()
        report = Report()
        for arg in apiserver.spec.containers[0].command:
            if '--audit-policy-file' in arg:
                return True
        report.append_to_report("O argumento do arquivo de configuração auditoria não foi encontrado")
        report.append_to_report(str(apiserver.spec.containers[0].command))

        return False

