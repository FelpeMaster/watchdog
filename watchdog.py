import json
import os
import subprocess

"""
Check if variation of file was change
"""
"""
Global variables
"""

cfgFIle = 'watchDogConfiguration.json'

def updateFileSize(fileSizeKey, fileSize):
    with open(cfgFIle,'r') as f:
        cfg = json.load(f)
    cfg['sizeFile'][fileSizeKey] = fileSize
    with open(cfgFIle, 'w') as f:
        json.dump(cfg, f)

def restartService(serviceKey):
    with open(cfgFIle,'r') as f:
        cfg = json.load(f)
    s = cfg['services']
    subprocess.Popen(["sudo", "systemctl", "restart", "%s"%s[serviceKey]], stdout=subprocess.PIPE)

def comparePreviousFileSize(fileSizeKey, serviceKey, file_path, previousSize=0):
    fileSize = os.stat(file_path).st_size
    if previousSize == fileSize:
        return True
        restartService(serviceKey)
    else:
        updateFileSize(fileSizeKey, fileSize)
        return False

def watchDog():
    with open(cfgFIle,'r') as file:
        cfg = json.load(file)
    d = cfg['databasesPath']
    s = cfg['sizeFile']
    for i in range(3):
        databasePathKey = "d%d"%i
        sizeFileKey = "s%d"%i
        serviceKey = "se%d"%i
        if comparePreviousFileSize(sizeFileKey, serviceKey, d[databasePathKey],s[sizeFileKey]):
            print ("Se cumple la condicion")
        else:
            print ("No se cumple la condición")

#file_path = "/home/frobles/Documentos/watchDog/README.md"
#file_path = "/home/frobles/Documentos/EOG CAT2 DataRAM 4.v2.pdf"
watchDog()
