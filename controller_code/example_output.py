from neopixel import Neopixel
import machine
from time import sleep
from hall_reader import *


LIGHTS = [
[63, 62, 61, 60, 59, 58, 57, 56],
[48, 49, 50, 51, 52, 53, 54, 55],
[47, 46, 45, 44, 43, 42, 41, 40],
[32, 33, 34, 35, 36, 37, 38, 39],
[31, 30, 29, 28, 27, 26, 25, 24],
[16, 17, 18, 19, 20, 21, 22, 23],
[15, 14, 13, 12, 11, 10,  9,  8],
[ 0,  1,  2,  3,  4,  5,  6,  7]
]



# Create an 'object' for our Hall Effect Sensor
# When sensor is near magnet, signal is pulled to zero volts
Hall_Input = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

numpix = 64
pixels = Neopixel(numpix, 0, 9, "GRB")
 
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (140, 140, 140)
cyan = (0, 255, 255)

pixels.brightness(255)

for i in range(64):
    if i % 2 == 0:
        pixels.set_pixel(i, blue)
    else:
        pixels.set_pixel(i, white)
    

while True:
    # Main loop to read signals
    signals = read_all_signals()
    for i in range(len(signals)):

        if signals[i] == 0:
            pixels.set_pixel(i, eval("(0, 255, 0)"))
        elif i % 2 == 0:
            pixels.set_pixel(i, blue)
        else:
            pixels.set_pixel(i, white)
 
    pixels.show()
    sleep(.05) 