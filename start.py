import sys
import os
import subprocess
import re
import time

def findThisProcess( process_name ):
    ps     = subprocess.Popen("ps -eaf | grep "+process_name, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()

    return output

# This is the function you can use  
def isThisRunning( process_name ):
    output = findThisProcess( process_name )
    if re.search('path/of/process'+process_name, output) is None:
        return False
    else:
        return True

while True:
    time.sleep(5)
    if isThisRunning('gossip-remover') == False:
        print("Not running")
        print("start gossip-remover")
        os.system('python '+os.path.abspath(".")+'/gossip-remover.py')
    else:
        print("Running!")
