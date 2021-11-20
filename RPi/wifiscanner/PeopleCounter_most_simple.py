#!/usr/bin/python3

# ==================== LIBS ====================

import re
import os
import argparse
import threading
from time import sleep
import subprocess as sub
from datetime import datetime
from collections import defaultdict

# ==================== COMMANDS ====================

# Router used 
# Bain Lab router
sourceRouterMACAddress = '18:64:72:82:30:f2'

# The filter to use for capturing packets
tcpdumpPacketFilter = 'ether src ' + sourceRouterMACAddress + 'or ether dst ' + sourceRouterMACAddress + ' and not type mgt subtype beacon'

# tcpdump command to execute
tcpdumpCommand = ['sudo', 'tcpdump', '-i', 'This will be replaced with the interface name', '-n', '-q', '-e', '-s', '64', '-l', tcpdumpPacketFilter]

printFunctionTimer = None

# ==================== CONSTANTS ====================

printInterval = 1 # seconds
timeoutSinceLastPacket = 120 # seconds

# ==================== COLORS ====================

ALL_OFF = 				'\033[0m'
BOLD = 					'\033[1m'
FG_DARK_GRAY =			'\033[90m'
FG_CYAN = 				'\033[36m'
FG_RED = 				'\033[31m'
FG_GREEN = 				'\033[32m'
FG_YELLOW = 			'\033[33m'
BG_MAGENTA = 			'\033[45m'
BG_GREEN = 				'\033[42m'
BG_YELLOW = 			'\033[43m'

class WiFiDevice:
    
    def __init__(self, detectedOrder, MACAddress, averageRSSI):
        self.detectedOrder = detectedOrder
        self.MACAddress = MACAddress
        self.firstPacketTime = datetime.now()
        self.lastPacketTime = self.firstPacketTime
        self.averageRSSI = averageRSSI
        self.sumRSSI = averageRSSI
        self.numberOfPackets = 1

    def __str__(self):
        return f"{self.MACAddress: <{18}} | {self.averageRSSI: <{9}} | {self.numberOfPackets: <{10}} | " + str(self.get_time_since_last_packet())

    def add_packet(self, newRSSI):
        self.lastPacketTime = datetime.now()
        self.sumRSSI = self.sumRSSI + newRSSI
        self.numberOfPackets = self.numberOfPackets + 1
        self.averageRSSI = round(self.sumRSSI / self.numberOfPackets, 1)
        
    def did_time_out(self):
        return self.get_time_since_last_packet() > timeoutSinceLastPacket

    def get_time_since_last_packet(self):
        return int((datetime.now() - self.lastPacketTime).total_seconds())#.strftime('%H:%M:%S')

# Captured packets
WiFiDevices = defaultdict(WiFiDevice)

def printWiFiDevices():

    global printFunctionTimer
    printFunctionTimer = threading.Timer(printInterval, printWiFiDevices)
    printFunctionTimer.start()
    os.system('cls' if os.name == 'nt' else 'clear')

    numberOfDevicesNotTimedOut = 0
    for device in WiFiDevices:
        if not WiFiDevices[device].did_time_out():
            numberOfDevicesNotTimedOut += 1

    print('---------------------------------------------')
    print('# of devices - Total: ' +  FG_YELLOW + str(len(WiFiDevices)) + ALL_OFF + ', Not timed out: ' + FG_GREEN + str(numberOfDevicesNotTimedOut) + ALL_OFF)
    print('---------------------------------------------\n')
    print(f"{'MAC Address': <{18}} | {'Avg RSSI': <{9}} | {'# packets': <{10}} | Time since last packet")

    colourRules = {
        '08:74:02:11:08:2f' : BG_MAGENTA,
        '50:bc:96:9f:f2:58' : BG_GREEN,
        '90:b6:86:6e:b1:98' : BG_YELLOW
    }

    #for device, packetsList in sorted(WiFiDevices.items()):
    for device in sorted(WiFiDevices, key=lambda x: WiFiDevices[x].detectedOrder):
        currentWiFiDevice = WiFiDevices[device]
        if currentWiFiDevice.numberOfPackets > 1:
            currentWiFiDevice = WiFiDevices[device]

            colorForThisDevice = ''
            if(device in colourRules):
                colorForThisDevice = colourRules[device]

            formatForThisDevice = colorForThisDevice if not colorForThisDevice == '' else (FG_CYAN if not currentWiFiDevice.did_time_out() else FG_DARK_GRAY)
            print(formatForThisDevice + str(currentWiFiDevice) + ALL_OFF)

# Main function
if __name__ == "__main__":

    # Setup arguments that can / must be passed on command line
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('interface',
    help='Which WiFi interface (adapter) to use')
    
    # Read in the arguments passed in from the command line
    args = parser.parse_args()

    # Start tcpdump
    tcpdumpCommand[3] = args.interface
    tcpdumpCommand = tuple(tcpdumpCommand)
    print('[' + FG_YELLOW + 'i' + ALL_OFF + '] Starting tcpdump: ' + ' '.join(tcpdumpCommand))
    tcpdumpCall = sub.Popen(tcpdumpCommand, stdout=sub.PIPE)

    # The current WiFi device number detected
    detectedDevices = 0

    # Setup regexes
    stationMACRegex = re.compile('SA:([0-9a-f:]{17})')
    RSSIRegex = re.compile('-([0-9]*)dBm')
    probeRegex = re.compile('Probe')
    assocRegex = re.compile('Assoc')
    reassocRegex = re.compile('ReAssoc')

    try:

        # Listen to output
        for line in iter(tcpdumpCall.stdout.readline, b''):
            
            # Convert current line to string
            line = line.decode('ascii').strip()

            # Get time packet was received
            timestamp = line[:line.index('.')]

            # Get RSSI
            RSSIValue = int('-' + re.search(RSSIRegex, line).group(1))

            # Get station MAC address
            stationMAC_RegexResult = re.search(stationMACRegex, line)
            if stationMAC_RegexResult is not None:
                stationMAC = stationMAC_RegexResult.group(1)

            # If this packet does not have a source address, skip it
            else:
                continue

            if stationMAC not in WiFiDevices:
                WiFiDevices[stationMAC] = WiFiDevice(detectedDevices, stationMAC, RSSIValue)
                detectedDevices += 1

                # Call print function which will be repeated regularly
                if(printFunctionTimer is None):
                    printWiFiDevices()

            else:
                WiFiDevices[stationMAC].add_packet(RSSIValue)

    except KeyboardInterrupt:

        print('Exiting...')
        if(not printFunctionTimer == None):
            printFunctionTimer.cancel()