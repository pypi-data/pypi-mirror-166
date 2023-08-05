#!/usr/bin/env python3

import VisualLog.ShellCmd as ShellCmd
import _thread
from time import sleep

shell = ShellCmd.Shell()

print(shell.run('adb devices'))
print(shell.run('adb shell ls'))

# _thread.start_new_thread(shell.run, ('adb shell logcat',))
# sleep(2)
# print(shell.stop())

print("----------------------")
def callback(line):
    if "sys" in line:
        return True
    else:
        return False

print(shell.reset(callback=callback).run('adb shell ls'))
