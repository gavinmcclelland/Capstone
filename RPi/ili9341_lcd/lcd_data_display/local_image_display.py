#!/usr/bin/python3

# ==================== LIBS ====================

# OS stuff
import os
import threading
from past.builtins import execfile

# Display stuff
import webbrowser
from PIL import Image, ImageDraw, ImageFont

# Time stuff
import time
from datetime import datetime, timezone, timedelta

# ==================== CONSTANTS ====================

# Display size
ILI9341_TFTWIDTH    = 240
ILI9341_TFTHEIGHT   = 320

# Dummy TFT display class fo store the display size
# Needed to keep the rendering code the same between the LCD version and this local image version
class TFT_ILI9341():

    def __init__(self, landscape=False):
        self.landscape = landscape

        if self.landscape:
            self.width = ILI9341_TFTHEIGHT
            self.height = ILI9341_TFTWIDTH
        else:
            self.width = ILI9341_TFTWIDTH
            self.height = ILI9341_TFTHEIGHT

        self.image_buffer = Image.new('RGB', (self.width, self.height))

    def get_draw_buffer(self):
        return ImageDraw.Draw(self.image_buffer)

    def get_image_buffer(self):
        return self.image_buffer
        
# ==================== SETUP DISPLAY ====================

# This will tell the rendering code to use mock data
localTest = True

# Get the create instance of "screen"
# and get PIL Draw object to start drawing on the display buffer
TFT = TFT_ILI9341(landscape=True)
draw = TFT.get_draw_buffer()

# Number of times screen was rendered
frame = 0

def update_lcd():

    # ==================== RENDER ====================
    
    execfile('render_display.py')

    # ==================== DRAW ====================

    TFT.get_image_buffer().save("screen.png")
    #webbrowser.open("screen.png")


# ==================== MAIN ====================

if __name__ == "__main__":
    
    # ==================== DISPLAY ====================

    update_lcd() 
            