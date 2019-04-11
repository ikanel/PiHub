import subprocess
import sys
import settings

def execute(command):
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        proc_output=p.communicate(timeout=settings.rpc_command_timeout)
        res=proc_output[0].decode("utf-8")+proc_output[1].decode("utf-8")
        return res
    except:
        return "Unexpected error:", (sys.exc_info()[0]).decode("utf-8")

