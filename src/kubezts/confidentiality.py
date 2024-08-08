from k8s.k8s import Cluster_k8s
from utils.sniffer import Sniffer
from src.kubezts.report import Report

class Confidentiality:

    def __init__(self):
        super()

    def check_unecrypted_communication(self, _time, folder):
        cluster = Cluster_k8s()
        pods = cluster.select_random_pods_from_each_services()
        sniffer = Sniffer()
        sniffer.sniff_pods(pods, _time, folder)
        report = Report()
        unencrypted_packets = []
        for pod in pods:
            unencrypted_packets += sniffer.check_unencrypted_http(f"{folder}/{pod}.pcap")

        if not len(unencrypted_packets) == 0:
            report.append_to_report("Foi encontrado indícios de comunicação não criptografada")
            report.append_to_report(str(unencrypted_packets))

        return len(unencrypted_packets) == 0


