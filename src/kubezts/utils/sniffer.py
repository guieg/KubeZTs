import pyshark

from src.kubezts.k8s.k8s import Cluster_k8s
from src.kubezts.utils.run_command import run_command
from kubernetes import client


class Sniffer:

    def __init__(self):
        super()

    @staticmethod
    def check_unencrypted_http(filepath):
        unencrypted_packets_found = []
        with pyshark.FileCapture(filepath) as packets:
            for packet in packets:
                if 'HTTP' in packet:
                    if packet.http.has_field('content_type'):
                        unencrypted_packets_found.append(packet)

        return unencrypted_packets_found

    @staticmethod
    def sniff_pods(pods, _time, folder):
        cluster = Cluster_k8s()
        v1 = client.CoreV1Api()
        ret = v1.list_pod_for_all_namespaces(watch=False)
        out = run_command("mkdir -p %s" % folder)
        kubecommand = "timeout -s INT %s kubectl sniff %s -n %s -p -o %s/%s.pcap"
        for pod in ret.items:
            if pod.status.phase == 'Running' and pod.metadata.name in pods:
                output = run_command(kubecommand % (_time, pod.metadata.name, pod.metadata.namespace, folder, pod.metadata.name))

        output = run_command("kubectl delete pods -l app=ksniff --all-namespaces")
