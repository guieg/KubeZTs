from utils.run_command import run_command


def check_kubectl():
    result = run_command("kubectl version --client=True")
    return not result == ''

def check_ksniff():
    result = run_command("kubectl sniff --help")
    return not result == ''

def check_k8s_api():
    result = run_command("kubectl cluster-info")
    return not result == ''