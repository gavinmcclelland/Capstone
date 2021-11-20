#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

# Check that an interface is supplied as argument
if [ $# == 0 ]; then
    # If not indicate and exit with error code 1
	printf "[${RED}i${NC}] Must supply interface as argument (eth0, wlan0)!\n"
    exit 1
else
    # Otherwise, get the IP (v4) addredd of the selected interface
    echo `ip -o -4 addr list $1 | awk '{print $4}' | cut -d/ -f1`

    # Breakdown:
    # Command:  ip -o -4 addr list <interface>
    # Output:   2: <interface>    inet <x.x.x.x>/24
    # Command:  awk '{print $4}'
    # Output:   <x.x.x.x>/24
    # Command:  cut -d/ -f1
    # Output:   <x.x.x.x>

fi