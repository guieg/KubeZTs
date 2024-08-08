from src.kubezts.k8s.k8s import Cluster_k8s
from report import Report

class Authorization:
    def __init__(self):
        super()

    def check_unecessary_cluster_admin_binding(self):
        cluster = Cluster_k8s()
        bind_list = cluster.list_cluster_role_bindings()
        binds_with_system_masters = []
        report = Report()
        for bind in bind_list.items:
            if bind.role_ref.name == "cluster-admin":
                binds_with_system_masters.append(bind)

        if len(binds_with_system_masters) != 2:
            report.append_to_report("Foi encrontrado mais de rolebind utilizando o role cluster-admin")
            report.append_to_report(str(binds_with_system_masters))

        return len(binds_with_system_masters) == 2

    def check_unecessary_system_masters_group_use(self):
        cluster = Cluster_k8s()
        bind_list = list(cluster.list_cluster_role_bindings().items) + list(cluster.list_role_bindings().items)

        report = Report()
        uses = 0
        binds_with_system_masters = []
        for bind in bind_list:
            if bind.subjects:
                for subject in bind.subjects:
                    if subject.name == 'system:masters':
                        # bind
                        binds_with_system_masters.append(bind)
                        uses += 1


        if uses != 1:
            report.append_to_report("Foi encrontrado mais de rolebind utilizando o grupo system:masters")
            report.append_to_report(str(binds_with_system_masters))
            return False

        return True

    def is_default_role(self, role):
        if role.metadata.labels:
            if 'kubernetes.io/bootstrapping' in role.metadata.labels and role.metadata.labels['kubernetes.io/bootstrapping'] == 'rbac-defaults':
                return True
        return False

    def uses_wildcard(self, role):
        if '*' in str(role.rules):
            return True
        return False
    def check_unecessary_wildcard_permission_use(self):
        cluster = Cluster_k8s()
        cluster_roles = cluster.list_cluster_roles()
        all_namespaces = cluster.list_namespaces()
        report = Report()
        using_wildcard = []

        for cluster_role in cluster_roles.items:
            if not self.is_default_role(cluster_role) and self.uses_wildcard(cluster_role):
                using_wildcard.append(cluster_role)

        for namespace in all_namespaces:
            roles = cluster.list_namespaced_roles(namespace)
            for role in roles.items:
                if not self.is_default_role(role) and self.uses_wildcard(role):
                    using_wildcard.append(role)

        if len(using_wildcard) > 0:
            report.append_to_report("Foram encontrados ClusterRoles/Roles com permissões wildcard")
            report.append_to_report(str(using_wildcard))
            return False
        return True

    def check_abac_use(self):
        cluster = Cluster_k8s()
        apiserver = cluster.get_api_server()
        for arg in apiserver.spec.containers[0].command:
            if 'ABAC' in arg:
                return False

        return True
    
    def can_list_secrets(self, role):
        for rule in role.rules:
            if 'secrets' in rule.resources and 'list' in rule.verbs:
                return True
        return False

    def check_listing_secrets_authorization(self):
        cluster = Cluster_k8s()
        cluster_roles = cluster.list_cluster_roles()
        all_namespaces = cluster.list_namespaces()
        report = Report()
        roles_with_list_secret_permission = []

        for cluster_role in cluster_roles.items:
            if not self.is_default_role(cluster_role) and self.can_list_secrets(cluster_role):
                roles_with_list_secret_permission.append(cluster_role)

        for namespace in all_namespaces:
            roles = cluster.list_namespaced_roles(namespace)
            for role in roles.items:
                if not self.is_default_role(role) and self.can_list_secrets(role):
                    roles_with_list_secret_permission.append(role)

        if len(roles_with_list_secret_permission) > 0:
            report.append_to_report("Foram encontrados ClusterRoles/Roles não padrões com permissões de listing secrets")
            report.append_to_report(str([role.metadata.name for role in roles_with_list_secret_permission]))
            return False
        return True