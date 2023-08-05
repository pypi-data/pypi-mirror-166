#!/usr/bin/env python3

import re
import difflib

def defaultCallback(line):
    status = -1
    matchObj = re.match(r'^([\+\- ]) ', line, re.M | re.I)
    if matchObj:
        match = matchObj.group(1)
        if match == " ":
            status = 0
        elif match == "-":
            status = 1
        elif match == "+":
            status = 2
        else:
            status = 10
    
    return status

def diffList(old, new, callback = defaultCallback):
    diff = difflib.Differ()
    sameLines = []
    oldIndexs = []
    newIndexs = []

    oldIndex = 0
    newIndex = 0
    for line in list(diff.compare(old, new)):
        status = callback(line)
        if status == 0:
            sameLines.append(line.lstrip())

            oldIndexs.append(oldIndex)
            newIndexs.append(newIndex)

            oldIndex += 1
            newIndex += 1
        elif status == 1:
            oldIndex += 1
        elif status == 2:
            newIndex += 1
        else:
            pass
    
    return sameLines, oldIndexs, newIndexs

if __name__ == "__main__" :

    old = [
        "USB Mass Storage device detected",
        "USB Mass Storage device detected",
        "scsi host0: usb-storage 1-1:1.0",
        "Direct-Access",
        "Attached SCSI removable disk",
        "/system/bin/sgdisk",
        "Disk::readPartitions",
        "Disk::createPublicVolume",
        "FAT-fs"
    ]

    new = [
        "scsi host0: usb-storage 1-1:1.0",
        "USB Mass Storage device detected",
        "Direct-Access",
        "Attached SCSI removable disk",
        "/system/bin/sgdisk",
        "Disk::readPartitions",
        "FAT-fs",
        "Disk::createPublicVolume",
    ]

    diff = difflib.Differ()
    print("new +++")
    print("old ---")
    print("\n".join(list(diff.compare(old, new))))

    sameLines, oldIndes, newIndes = diffList(old, new)
    print("-----same line------")
    for line in sameLines:
        print(line)

    print("-----old index------")
    for index in oldIndes:
        print(str(index) + " -> " + old[index])

    print("-----new index------")
    for index in newIndes:
        print(str(index) + " -> " + new[index])
