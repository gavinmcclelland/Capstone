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
sourceRouterMACAddresses = ['18:64:72:82:30:f1', '18:64:72:82:30:f2']

# The filter to use for capturing packets
tcpdumpPacketFilter = 'ether src ' + sourceRouterMACAddresses[0] + ' or ether dst ' + sourceRouterMACAddresses[0] + ''.join([(' or ether src ' + sourceRouterMACAddress + ' or ether dst ' + sourceRouterMACAddress) for sourceRouterMACAddress in sourceRouterMACAddresses[1:]]) + ' and not type mgt subtype beacon'

# tcpdump command to execute
tcpdumpCommand = ['sudo', 'tcpdump', '-i', 'This will be replaced with the interface name', '-n', '-q', '-e', '-s', '64', '-l', tcpdumpPacketFilter]

printFunctionTimer = None

# ==================== CONSTANTS ====================

printInterval = 1 # seconds
timeoutSinceLastPacket = 90 # seconds

timeToStayActive = 30 # seconds
packetsToStayActive = 50 # of packets

currentFileLogTimeCount = 100000000
fileLogInterval = 30 # seconds
outputFileName = '/root/Documents/Logs/PeopleCounter/Alpha/' + datetime.now().strftime('%Y_%m_%d_%H-%M-%S_') + 'ReAssoc_Count.csv'

# Names of WiFi networks correcponding to the router MAC addresses (e = eduroam, Q = Queensu)
BSSIDIndexNames = ['e', 'Q'] 

# ==================== COLORS ====================

ALL_OFF = 				'\033[0m'
BOLD = 					'\033[1m'
FG_DARK_GRAY =			'\033[90m'
FG_CYAN = 				'\033[36m'
FG_RED = 				'\033[31m'
FG_GREEN = 				'\033[32m'
FG_YELLOW = 			'\033[33m'
FG_MAGENTA = 			'\033[35m'
BG_MAGENTA = 			'\033[45m'
BG_GREEN = 				'\033[42m'
BG_YELLOW = 			'\033[43m'
BG_BLUE = 			    '\033[44m'

class WiFiDevice:
    
    def __init__(self, detectedOrder, BSSIDIndex, MACAddress, averageRSSI):
        self.detectedOrder = detectedOrder
        self.BSSIDIndex = BSSIDIndex
        self.MACAddress = MACAddress
        self.firstPacketTime = datetime.now()
        self.lastPacketTime = self.firstPacketTime
        self.averageRSSI = averageRSSI
        self.sumRSSI = averageRSSI
        self.numberOfPacketsTo = 1
        self.numberOfPacketsFrom = 1

    def __str__(self):
        return f"{BSSIDIndexNames[self.BSSIDIndex]: <{2}} | {self.MACAddress: <{17}} | {self.averageRSSI: <{8}} | {self.numberOfPacketsTo: <{10}} | {self.numberOfPacketsFrom: <{8}} | {self.get_time_since_last_packet()}"

    def add_packet(self, newRSSI, isFromDeviceToRouter):
        self.lastPacketTime = datetime.now()
        if(isFromDeviceToRouter):
            self.sumRSSI = self.sumRSSI + newRSSI
            self.numberOfPacketsFrom = self.numberOfPacketsFrom + 1
        else:
            self.numberOfPacketsTo = self.numberOfPacketsTo + 1
        self.averageRSSI = round(self.sumRSSI / self.numberOfPacketsFrom, 1)
    
    def total_number_of_packets(self):
        return self.numberOfPacketsTo + self.numberOfPacketsFrom
    
    def is_active_after_reassociation(self):
        return (self.get_time_since_first_packet() >= timeToStayActive and (self.numberOfPacketsTo + self.numberOfPacketsFrom) >= packetsToStayActive)

    def did_time_out(self):
        return self.get_time_since_last_packet() > timeoutSinceLastPacket

    def get_time_since_last_packet(self):
        return int((datetime.now() - self.lastPacketTime).total_seconds())#.strftime('%H:%M:%S')

    def get_time_since_first_packet(self):
        return int((datetime.now() - self.firstPacketTime).total_seconds())#.strftime('%H:%M:%S')

# The current WiFi device number detected
detectedDevices = 0

# List 1 and 2
WiFiDevicesActive = defaultdict(WiFiDevice)
WiFiDevicesReassociated = defaultdict(WiFiDevice)

def logNumberToFile():
    with open(outputFileName, 'a') as outputFile:
        print(datetime.now().strftime('%H:%M:%S, '), end = '', file = outputFile)
        print(f"{detectedDevices}, {len(WiFiDevicesReassociated)}, {len(WiFiDevicesActive)}", file = outputFile)

def printWiFiDevices():

    global printFunctionTimer
    printFunctionTimer = threading.Timer(printInterval, printWiFiDevices)
    printFunctionTimer.start()
    os.system('cls' if os.name == 'nt' else 'clear')

    # Remove from list 1 if need be
    devicesToRemove = []
    for device in WiFiDevicesReassociated:
        if WiFiDevicesReassociated[device].did_time_out():
            #print('device ' + device + ' timed out')
            devicesToRemove.append(device)
    for device in devicesToRemove:
        del WiFiDevicesReassociated[device]

    # Add to list 2 if need be
    devicesToMove = []
    for device in WiFiDevicesReassociated:
        if WiFiDevicesReassociated[device].is_active_after_reassociation():
            devicesToMove.append((device, WiFiDevicesReassociated[device].BSSIDIndex))
    for (device, BSSIDIndex) in devicesToMove:
        WiFiDevicesActive[device] = WiFiDevice(detectedDevices, BSSIDIndex, device, RSSIValue)
        del WiFiDevicesReassociated[device]
    
    # Remove from list 2 if need be
    numberOfDevicesNotTimedOut = 0
    devicesToRemove = []
    for device in WiFiDevicesActive:
        if WiFiDevicesActive[device].did_time_out():
            #print('device ' + device + ' timed out')
            devicesToRemove.append(device)
    for device in devicesToRemove:
        del WiFiDevicesActive[device]

    print('-------------------------------------------------------------------------------')
    print('# of devices - Total: ' +  FG_YELLOW + str(detectedDevices) + ALL_OFF +
     ', Reassociated: ' + FG_GREEN + str(len(WiFiDevicesReassociated)) + ALL_OFF +
     ', Active: ' + FG_MAGENTA + str(len(WiFiDevicesActive)) + ALL_OFF
     )
    print('-------------------------------------------------------------------------------\n')
    print(f"ID | {'MAC Address': <{17}} | {'Avg RSSI': <{8}} | {'# pck from': <{10}} | {'# pck to': <{8}} | T_last_pck")

    colourRules = {
        '08:74:02:11:08:2f' : BG_MAGENTA,
        '50:bc:96:9f:f2:58' : BG_GREEN,
        '90:b6:86:6e:b1:98' : BG_YELLOW,
        '80:b0:3d:45:98:a5' : BG_BLUE
    }

    #for device, packetsList in sorted(WiFiDevicesActive.items()):
    for device in sorted(WiFiDevicesReassociated, key=lambda x: WiFiDevicesReassociated[x].detectedOrder):
        currentWiFiDevice = WiFiDevicesReassociated[device]
        if currentWiFiDevice.total_number_of_packets() > 1:
            currentWiFiDevice = WiFiDevicesReassociated[device]

            colorForThisDevice = ''
            if(device in colourRules):
                colorForThisDevice = colourRules[device]

            formatForThisDevice = colorForThisDevice if not colorForThisDevice == '' else (FG_CYAN if not currentWiFiDevice.did_time_out() else FG_DARK_GRAY)
            print(formatForThisDevice + str(currentWiFiDevice) + ALL_OFF)

    print('--- Standby ↑  ↓ Active -------------------------------------------------------')

    for device in sorted(WiFiDevicesActive, key=lambda x: WiFiDevicesActive[x].detectedOrder):
        currentWiFiDevice = WiFiDevicesActive[device]
        if currentWiFiDevice.total_number_of_packets() > 1:
            currentWiFiDevice = WiFiDevicesActive[device]

            colorForThisDevice = ''
            if(device in colourRules):
                colorForThisDevice = colourRules[device]

            formatForThisDevice = colorForThisDevice if not colorForThisDevice == '' else (FG_CYAN if not currentWiFiDevice.did_time_out() else FG_DARK_GRAY)
            print(formatForThisDevice + str(currentWiFiDevice) + ALL_OFF)

    global currentFileLogTimeCount
    if currentFileLogTimeCount >= fileLogInterval:
        currentFileLogTimeCount = 0
        logNumberToFile()
    else:
        currentFileLogTimeCount = currentFileLogTimeCount + 1

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

    # Setup regexes
    sourceMACRegex = re.compile('SA:([0-9a-f:]{17})')
    destinationMACRegex = re.compile('DA:([0-9a-f:]{17})')
    RSSIRegex = re.compile('-([0-9]*)dBm')
    probeRegex = re.compile('Probe')
    assocRegex = re.compile('Assoc')
    reassocRegex = re.compile('ReAssoc')

    # Call print function which will be repeated regularly
    if(printFunctionTimer is None):
        printWiFiDevices()

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
            sourceMAC_RegexResult = re.search(sourceMACRegex, line)
            if sourceMAC_RegexResult is not None:
                sourceMAC = sourceMAC_RegexResult.group(1)

                destinationMAC_RegexResult = re.search(destinationMACRegex, line)
                if destinationMAC_RegexResult is not None:
                    destinationMAC = destinationMAC_RegexResult.group(1)

            # If this packet does not have a source address, skip it
            else:
                continue

            # If the source was the router, take the destination MAC address instead
            if sourceMAC in sourceRouterMACAddresses:
                BSSIDIndex = sourceRouterMACAddresses.index(sourceMAC)
                MACAddress = destinationMAC
            else:
                BSSIDIndex = sourceRouterMACAddresses.index(destinationMAC)
                MACAddress = sourceMAC

            # Get packet type
            packetType = 'Probe' if re.search(probeRegex, line) is not None else None
            if packetType is None:
                packetType = 'ReAssoc' if re.search(reassocRegex, line) is not None else None
                if packetType is None:
                    packetType = 'Assoc' if re.search(assocRegex, line) is not None else 'Null'

            #print(packetType)
            #print(line)

            # Add to list 1
            #if packetType == 'Assoc' or packetType == 'ReAssoc':
            if packetType == 'ReAssoc':
                if MACAddress not in WiFiDevicesReassociated:
                    if MACAddress not in WiFiDevicesActive:
                        WiFiDevicesReassociated[MACAddress] = WiFiDevice(detectedDevices, BSSIDIndex, MACAddress, RSSIValue)
                        detectedDevices += 1

            # Is this packet coming from the router or not
            isFromRouter = sourceMAC in sourceRouterMACAddresses

            if MACAddress in WiFiDevicesReassociated:
                WiFiDevicesReassociated[MACAddress].add_packet(RSSIValue, not isFromRouter)

            if MACAddress in WiFiDevicesActive:
                WiFiDevicesActive[MACAddress].add_packet(RSSIValue, not isFromRouter)
                
    except KeyboardInterrupt:

        print('Exiting...')
        if(not printFunctionTimer == None):
            printFunctionTimer.cancel()