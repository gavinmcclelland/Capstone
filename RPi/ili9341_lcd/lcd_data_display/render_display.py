from PIL import Image
from operator import itemgetter
from random import sample, randint

# Top section
TOP_SECTION_TOP_MARGIN = -1
TOP_SECTION_BOTTOM_PADDING = 4

# Bottom section
BOTTOM_SECTION_RIGHT_MARGIN = 2
BOTTOM_SECTION_BOTTOM_MARGIN = 1
BOTTOM_VERTICAL_SEPARATOR_1_X_POS = 120
BOTTOM_VERTICAL_SEPARATOR_2_X_POS = 210

# Piegraph
PIEGRAPH_MAX_TYPES = 4 # This many types will be separate, rest will be grouped into "other" category
PIEGRAPH_RADIUS = 92
PIEGRAPH_BOTTOM_MARGIN = 20
PIEGRAPH_RIGHT_MARGIN = 6
PIEGRAPH_TEXT_LEFT_MARGIN = 6

# Bargraph
BARGRAPH_TICK_SIZE = 2
BARGRAPH_BAR_SIZE = 10
typeColors = ['YELLOW', 'MAGENTA', 'CYAN', 'LIME', 'ORANGE']
BARGRAPH_LEFT_MARGIN = 20
BARGRAPH_BOTTOM_MARGIN = 20
BARGRAPH_HEIGHT = 92
BARGRAPH_WIDTH = 200

 # Fonts
tinyFont=ImageFont.truetype('basis33.ttf', 16)
smallFont=ImageFont.truetype('basis33.ttf', 32)
mediumFont=ImageFont.truetype('basis33.ttf', 32)
largeFont=ImageFont.truetype('basis33.ttf', 48)
veryLargeFont=ImageFont.truetype('FreeSans.ttf', 64)

# Heights of fonts (for positioning)
_, tinyFontHeight = draw.textsize(' ', font=tinyFont)
_, smallFontHeight = draw.textsize(' ', font=smallFont)
_, mediumFontHeight = draw.textsize(' ', font=mediumFont)
_, largeFontHeight = draw.textsize(' ', font=largeFont)
_, veryLargeFontHeight = draw.textsize(' ', font=veryLargeFont)

# Texts with colors for each part
# Each [COLOR] control label makes all the text after it that color up to the next control label
TITLE_LABEL = '[GREY]------- [CYAN]Wi-Wait [GREY]-------'
TITLE_LABEL_HIGHLIGHT = '        [CORAL]Wi-Wait        '
ETHERNET_LABEL = '[GREY]Ethr: '
WLAN_LABEL = '[GREY]WLAN: '
CHANNEL_LABEL = '[GREY]Ch: '
STATUS_LABEL = '[GREY]Status: '
UPTIME_LABEL = '[GREY]Up: '

image_buffer = TFT.get_image_buffer()

# ==================== HELPER DRAW FUNCTIONS ====================

# Checks if the given IP addres (string) is empty
# If so sets text to 'Not connected' and color to red
# Otherwise text is passed through and color is green
def process_IP_address_text(text):
    color = 'GREEN'
    if(text.strip() == ''):
        #text = 'Not connected'
        text = 'N/A'
        color = 'RED'
    return text, color

def draw_text(xPos, yPos, textToDraw, fontToUse):

    # If text does not specify a starting color, assume white
    if(not textToDraw.startswith('[')):
        textToDraw = '[WHITE]' + textToDraw

    # Split on opening square bracket to produce items containing 'COLOR]TEXT'
    textParts = textToDraw.split('[')

    # Text data used for drawing
    texts = []
    colors = []
    widths = []

    # Process each text part (each one is a certain color)
    currentIndex = -1
    for currentTextPart in textParts:
        currentIndex += 1
        
        # Discard any empty elements since they are useless (left over from previous split)
        if(currentTextPart == ''):
            continue

        # Get the color and text of each part
        currentTextPartSplit = currentTextPart.split(']')
        color = currentTextPartSplit[0]
        text = currentTextPartSplit[1]
        texts.append(text)
        colors.append(color)

        # Get the size of the current text part
        width, _ = draw.textsize(text, font=fontToUse)

        widths.append(width)

    # Draw each text part in its color
    currentIndex = -1
    for currentText in texts:
        currentIndex += 1

        # Get the current color to use 
        currentColor = colors[currentIndex]
        
        # The x offset for the current text part is the sum of all the widths up to this point
        xOffset = sum(widths[:currentIndex])

        # Draw the current text part 
        draw.text((xPos + xOffset, yPos), currentText, fill=currentColor, font=fontToUse)

        #print(xOffset, currentColor, currentText)

    # print(texts, colors, widths)


# ==================== RENDER DISPLAY ====================

# ==================== TITLE ====================
    
# Title label
draw_text(1, 0, TITLE_LABEL_HIGHLIGHT, smallFont)
draw_text(0, 0 + TOP_SECTION_TOP_MARGIN, TITLE_LABEL, smallFont)

# Separator line under title
draw.line((0, smallFontHeight + TOP_SECTION_TOP_MARGIN + TOP_SECTION_BOTTOM_PADDING, TFT.width, smallFontHeight + TOP_SECTION_TOP_MARGIN + TOP_SECTION_BOTTOM_PADDING), fill='GREY', width=1)

# ==================== # OF PEOPLE ====================

peopleIconImage = Image.open('People.png', 'r')
image_buffer.paste(peopleIconImage, (BARGRAPH_LEFT_MARGIN, 40), peopleIconImage)

draw_text(BARGRAPH_LEFT_MARGIN + 40, 38, "15", largeFont)

# ==================== IP ADDRESSES ====================

# For Ethernet
EthernetIP = '' if localTest else sub.check_output(GET_IP_ADDRESS_COMMAND + [ETH0_INTERFACE]).decode('ascii')
EthernetIP,EthernetIPColor = process_IP_address_text(EthernetIP)
#EthernetIPText = ETHERNET_LABEL + '[' + EthernetIPColor + ']' + EthernetIP
EthernetIPText = '  [' + EthernetIPColor + ']' + EthernetIP
draw_text(BOTTOM_SECTION_RIGHT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN, EthernetIPText, tinyFont)

# For WLAN
WlanIP = '192.168.1.20' if localTest else sub.check_output(GET_IP_ADDRESS_COMMAND + [WLAN0_INTERFACE]).decode('ascii')
WlanIP,WlanIPColor = process_IP_address_text(WlanIP)
#WlanIPText = WLAN_LABEL + '[' + WlanIPColor + ']' + WlanIP
WlanIPText = '  [' + WlanIPColor + ']' + WlanIP
draw_text(BOTTOM_SECTION_RIGHT_MARGIN, TFT.height - tinyFontHeight - BOTTOM_SECTION_BOTTOM_MARGIN, WlanIPText, tinyFont)

# Separator line above IP addresses
draw.line((0, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN, TFT.width, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN), fill='GREY', width=1)

# Separator line to right of IP addresses
draw.line((BOTTOM_VERTICAL_SEPARATOR_1_X_POS, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN, BOTTOM_VERTICAL_SEPARATOR_1_X_POS, TFT.height), fill='GREY', width=1)

wim = Image.open('WiFi.png', 'r')
eim = Image.open('Ethernet.png', 'r')

image_buffer.paste(wim, (2, TFT.height - 9), wim)
image_buffer.paste(eim, (2, TFT.height - 20), eim)

# ==================== UPTIME ====================

# Get total number of second the system has been on for
uptimeTotalSeconds = 12340 if localTest else int(sub.check_output(GET_UPTIME_COMMAND).decode('ascii').split('.')[0])

# Split into hours minutes seconds
uptimeHours = int(uptimeTotalSeconds / 3600)
uptimeMinutes = int(uptimeTotalSeconds / 60) -  uptimeHours*60
uptimeSeconds = uptimeTotalSeconds - uptimeMinutes*60

# Text is minutes:seconds if hours is 0, otherwise hours:minutes
if uptimeHours == 0:
    uptimeColor = 'CYAN'
    uptime = str(uptimeMinutes) + ':' + ('0' if uptimeSeconds < 10 else '') + str(uptimeSeconds)
else:
    uptimeColor = 'BLUE'
    uptime = str(uptimeHours) + ':' + ('0' if uptimeMinutes < 10 else '') + str(uptimeMinutes)

# Draw it
uptimeText = UPTIME_LABEL + '[' + uptimeColor + ']' + uptime
#uptimeText = '  [' + uptimeColor + ']' + uptime
draw_text(BOTTOM_VERTICAL_SEPARATOR_1_X_POS + BOTTOM_SECTION_RIGHT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN, uptimeText, tinyFont)


#clockIconImage = Image.open('Clock.png', 'r')
#image_buffer.paste(clockIconImage, (BOTTOM_VERTICAL_SEPARATOR_1_X_POS + BOTTOM_SECTION_RIGHT_MARGIN, TFT.height - tinyFontHeight*2 + 3 - BOTTOM_SECTION_BOTTOM_MARGIN), clockIconImage)


# ==================== CHANNEL ====================

channel = '7' if localTest else sub.check_output(GET_WIFI_CHANNEL_COMMAND + [WLAN0_INTERFACE]).decode('ascii')
#print('Channel:' + channel)
channelColor = 'ORANGE'
channelText = CHANNEL_LABEL + '[' + channelColor + ']' + channel
draw_text(BOTTOM_VERTICAL_SEPARATOR_1_X_POS + BOTTOM_SECTION_RIGHT_MARGIN, TFT.height - tinyFontHeight - BOTTOM_SECTION_BOTTOM_MARGIN, channelText, tinyFont)

# Separator line to right of channel & status
draw.line((BOTTOM_VERTICAL_SEPARATOR_2_X_POS, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN, BOTTOM_VERTICAL_SEPARATOR_2_X_POS, TFT.height), fill='GREY', width=1)

# ==================== STATUS ====================

status = 'ONLINE'
statusColor = 'GREEN'
statusText = STATUS_LABEL + '[' + statusColor + ']' + status
draw_text(BOTTOM_VERTICAL_SEPARATOR_2_X_POS + BOTTOM_SECTION_RIGHT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN, statusText, tinyFont)

# ==================== "HEARTBEAT" INDICATOR ====================

# Draw indicator on odd-numbered frames
heartbeatText = '' if (frame % 2 != 0) else '           *'
draw_text(BOTTOM_VERTICAL_SEPARATOR_2_X_POS + BOTTOM_SECTION_RIGHT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN, heartbeatText, tinyFont)

# ==================== DEVICES OVER TIME BARGRAPH ====================

# Lower left corner of bargraph
bargraphOrigin = (BARGRAPH_LEFT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN - BARGRAPH_BOTTOM_MARGIN)

# Get bar values
barValues = [10, 20, 40, 60, 30, 50, 40, 10, 15, 30, 45, 35, 30, 20, 15, 5, 10]
#barValues = [(randint(-5, 5) + i) for i in barValues]

for i in range(0, len(barValues)):
    barValues[i] = (randint(-3, 3) + barValues[i])

#barValues = sample(range(1000), 50)

# Calculate bar width
numberOfBars = len(barValues)
barWidth = BARGRAPH_WIDTH / numberOfBars

# Draw each bar
for currentIndex in range(0, len(barValues)):

    # Calculate parameters for current bar
    barValue = barValues[currentIndex]
    barHeight = (BARGRAPH_HEIGHT / max(barValues)) * barValue
    xOffset = barWidth * currentIndex
    barColor = 'RED'

    # Determine color
    if currentIndex == 0 or barValue > barValues[currentIndex - 1]:
        barColor = 'GREEN'

    # Draw it
    draw.rectangle((bargraphOrigin[0] + xOffset, bargraphOrigin[1], bargraphOrigin[0] + xOffset + barWidth - 2, bargraphOrigin[1] - barHeight), fill=barColor)

# X axis
draw.line((BARGRAPH_LEFT_MARGIN - BARGRAPH_TICK_SIZE, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN - BARGRAPH_BOTTOM_MARGIN, BARGRAPH_LEFT_MARGIN + BARGRAPH_WIDTH, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN - BARGRAPH_BOTTOM_MARGIN), fill='GREY', width=1)
# Y axis
draw.line((BARGRAPH_LEFT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN - BARGRAPH_BOTTOM_MARGIN + BARGRAPH_TICK_SIZE, BARGRAPH_LEFT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN - BARGRAPH_BOTTOM_MARGIN - BARGRAPH_HEIGHT), fill='GREY', width=1)

# ==================== DEVICE TYPES (stretch goal) ====================

# Upper right corner and dimensions of piegraph
piegraphTopCorner = (TFT.width - PIEGRAPH_RADIUS - PIEGRAPH_RIGHT_MARGIN, TFT.height - tinyFontHeight*2 - BOTTOM_SECTION_BOTTOM_MARGIN - PIEGRAPH_RADIUS - PIEGRAPH_BOTTOM_MARGIN)
piegraphCoordinates = (piegraphTopCorner[0], piegraphTopCorner[1], piegraphTopCorner[0] + PIEGRAPH_RADIUS, piegraphTopCorner[1] + PIEGRAPH_RADIUS)

# Get device type names and count values and sort by number of devices
typeCounts = [('Dell', 10), ('Asus', 30), ('MacOS', 45), ('Samsung', 70), ('iOS', 95), ('Acer', 15)]
typeCounts = sorted(typeCounts, key=itemgetter(1), reverse=True)
typeCountsSum = sum([type[1] for type in typeCounts])
typeNameMaxLength = max([len(type[0]) for type in typeCounts])

# Group types with lowest counts into "other" category
typesOtherSum = sum([type[1] for type in typeCounts[PIEGRAPH_MAX_TYPES:]])
#print(typeCounts[PIEGRAPH_MAX_TYPES:])
typeCounts = typeCounts[:PIEGRAPH_MAX_TYPES] + [('Other', typesOtherSum)]
typeCounts = sorted(typeCounts, key=itemgetter(1), reverse=True)

# Draw each pie slice and label
previousAngle = 0
for currentIndex in range(0, len(typeCounts)):

    # Calculate current type color and angle
    typeColor = typeColors[currentIndex]
    typeName = typeCounts[currentIndex][0]
    typeCount = typeCounts[currentIndex][1]
    typeAngle = (typeCount / typeCountsSum) * 360 + previousAngle

    # Draw pie slice (rotated -90 degrees to start at top instead of right)
    draw.pieslice(piegraphCoordinates, previousAngle - 90, typeAngle - 90, fill=typeColor)

    # Draw label (insert spaces after name to align numbers)
    typeLabelText = typeName + ':' + (' ' * (typeNameMaxLength - len(typeName)))  + ' [' + typeColor + ']' + str(typeCount)
    draw_text(piegraphTopCorner[0] + PIEGRAPH_TEXT_LEFT_MARGIN, piegraphTopCorner[1] - tinyFontHeight*(PIEGRAPH_MAX_TYPES+2) + tinyFontHeight * currentIndex, typeLabelText , tinyFont)

    # Keep track of previous angle to draw next slice statring at it
    previousAngle = typeAngle

# Draw outline
draw.ellipse(piegraphCoordinates, fill=None, outline='GREY')
# draw.ellipse((piegraphCoordinates[0] - 2, piegraphCoordinates[1] - 2, piegraphCoordinates[2] + 2, piegraphCoordinates[3] + 2), fill=None, outline='GREY')

# ==================== TIME ====================

#timeValue = datetime.now().strftime('%H:%M:%S.%f')[:-5] # With 1/10th seconds
#timeValue = datetime.now().strftime('%H:%M:%S')
