import subprocess
import sys
import settings

def execute(command):
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        return str(p.communicate(timeout=settings.rpc_command_timeout))
    except:
        return "Unexpected error:", str(sys.exc_info()[0])


#print(execute(["ping ya.ru"]))
