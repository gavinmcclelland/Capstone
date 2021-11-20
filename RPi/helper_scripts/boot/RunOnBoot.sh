#!/bin/bash

echo "Running boot scripts..."

echo "Running boot scripts at " `date` >> /home/pi/helper_scripts/boot/boot_scripts.txt

timeout 5 /home/pi/helper_scripts/SetupWiFiMonitorMode.sh >> /home/pi/helper_scripts/boot/boot_scripts.txt
timeout 5 /home/pi/helper_scripts/ForceIPv4_eth0.sh >/dev/null 2>&1

pushd /home/pi/ili9341_lcd/lcd_data_display/ >/dev/null
nohup ./lcd_data_display.py >/dev/null 2>&1 &
popd >/dev/null

echo "Done." >> /home/pi/helper_scripts/boot/boot_scripts.txt
echo " " >> /home/pi/helper_scripts/boot/boot_scripts.txt

echo "Done."
