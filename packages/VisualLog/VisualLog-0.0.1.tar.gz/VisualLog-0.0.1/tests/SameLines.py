#!/usr/bin/env python3

import VisualLog.SameLines as SameLines

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

sameLines, oldIndes, newIndes = SameLines.diffList(old, new)
print("-----same line------")
for line in sameLines:
    print(line)

print("-----old index------")
for index in oldIndes:
    print(str(index) + " -> " + old[index])

print("-----new index------")
for index in newIndes:
    print(str(index) + " -> " + new[index])
