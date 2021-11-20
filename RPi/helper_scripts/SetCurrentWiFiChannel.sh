#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

INTERFACE="wlan1"
CHANNEL=1

# Get interface name
if [ $# == 0 ]; then
        printf "[${YELLOW}i${NC}] Usage: SetCurrentWiFiChannel.sh <interface> <channel>\n\>"
        printf "[${YELLOW}i${NC}] Using default interface: $INTERFACE and channel $CHANNEL\n"
else
        INTERFACE=$1
        CHANNEL=$2
fi

# Set channel
sudo iw $INTERFACE set channel $CHANNEL
printf "[${GREEN}i${NC}] Set interface ${CYAN}$INTERFACE${NC} to ${CYAN}channel $CHANNEL${NC}\n"
