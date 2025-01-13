from neopixel import Neopixel
import machine
from time import sleep
from hall_reader import *

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
        
pixels.show()

def set_led_colors(colors):
    colors = eval(colors)
    for i in range(len(colors)):
        pixels.set_pixel(i, colors[i])

def read_signals():
    print(read_all_signals)
