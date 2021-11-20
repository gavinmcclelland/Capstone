#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

INTERFACE="wlan1"
INTERVAL=1 # seconds

# Get interface name
if [ $# == 0 ]; then
	printf "[${YELLOW}i${NC}] Usage: WiFiChannelHopper <interface> <interval (s)>\n\n"
	printf "[${YELLOW}i${NC}] Using default interface: $INTERFACE\n"
else
	INTERFACE=$1
	INTERVAL=$2
	printf "[${GREEN}i${NC}] Using set interface: $INTERFACE\n"
fi

# Set interface to monitor mode
#printf "[${GREEN}i${NC}] Setting monitor mode...\n"
#~/helper_scripts/SetupWiFiMonitorMode.sh $INTERFACE

# Get supported channel list (code from airmon-ng script)
# This returned channel 14 as supported when it was sometimes not
#channel_list="$(iw phy $(cat /sys/class/net/$INTERFACE/phy80211/name) info 2>&1 | awk -F'[][]' '$2{print $2}')"
channel_list=`iwlist $INTERFACE channel | egrep '^\W*Channel' |  sed -r 's/^\W*Channel ([0-9]{2,3}).*$/\1/'`

#channel_list='6 11 44 60 100 132'
#channel_list='44 60 100'

# Print out supported channel list
printf "[${GREEN}i${NC}] Supported channel list: [ "
echo -n $channel_list
echo " ]"

# Hop between each supported channel in a loop

while true
do

	for i in $channel_list
	do

		#printf "[${GREEN}i${NC}] Setting channel $i\n"

		sudo iw $INTERFACE set channel $i

		sleep $INTERVAL

	done

done
