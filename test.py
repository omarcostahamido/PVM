import os
from subprocess import CalledProcessError, check_output
import subprocess
import time
from pythonosc.udp_client import SimpleUDPClient

def killPvm():
    try:
        ret = check_output(["pgrep", "-f", "python pvm.py"])
        pid = int(ret.decode("utf-8").strip())
        os.kill(pid, 9)
        print("killed", pid)
    except CalledProcessError as ce:
        print("No pvm.py running")
def sendCommand():
    port = 8001
    ip = "0.0.0.0"
    client = SimpleUDPClient(ip, port)  # Create client

    client.send_message("/PVM", ["file", "jellyfish720.mp4"])
    time.sleep(1)
    client.send_message("/PVM", "start")
    time.sleep(1)
    client.send_message("/PVM", "stop")
    time.sleep(1)
    client.send_message("/PVM", "stop")

def test():
    killPvm()
    cmd = ["python", "pvm.py"]
    popen = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    time.sleep(2)
    sendCommand()
    killPvm()
    out, err = popen.communicate()
    # ret = err.readlines()
    print("***err", err)
    print("***out", out)
    if "error" in err.lower() or "exception" in err.lower():
        print("Exceptions or errors detected, test failed.")
    else:
        print("Test finished successfully.")
test()