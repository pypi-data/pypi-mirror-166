#!/usr/bin/env python3

import sys
sys.path.insert(0, "/home/x/OneDrive/Projects/bthci/src")

import subprocess

from bthci import HCI, HciOpcodes
from bthci.event import HciEvent, HciEventCodes, HCI_Command_Status, HCI_LE_Connection_Complete

print(hex(HciOpcodes.Disconnect))

output = subprocess.check_output("hciconfig | grep Type", shell=True)
print(output.decode())
print(HCI.find_hci_strs_in_txt(""))

# HCI_Command_Status()
