import pathlib
from os.path import join

from dotenv import load_dotenv

from src.kubezts.utils.bcolors import Bcolors
from authorization import Authorization
from auditing import Auditing
from admission_control import AdmissionControl
from confidentiality import Confidentiality
from check_requirements import *
from report import Report


def check(value, text):
    if value:
        print(Bcolors.OKGREEN + text + " OK" + Bcolors.OKGREEN)
    else:
        print(Bcolors.FAIL + text + " FAIL" + Bcolors.FAIL)
    return value

if __name__ == "__main__":
    dotenv_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    dotenv_path = join(dotenv_path, '.env')
    load_dotenv(dotenv_path)

    authorization = Authorization()
    auditing = Auditing()
    admission_control = AdmissionControl()
    confidentiality = Confidentiality()

    reqlist = []

    print(f"{Bcolors.WHITE}Checando requisitos:{Bcolors.WHITE}")

    print("---------------------------------------")
    reqlist.append(check(check_kubectl(), "kubectl está instalado"))
    reqlist.append(check(check_ksniff(), "ksniff plugin está instalado"))
    reqlist.append(check(check_k8s_api(), "Cluster kubernetes disponível"))

    for req in reqlist:
        if not req:
            exit(1)

    print(f"{Bcolors.WHITE}---------------------------------------{Bcolors.WHITE}")
    print(f"{Bcolors.WHITE}Iniciando verificações{Bcolors.WHITE}")

    print(f"{Bcolors.WHITE}---------------------------------------{Bcolors.WHITE}")
    check(authorization.check_unecessary_cluster_admin_binding(), "Least Privilege: Bind desnecessário de role ClusterAdmin")
    check(authorization.check_unecessary_system_masters_group_use(), "Least Privilege: system:masters possui outro usuário além do ClusterAdmin")
    check(authorization.check_unecessary_wildcard_permission_use(), "Least Privilege: Algum Role ou ClusterRole não padrão do kubernetes possui permissão wildcard")
    check(auditing.check_auditing_activated(), "Auditing: Auditoria do kubernetes ativada")
    check(authorization.check_abac_use(), "Authorization: Uso de recurso depreciado ABAC")
    check(admission_control.check_namespaces_resource_quota(), "Admission Control: ResourceQuota especificado em todos os namespaces.")
    check(admission_control.check_namespaces_limit_ranges(), "Admission Control: LimitRange especificado em todos os namespaces.")
    check(authorization.check_listing_secrets_authorization(),"Least Privilege: Algum Role ou ClusterRole não padrão do kubernetes possui permissão de list secrets")
    check(confidentiality.check_unecrypted_communication("30s", "/tmp/kubeZTs"),"Confidentiality: comunicação não criptografada detectada.")
    print(f"{Bcolors.WHITE}---------------------------------------{Bcolors.WHITE}")
    print(f"{Bcolors.WHITE}Report das falhas encontradas{Bcolors.WHITE}")
    print(f"{Bcolors.WHITE}---------------------------------------{Bcolors.WHITE}")
    print(f"{Bcolors.FAIL}{Report().get_report()}{Bcolors.FAIL}")
    print(f"{Bcolors.WHITE}---------------------------------------{Bcolors.WHITE}")


