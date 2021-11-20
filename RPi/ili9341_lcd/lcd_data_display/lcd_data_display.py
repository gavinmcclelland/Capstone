#!/usr/bin/python3

# ==================== LIBS ====================

# OS stuff
import os
import signal
import atexit
import threading
import subprocess as sub
from past.builtins import execfile

# Display stuff
import spidev
import RPi.GPIO as GPIO
from TFT_ILI9341 import TFT_ILI9341
from PIL import Image, ImageDraw, ImageFont

# Time stuff
import time
from datetime import datetime, timezone, timedelta

# ==================== CONSTANTS ====================

# For LCD TFT SCREEN
DC_GPIO_PIN = 24
RST_GPIO_PIN = 25
LED_GPIO_PIN = 15

DISPLAY_UPDATE_INTERVAL = 1 # seconds

# Command to get IP address, plus the first argument as the interface name
GET_IP_ADDRESS_COMMAND = ['/home/pi/helper_scripts/GetIPAddress.sh']
# Command to get system uptime
GET_UPTIME_COMMAND = ['cat'] + ['/proc/uptime']
# Command to get the current WiFi channel for a wireless interface
GET_WIFI_CHANNEL_COMMAND = ['/home/pi/helper_scripts/GetCurrentWiFiChannel.sh']

ETH0_INTERFACE = 'eth0'
WLAN0_INTERFACE = 'wlan0'
WLAN1_INTERFACE = 'wlan1'

# ==================== SETUP DISPLAY ====================

# This will tell the rendering code to use real data
localTest = False

updateLCDFunctionTimer = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup screen
TFT = TFT_ILI9341(spidev.SpiDev(), GPIO, landscape=True)
TFT.init_lcd(DC_GPIO_PIN, RST_GPIO_PIN, LED_GPIO_PIN)

# Get the PIL Draw object to start drawing on the display buffer.
draw = TFT.get_draw_buffer()

# Number of times screen was rendered
frame = 0

# ==================== UPDATE LCD ====================

def update_lcd():

    # ==================== CLEAR ====================

    TFT.clear()

    # ==================== RENDER ====================
    
    execfile('render_display.py')
    global frame
    frame += 1

    # ==================== DRAW ====================

    TFT.display()
    
    global updateLCDFunctionTimer
    if(updateLCDFunctionTimer is not None):
        updateLCDFunctionTimer.cancel()
    updateLCDFunctionTimer = threading.Timer(DISPLAY_UPDATE_INTERVAL, update_lcd)
    updateLCDFunctionTimer.start()
    

# ==================== EXIT HANDLER ====================

def exit_handler():

    # Stop the timer
    if(updateLCDFunctionTimer is not None):
        updateLCDFunctionTimer.cancel()

    try:

        # Remove the current PID file if it exists
        os.remove('current_pid.txt')
        print('Removed current PID file on exit (This PID: ' + str(os.getpid()) + ')')

    except:

        # Otherwise, there is nothing to do
        print('No current PID to remove on exit (This PID: ' + str(os.getpid()) + ')')
        pass


# ==================== MAIN ====================

if __name__ == "__main__":
    
    # ==================== CHECK SINGLE INSTANCE ====================

    # If this script is already running (i.e. on startup)
    # And another one is ran, terminate the previous one since this one is a new version
    
    try:
        
        # Get the PID of the previously running script from a text file
        with open('current_pid.txt', 'r') as previousPIDFile:
            previousPIDString = previousPIDFile.readline()

            # If there is a PID recorded, terminate the previous script
            if(previousPIDString.strip() != ''):
                
                try:

                    # This will work if the script is still running
                    os.kill(int(previousPIDString), signal.SIGTERM)
                    print('Terminated previous script with PID ' + previousPIDString + ' (This PID: ' + str(os.getpid()) + ')')

                except ProcessLookupError:
                    
                    # If there is no process with that PID anymore, do nothing
                    print('No process with previous PID ' + previousPIDString + ' (This PID: ' + str(os.getpid()) + ')')
                    pass

    except FileNotFoundError:

        # If there is no current PID file, the previous script does not need to be closed
        print('No previous PID file to check on start (This PID: ' + str(os.getpid()) + ')')
        pass

    # Now record the PID of this script to the same text file for doing this check the next time
    with open('current_pid.txt', 'w') as currentPIDFile:
        print(str(os.getpid()), end='', file=currentPIDFile)

    # Register handler to delete current PID file on exit
    atexit.register(exit_handler)

    # ==================== DISPLAY ====================

    # Call update lcd function which keep being called using a timer
    update_lcd()
