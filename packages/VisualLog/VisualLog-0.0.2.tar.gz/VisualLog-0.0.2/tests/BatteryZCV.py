#!/usr/bin/env python3

import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

def defaultShowCallback(fig, index):
    ax = fig.get_axes()[index]
    ax.set_xlabel(customData["xlabel"])
    ax.set_ylabel(customData["ylabel"])

    for i in range(len(lineInfos[0])):
        ax.plot(range(len(lineInfos)), [s[i] for s in lineInfos], label = labels[i])

    ax.legend()

def defaultLineCallback(lineInfo):
    lineInfoFixed = []
    for index in range(len(lineInfo)):
        lineInfoFixed.append(float(lineInfo[index].strip()))
    
    return lineInfoFixed

filename = "default/zcv.txt"

# 电池容量   开路电压  电池电阻 
# {0.1mah, 0.1mv ,0.1mΩ}
# 2705    42248   1025
lineInfos = LogParser.logFileParser(
        filename,
        r'(\d+)\s+(\d+)\s+(\d+)',
        callback=defaultLineCallback
    )

for info in lineInfos:
    print(info)

labels = ["Battery Capacity", "Open Circuit Voltage", "Battery Resistance"]
customData = {"xlabel": "X", "ylabel": "Y"}
# MatplotlibZoom.Show(callback=defaultShowCallback, rows = 1, cols = 1)
MatplotlibZoom.Live(callback=defaultShowCallback, rows = 1, cols = 1)
