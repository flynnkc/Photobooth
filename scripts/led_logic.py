from time import sleep
import board
import neopixel

debug = True

class LED:
    def __init__(self):
        #GLOBAL VARIABLES
        #Raspberry Pi data pin
        self.pixel_pin = board.D18

        #Total number of pixels
        self.num_pixels = 24

        #Type of neopixel colors
        self.ORDER = neopixel.RGBW
        
        #Create NeoPixel object
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=1.0, auto_write=False, pixel_order=self.ORDER)
        
        #Colorwheel Iteration Control
        self.j = 0


    #Turn on flash
    def flash_on(self):
        self.pixels.brightness = 1.0
        self.pixels.fill((0, 0, 0, 255))
        self.pixels.show()

    #Turn off flash
    def flash_off(self):
        self.pixels.brightness = 0
        self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        
    def led_fill(self, r, g, b, w):
        self.pixels.fill((r, g, b, w))
        self.pixels.show()
        
    def cleanup(self):
        self.pixels.deinit()
        if(debug == True):
            print("LED Cleaned up")
        

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b, 0)

    def rainbow_cycle(self, wait):
        #for j in range(255):
        if(self.j > 254):
            self.j = 0
        for i in range(self.num_pixels):
            pixel_index = (i * 256 // self.num_pixels) + self.j
            self.pixels[i] = self.wheel(pixel_index & 255)
            self.j += 1
        self.pixels.show()
        sleep(wait)
            
    def colorWheel(self):
        self.pixels.brightness = 0.2
        self.rainbow_cycle(0.001) # rainbow cycle with 1ms delay per step
            
            
######################################################################################
#                                                                                    #
# Running this file will cause colorwheel to run briefly and then turn off all LEDs. #
# This is handy as if something goes wrong there is a good chance that the LEDs will #
#                          become "stuck" in the on position.                        #
######################################################################################
if __name__ == "__main__":
    led = LED()
    led.flash_on()
    sleep(1)
    led.flash_off()
