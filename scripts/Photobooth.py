from img_logic import Camera
from led_logic import LED
import pygame
from time import sleep
import RPi.GPIO as GPIO

#maxres imgW = 3280, imgH = 2464

#GLOBAL VARIABLES
debug = True

class Photobooth:

    ### Init Photobooth object, LED object, and Camera object. ###
    def __init__(self):
        if(debug == True):
            print("Running init")
        self._running = True
        self._idle = False
        self.led = LED()
        self.camera = Camera()
        
        
        
    ### Initialize pygame, get information about display, set display surface size, set display to fullscreen, and initalize GPIO pins for LEDs and arcade button. ###
    def on_init(self):
        if(debug == True):
            print('Running on_init')
        pygame.init()
        self.displayInfo = pygame.display.Info()
        self._display_surf = pygame.display.set_mode((self.displayInfo.current_w, self.displayInfo.current_h), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False) #hide the mouse cursor
        self.myfont = pygame.font.SysFont('dejavusans', 60)
        GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        GPIO.add_event_detect(15, GPIO.RISING, bouncetime=5)
        
        
    ### Pygame event detection. Set loop to end on next test if key is pressed. ###
    # Parameters:
    # event (event) :: pygame event object to detect and track user input. Any key press quits loop by setting _running to false.
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            self._running = False
            
    ### Loop events not related to display. ###    
    def on_loop(self):
        
        # Pygame event detection
        for event in pygame.event.get():
            self.on_event(event)
            
        # Runs any captured GPIO inputs since last pass
        if GPIO.event_detected(15):
            self.buttonPress()
        self.led.colorWheel()
        
            
    ### Display rendering. Sets event state to Idle once events are handled. ###
    def on_render(self):
        if self._idle is False:
            self.set_Message('Idle')
        
    ### Stop processes, turn off LEDs, stop camera from using power. ###
    def on_cleanup(self):
        self.led.cleanup()
        self.camera.cleanup()
        pygame.quit()
        if(debug == True):
            print("Pygame cleaned up")
        GPIO.cleanup()
        if(debug == True):
            print("GPIO cleaned up")
            
            
    ### Actions to take when button is pressed. ###
    def buttonPress(self):
        if(debug == True):
            print("Button press registered")
        
        # Remove event detection from arcade button to clear potential bounce
        GPIO.remove_event_detect(15)
        
        self.set_Message('Pressed')
        # Runs camera method to take photo series, returns absolute filenames in list structure
        self.photos = self.camera.pointShoot(self.led)
        # Passes photos list to draw_Surface method to display on UI
        self.draw_Surface(photographs=self.photos)
        # Users are going to want to look at photos for longer than a few ms
        sleep(10)

        # Restore event detection once function is complete
        GPIO.add_event_detect(15, GPIO.RISING, bouncetime=5)
            
    ### Manipulates which message to be displayed to pass to draw_Surface method. Manipulates _idle variable. ###
    def set_Message(self, state):
        # If _idle is set to True, will not run on_render
        if(state == 'Idle'):
            message = 'Please press button to begin countdown'
            self._idle = True
        elif(state == 'Pressed'):
            message = 'Please wait...'
            self._idle = False
        elif(state == 'Blank'):
            message = None
            self._idle = False
        else:
            message = 'Something went wrong setting message'
        
        # Pass message to draw_Surface to display new message
        self.draw_Surface(message)
            
    ### This method is for drawing the display ###
    # Parameters:
    # message (str) :: Message to draw and show to users.
    # photographs (list) :: List of filenames to pull and draw onto the display from buttonPress method.
    def draw_Surface(self, message=None, photographs=None):
        # Start by blitting the background onto the surface
        self._display_surf.blit(pygame.image.load("backdrop.jpeg"), (0,0))
        
        # Set Message on surface
        if message is not None:
            # Create new surface to dispaly message, antialias True, background color(150, 90, 255)
            self.textsurface = self.myfont.render(message, True, (150, 90, 255))
            # Center text rectangle
            self.text_rect = self.textsurface.get_rect(center=(self.displayInfo.current_w // 2, self.displayInfo.current_h // 2)) 
            # Blit textsurface at position text_rect onto _display_surf
            self._display_surf.blit(self.textsurface, self.text_rect)
            
        # Process and display photos after they are taken
        if photographs is not None:
            # Loop over photographs with counter i
            for i, photo in enumerate(photographs):
                # Iterate through photos in list and place on screen
                self.pic = pygame.transform.smoothscale(pygame.image.load(photo), (self.displayInfo.current_w // 3, self.displayInfo.current_h // 3))
                if i == 0:
                    self.pic_rect = self.pic.get_rect(center=(self.displayInfo.current_w // 4, self.displayInfo.current_h // 4))
                elif i == 1:
                    self.pic_rect = self.pic.get_rect(center=(int(self.displayInfo.current_w * 0.75), self.displayInfo.current_h // 4))
                elif i == 2:
                    self.pic_rect = self.pic.get_rect(center=(self.displayInfo.current_w // 4, int(self.displayInfo.current_h * .75)))
                else:
                    self.pic_rect = self.pic.get_rect(center=(int(self.displayInfo.current_w * 0.75), int(self.displayInfo.current_h * .75)))
                self._display_surf.blit(self.pic, self.pic_rect)
        
        # Finally update display with changes
        pygame.display.flip()
        
    
    ### Run after Photobooth object created. Main loop contained here. ###
    def on_execute(self):
        if(debug == True):
            print("Running on_execute")
        self.on_init()
            #self._running = False
            
        # Main Loop
        if(debug == True):
            print("Starting main loop")
        while(self._running):
            self.on_loop()
            self.on_render()
        self.on_cleanup()



    
if __name__ == "__main__":
    thePhotobooth = Photobooth()
    thePhotobooth.on_execute()