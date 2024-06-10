#!/usr/bin/env python

# Write text to GPIO-connected OLED displays
#
# Modified by: Jim Nicholson
# Based on code by: Michael Klements
# Base on Adafruit CircuitPython & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
import time
import board
import busio
import digitalio

import RPi.GPIO as GPIO

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 32
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# How to address LEDs via GPIO:
leds = [5, 6, 19, 13]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(len(leds)):
    GPIO.setup(leds[i], GPIO.OUT)

# Clear display.
oled.fill(0)
oled.show()

width = oled.width
height = oled.height

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('dogicapixel.ttf', 8)
#font = ImageFont.load_default()

try:

    led = 0
    
    while True:
        GPIO.output(leds[led], GPIO.HIGH)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )

        cmd = "iwgetid -r"
        WIFI = subprocess.check_output(cmd, shell = True)
        
        cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
        Temp = subprocess.check_output(cmd, shell = True )

        # Pi Stats Display
        draw.text((0,0), f"{str(WIFI, 'utf-8')}", font=font, fill=255)
        draw.text((0, 10), f"IP: {str(IP,'utf-8')}", font=font, fill=255)
        draw.text((0, 20), f"Temp: {str(Temp,'utf-8')}", font=font, fill=255)
            
        # Display image
        oled.image(image)
        oled.show()
        time.sleep(LOOPTIME)
        GPIO.output(leds[led], GPIO.LOW)
        led += 1
        if led > 3:
            led = 0
except KeyboardInterrupt:
        print("\nExiting...")
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        oled.image(image)
        oled.show()
