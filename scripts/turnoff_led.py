import board
import neopixel

##################################################################
#  This script exists because the NeoPixel ring I am using for   #
#  flash kept freezing and getting stuck in the "on" condition.  #
#  This script was meant to shut off LEDs on Neopixel ring.      #
##################################################################

pixel_pin = board.D18
num_pixels = 24
ORDER = neopixel.RGBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness = 0, auto_write = False, pixel_order=ORDER)

pixels.fill((0,0,0,0))
