import os
import subprocess
import shlex

from src.kubezts.utils.bcolors import Bcolors


def run_command(cmd: str) -> str:
    env = os.environ.copy()
    env["PATH"] = f"{env['HOME']}/.krew/bin:{env['PATH']}"
    # cmd = "KUBECONFIG=" + env["KUBECONFIG"] + " " + cmd
    # print(env["KUBECONFIG"])
    try:
        p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        p.wait()
        stdout, stderr = p.communicate()
        if stderr:
            print(Bcolors.FAIL + str(stderr) + Bcolors.FAIL)
            return ''
        else:
            return stdout

    except Exception as err:
        return err.__str__()