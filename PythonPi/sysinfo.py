import os
import time
from subprocess import check_output
from re import findall
import psutil
import sys

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])

def get_disk():
    return str(psutil.disk_usage('/').percent)

def get_ram():
    return str(psutil.virtual_memory().percent)

def get_cpu():
    return str(psutil.cpu_percent(interval=None))
