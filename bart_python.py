# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import requests
import xml.etree.ElementTree as ET
from neopixel import *


# LED strip configuration:
LED_COUNT   = 120      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

def one(strip, wait_seconds=10):
	url = 'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=embr&key=MW9S-E7SL-26DU-VV8V'
	r = requests.get(url)
	root = ET.fromstring(r.text)
	result = ""
	color = ""
	blackout(strip)
	for station in root.findall('station'):
		for name in station.findall('name'):
			result += name.text
			for etd in station.findall('etd'):
				for destination in etd.findall('destination'):
					result += " " + destination.text + " "
				for estimate in etd.findall('estimate'):
					for direction in estimate.findall('direction'):
						direction = direction.text
					for hexColor in estimate.findall('hexcolor'):
						color = hexColor.text
						red = int(color[1:3], 16) - 100
						green = int(color[3:5], 16) - 100
						blue = int(color[5:7], 16) - 100
						if red < 0:
							red = 0
						if green < 0:
							green = 0
						if blue < 0:
							blue = 0
					print red, green, blue, color
					for minutes in estimate.findall('minutes'):
						etd_minutes = minutes.text
						if etd_minutes == "Leaving":
							etd_minutes = 0
						else:
							etd_minutes = int(etd_minutes)
						if direction == "South":
							strip.setPixelColor(etd_minutes, Color(red,green,blue))
							result += " " + minutes.text + " minutes"
	print result
	strip.show()
	time.sleep(wait_seconds)

def blackout(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i,Color(0,0,0))

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	print 'Press Ctrl-C to quit.'
	while True:
		one(strip)
