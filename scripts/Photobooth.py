import img_logic
from led_logic import LED
import pygame
from time import sleep
import RPi.GPIO as GPIO

#maxres imgW = 3280, imgH = 2464

#GLOBAL VARIABLES
debug = True
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

class Photobooth:
    def __init__(self):
        if(debug == True):
            print("Running init")
        self._running = True
        self._display_surf = None
        self.led = LED()
        
        
    def on_init(self):
        if(debug == True):
            print("Running on_init")
        pygame.init()
        self.displayInfo = pygame.display.Info()
        self._display_surf = pygame.display.set_mode((self.displayInfo.current_w, self.displayInfo.current_h), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False) #hide the mouse cursor
        self._running = True
        self.myfont = pygame.font.SysFont('dejavusans', 60)
        GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        GPIO.add_event_detect(15, GPIO.RISING, bouncetime=5)
        
        
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            self._running = False
            
            
    def on_loop(self):
        self.led.colorWheel()
        if GPIO.event_detected(15): #Run gpio event since last loop
            buttonPress()
            
    
    def on_render(self):
        self.set_Message('Idle')
        
    
    def on_cleanup(self):
        self.led.cleanup()
        if(debug == True):
            print("Turning off LED")
        pygame.quit()
        if(debug == True):
            print("Pygame quit")
        GPIO.cleanup()
        if(debug == True):
            print("GPIO cleaned up")
            
    
    def set_Message(self, state):
        self._display_surf.fill(white)
        self.textsurface = self.myfont.render(setMessage(state), False, (0, 0, 0))
        self._display_surf.blit(self.textsurface,(self.displayInfo.current_w // 4, self.displayInfo.current_h // 2))
        pygame.display.flip()
        
    
    ##IMPORTANT STOP PUTTING DEFS HERE##
    def on_execute(self):
        if(debug == True):
            print("Running on_execute")
        if self.on_init() == False:
            self._running = False
            
        #Main Loop
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    ##END IMPORTANT AREA##
##END CLASS##
    
#Method to set display text
def setMessage(state):
    if(state == 'Idle'):
        message = 'Please press button to begin countdown'
    elif(state == 'Pressed'):
        message = 'Please wait...'
    elif(state == 'Button'):
        message = "Button pressed"
    else:
        message = 'Something went wrong setting message'
    return message

#Actions to take when button is pressed
def buttonPress():
    if(debug == True):
        print("Button press registered")
    
    GPIO.remove_event_detect(15)
    
    thePhotobooth.set_Message('Pressed')
    img_logic.pointShoot(thePhotobooth.led)
    pygame.event.clear()

    GPIO.add_event_detect(15, GPIO.RISING, bouncetime=5)

    
if __name__ == "__main__":
    thePhotobooth = Photobooth()
    thePhotobooth.on_execute()