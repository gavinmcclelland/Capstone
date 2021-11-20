# Interfacing with 2.4 inch 240x320 SPI LCD

# ==================== LIBS ====================

# Image
import textwrap
import numpy
from PIL import Image, ImageDraw, ImageChops

# Others
import time
import numbers
from types import MethodType

# ==================== CONSTANTS ====================

# Display size
ILI9341_TFTWIDTH    = 240
ILI9341_TFTHEIGHT   = 320

# Interacting with display registers
ILI9341_SWRESET     = 0x01
ILI9341_SLPOUT      = 0x11
ILI9341_INVOFF      = 0x20
ILI9341_INVON       = 0x21
ILI9341_GAMMASET    = 0x26
ILI9341_DISPON      = 0x29
ILI9341_CASET       = 0x2A
ILI9341_PASET       = 0x2B
ILI9341_RAMWR       = 0x2C
ILI9341_RAMRD       = 0x2E
ILI9341_MADCTL      = 0x36
ILI9341_PIXFMT      = 0x3A
ILI9341_FRMCTR1     = 0xB1
ILI9341_DFUNCTR     = 0xB6

ILI9341_PWCTR1      = 0xC0
ILI9341_PWCTR2      = 0xC1
ILI9341_VMCTR1      = 0xC5
ILI9341_VMCTR2      = 0xC7
ILI9341_GMCTRP1     = 0xE0
ILI9341_GMCTRN1     = 0xE1

MADCTL_MY           = 0x80
MADCTL_MX           = 0x40
MADCTL_MV           = 0x20
MADCTL_ML           = 0x10
MADCTL_RGB          = 0x00
MADCTL_BGR          = 0x08
MADCTL_MH           = 0x04

# ==================== IMAGE BUFFER ====================

image_buffer = None

class TFT_ILI9341():

    # ==================== INIT CLASS ====================

    def __init__(self, spi, gpio, landscape=False):
        self.width = ILI9341_TFTWIDTH
        self.height = ILI9341_TFTHEIGHT
        self.is_landscape = landscape
        self._spi = spi
        self._gpio = gpio

    # ==================== SEND DATA ====================

    def send_to_lcd(self, data, is_data=True, chunk_size=4096):

        # Set DC low for command, high for data.
        self._gpio.output(self._dc, is_data)
        self._spi.open(0, self._ce_lcd)
        self._spi.max_speed_hz=self._spi_speed_lcd

        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]
        # Write data a chunk at a time.
        for start in range(0, len(data), chunk_size):
            end = min(start+chunk_size, len(data))
            self._spi.writebytes(data[start:end])
        self._spi.close()

    def command(self, command):
        """Write a byte or array of bytes to the display as command data."""
        self.send_to_lcd(command, is_data=False)

    def data(self, data):
        """Write a byte or array of bytes to the display as display data."""
        self.send_to_lcd(data, is_data=True)

    def reset_lcd(self):
        if self._rst is not None:
            self._gpio.output(self._rst, self._gpio.HIGH)
            time.sleep(0.005)
            self._gpio.output(self._rst, self._gpio.LOW)
            time.sleep(0.02)
            self._gpio.output(self._rst, self._gpio.HIGH)
            time.sleep(0.150)
        else:
            self.command(ILI9341_SWRESET)
            time.sleep(1)

    def set_rotation(self, rotation):

        self.command(ILI9341_MADCTL)
        rotation = rotation % 4
        if (rotation == 0):
            self.data(MADCTL_MX | MADCTL_BGR)
            self.width  = ILI9341_TFTWIDTH
            self.height = ILI9341_TFTHEIGHT
        elif (rotation == 1):
            self.data(MADCTL_MV | MADCTL_BGR)
            self.width  = ILI9341_TFTHEIGHT
            self.height = ILI9341_TFTWIDTH
        elif (rotation == 2):
            self.data(MADCTL_MY | MADCTL_BGR)
            self.width  = ILI9341_TFTWIDTH
            self.height = ILI9341_TFTHEIGHT
        elif (rotation == 3):
            self.data(MADCTL_MX | MADCTL_MY | MADCTL_MV | MADCTL_BGR)
            self.width  = ILI9341_TFTHEIGHT
            self.height = ILI9341_TFTWIDTH

    # ==================== INIT LCD ====================

    def init_ili9341(self):
        self.command(ILI9341_PWCTR1)
        self.data(0x23)
        self.command(ILI9341_PWCTR2)
        self.data(0x10)
        self.command(ILI9341_VMCTR1)
        self.data([0x3e, 0x28])
        self.command(ILI9341_VMCTR2)
        self.data(0x86)
        self.set_rotation(0 if not self.is_landscape else 1)
        self.command(ILI9341_PIXFMT)
        self.data(0x55)
        self.command(ILI9341_FRMCTR1)
        self.data([0x00, 0x18])
        self.command(ILI9341_DFUNCTR)
        self.data([0x08, 0x82, 0x27])
        self.command(0xF2)
        self.data(0x00)
        self.command(ILI9341_GAMMASET)
        self.data(0x01)
        self.command(ILI9341_GMCTRP1)
        self.data([0x0F, 0x31, 0x2b, 0x0c, 0x0e, 0x08, 0x4e, 0xf1, 0x37, 0x07, 0x10, 0x03, 0x0e, 0x09, 0x00])
        self.command(ILI9341_GMCTRN1)
        self.data([0x00, 0x0e, 0x14, 0x03, 0x11, 0x07, 0x31, 0xc1, 0x48, 0x08, 0x0f, 0x0c, 0x31, 0x36, 0x0f])
        self.command(ILI9341_SLPOUT)
        time.sleep(0.120)
        self.command(ILI9341_DISPON)

    def init_lcd(self, dc=None, rst=None, led=None, ce=0, spi_speed=32000000):
        global image_buffer
        self._dc = dc
        self._rst = rst
        self._led = led
        self._ce_lcd = ce
        self._spi_speed_lcd=spi_speed
        # Set DC as output.
        self._gpio.setup(dc, self._gpio.OUT)
        # Setup reset as output (if provided).
        if rst is not None:
            self._gpio.setup(rst, self._gpio.OUT)
        if led is not None:
            self._gpio.setup(led, self._gpio.OUT)
            self._gpio.output(led, self._gpio.HIGH)

        # Create an image buffer.
        if self.is_landscape:
           image_buffer = Image.new('RGB', (ILI9341_TFTHEIGHT, ILI9341_TFTWIDTH))
        else:
            image_buffer = Image.new('RGB', (self.width, self.height))
        # and a previous frame buffer for determining area to draw
        self.image_buffer_2 = image_buffer.copy()
        # and a backup buffer for backup/restore
        self.prev_image_buffer = None
        self.prev_pixel_array = [0, 0] * (self.width * self.height)
        self.reset_lcd()
        self.init_ili9341()

    # ==================== DISPLAYING ====================

    def set_frame(self, x0=0, y0=0, x1=None, y1=None):

        if x1 is None:
            x1 = self.width-1
        if y1 is None:
            y1 = self.height-1
        self.command(ILI9341_CASET)        # Column addr
        self.data([x0 >> 8, x0, x1 >> 8, x1])
        self.command(ILI9341_PASET)        # Row addr
        self.data([y0 >> 8, y0, y1 >> 8, y1])
        self.command(ILI9341_RAMWR)

    def display(self, image=None):
        """Write the display buffer or provided image to the hardware.  If no
        image parameter is provided the display buffer will be written to the
        hardware.  If an image is provided, it should be RGB format and the
        same dimensions as the display hardware.
        """

        # startTime = time.time()

        # By default write the internal buffer to the display.
        if image is None:
            image = image_buffer
        if image.size[0] == self.height:
            image = image.rotate(90)

        # Set address bounds to entire display.
        self.set_frame()
        # Convert image to array of 16bit 565 RGB data bytes.
        pixel_bytes = list(self.image_to_data(image))
        # Write data to hardware.
        self.data(pixel_bytes)

        # timeInterval = time.time() - startTime
        # print(str(round(timeInterval, 3)))

    def pen_print(self, position, size, color=(0,0,0) ):
        x=position[0]
        y=position[1]
        self.set_frame(x, y-size, x+size, y+size)
        pixel_bytes=[0]*(size*size*8)
        self.data(pixel_bytes)

    def clear(self, color=(0,0,0)):
        """
        Clear the image buffer to the specified RGB color (default black).
        USE (r, g, b) NOTATION FOR THE COLOUR !!
        """

        if type(color) != type((0,0,0)):
            print("clear() function colours must be in (255,255,0) form")
            exit()
        width, height = image_buffer.size
        image_buffer.putdata([color]*(width*height))
        #self.display()

    def get_draw_buffer(self):
        """Return a PIL ImageDraw instance for drawing on the image buffer."""
        draw_buffer = ImageDraw.Draw(image_buffer)
        # Add custom methods to the draw object:
        draw_buffer.textrotated = MethodType(_textrotated, draw_buffer)
        draw_buffer.pasteimage = MethodType(_pasteimage, draw_buffer)
        draw_buffer.textwrapped = MethodType(_textwrapped, draw_buffer)
        return draw_buffer

    def get_image_buffer(self):
        global image_buffer
        return image_buffer

    def load_wallpaper(self, filename):
        # The image should be 320x240 or 240x320 only (full wallpaper!). Errors otherwise.
        # We need to cope with whatever orientations file image and TFT canvas are.
        image = Image.open(filename)
        if image.size[0] > image_buffer.size[0]:
            image_buffer.paste(image.rotate(90))
        elif image.size[0] < image_buffer.size[0]:
            image_buffer.paste(image.rotate(-90))
        else:
            image_buffer.paste(image)

    def image_to_data(self, image):
        """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
        # Based on Adafruit ILI9341 python project

        bounds = None
        forceDraw = True if self.prev_image_buffer is None else False

        # Get bounding box of difference between this image and previously displayed image
        if(self.prev_image_buffer is not None):
            bounds = ImageChops.difference(image, self.prev_image_buffer).getbbox()
        else:
            self.prev_image_buffer = image.copy()

        if(bounds is not None):
            startX, startY = (bounds[0], bounds[1])
            width, height = (bounds[2], bounds[3])           

        if(forceDraw):
            startX, startY = (0, 0)
            width, height = image.size

        if(forceDraw or bounds is not None):

            # startTime = time.time()
            pixels = image.convert('RGB').load()
            for y in range(startY, height):
                for x in range(startX, width):
                    r,g,b = pixels[(x, y)]
                    color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                    self.prev_pixel_array[(y * self.width + x) * 2 + 0] = (color >> 8) & 0xFF
                    self.prev_pixel_array[(y * self.width + x) * 2 + 1] = color & 0xFF

            # timeInterval = time.time() - startTime
            # print(str(round(timeInterval, 3)))

        self.prev_image_buffer.paste(image)
        return self.prev_pixel_array

        # timeInterval = time.time() - startTime
        # print(timeInterval)

        # startTime = time.time()

        # # # img_bytes = BytesIO()
        # # # image.save(img_bytes, format='BMP')
        # # # img_bytes = img_bytes.getvalue()

        # # pixels = list(image.getdata())
        # # width, height = image.size
        # # pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

        # # pixels = numpy.array(image)
        # #pixels = image.convert('RGB').load()
        # #pixels = [(r, g, b) for p in pixels]

        # timeInterval = time.time() - startTime
        # print(pixels)
        # print(timeInterval)

        # return pixels
        
    # ==================== 2ND BUFFER ====================

    def backup_buffer(self):
        self.image_buffer_2.paste(image_buffer)

    def restore_buffer(self):
        image_buffer.paste(self.image_buffer_2)

    # ==================== ON / OFF ====================

    def invert(self, setOn):
        if setOn:
            self.command(ILI9341_INVON)
        else:
            self.command(ILI9341_INVOFF)

    def backlight(self, setOn):
        if self._led is not None:
            self._gpio.output(self._led, setOn)

 # ==================== CUSTOM FUNCTIONS FOR draw() IN LCD CANVAS SYSTEM ====================

# Import these extra functions below as new custom methods of the PIL "draw" function:
# Hints on this custom method technique:
# http://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc

def _textrotated(self, position, text, angle, font, fill="white"):
    # Define a function to create rotated text.
    # Source of this rotation coding: Adafruit ILI9341 python project
    # "Unfortunately PIL doesn't have good
    # native support for rotated fonts, but this function can be used to make a
    # text image and rotate it so it's easy to paste in the buffer."
    width, height = self.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the TFT canvas image, using text itself as a mask for transparency.
    image_buffer.paste(rotated, position, rotated)  # into the global Buffer
    #   example:  draw.textrotated(position, text, angle, font, fill)

def _pasteimage(self, filename, position):
    image_buffer.paste(Image.open(filename), position)
    # example: draw.pasteimage('bl.jpg', (30,80))

def _textwrapped(self, position, text1, length, height, font, fill="white"):
    text2=textwrap.wrap(text1, length)
    y=position[1]
    for t in text2:
        self.text((position[0],y), t, font=font, fill=fill)
        y += height
    # example:  draw.textwrapped((2,0), "but a lot longer", 50, 18, myFont, "black")

#        All colours may be any notation:
#        (255,0,0)  =red    (R, G, B)
#        0x0000FF   =red    BBGGRR
#        "#FF0000"  =red    RRGGBB
#        "red"      =red    html colour names, insensitive
