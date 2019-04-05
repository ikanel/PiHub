import subprocess
import sys
import settings

def execute(command):
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        return p.communicate(timeout=settings.rpc_command_timeout)[0].decode("utf-8")
    except:
        return "Unexpected error:", (sys.exc_info()[0]).decode("utf-8")

print(execute(["ls"]))
