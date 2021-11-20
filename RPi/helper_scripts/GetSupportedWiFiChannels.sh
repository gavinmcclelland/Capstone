#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Default interface
INTERFACE="wlan1"

# Check that an interface is supplied as argument
if [ $# == 0 ]; then
	# If not, indicate that the default one is being used
	printf "[${YELLOW}i${NC}] Using default interface: $INTERFACE\n"
else
	# Otherwise, indicate that the selected interface is being used
	INTERFACE=$1
	printf "[${GREEN}i${NC}] Using interface: $INTERFACE\n"
fi

# Get the supported and current channels
iwlist $INTERFACE channel