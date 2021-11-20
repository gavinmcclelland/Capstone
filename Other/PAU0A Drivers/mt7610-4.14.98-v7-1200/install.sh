#!/bin/bash

kernel=$(uname -r)
driver=mt7610

module_bin="mt7610u.ko"
module_dir="/lib/modules/$kernel/kernel/drivers/net/wireless"

sudo mkdir -p /etc/Wireless/RT2870STA/
sudo cp RT2870STA.dat /etc/Wireless/RT2870STA/
sudo cp *.bin /lib/firmware

if [ -f 95-ralink.rules ] ; then
	sudo mv 95-ralink.rules /etc/udev/rules.d/
	echo "1"
elif [ -f /etc/udev/rules.d/95-ralink.rules ] ; then
	sudo rm /etc/udev/rules.d/95-ralink.rules
	echo "2"
fi

echo "sudo install -p -m 644 $module_bin $module_dir"
sudo install -p -m 644 $module_bin $module_dir
echo "sudo depmod $kernel"
sudo depmod $kernel
#rm $module_bin
#rm -f $driver* > /dev/null 2>&1

echo
echo "Reboot to run the driver."
echo
echo "If you have already configured your wifi it should start up and connect to your"
echo "wireless network."
echo
echo "If you have not configured your wifi you will need to do that to enable the wifi."

#rm -f install.sh  > /dev/null 2>&1
