####################################################################
# Preview scripts                                                  #
#This script will provide methods to generate previews and snap    #
# photos including screen overlays                                 #
####################################################################

from picamera import PiCamera
from datetime import datetime
from time import sleep
import traceback
import os

debug = True



class Camera(PiCamera):
    

    ### Camera.takePhoto is called by Camera.pointShoot to capture and name image files/folder. Returns image filename. ###
    # Parameters:
    # res1 (int) :: Width of image capture (Does not affect preview resolution) :: max 2592
    # res2 (int) :: Height of image capture (Does not affect preview resolution) :: max 1944
    # currentTime (str) :: capture of current time using datetime library :: default %m_%d_%Y_%H_%M_%S
    # i (int) :: Iteration of photo since datetime is only taken once when run in for loop :: default 0
    # folder (str) :: Folder where pictures will be saved
    # saveAs (str) :: Complete filepath and filename of image

    def takePhoto(self, res1, res2, i = 0, currentTime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S-")):
        try:
            # Parse folder info and image filename
            folder = os.path.dirname(os.getcwd()) + "/photos"
            saveAs = folder + "/" + currentTime + str(i) + ".jpg"
            self.resolution = (res1, res2)
            
            #Make photos folder if does not exist
            if(not os.path.isdir(folder)):
                try:
                    os.mkdir(folder)
                except:
                    if(debug == True):
                        print("Folder does not exist and could not be created")
                
            #Capture image
            self.capture(saveAs)
            if(debug == True):
                print("Image saved to " + saveAs)
            return saveAs
        
        except:
            if(debug == True):
                print("Error in takePhoto method")
                traceback.print_exc()
            


    ### Point and Shoot method to create countdown overlay then call Camera.takePhoto three times to capture images. Returns list of filenames. ###
    # Parameters:
    # led (LED) :: LED object created in Photobooth script
    # imgW (int) :: Width of image in pixels :: Default 1920
    # imgH (int) :: Height of image in pixels :: Default 1080
            
    def pointShoot(self, led, imgW = 1920, imgH = 1080):
        try:
            filenames = [] # List to store image filenames
            if(debug == True):
                print("Begin pointShoot")
            #Turn off led lights since LED.colorWheel most likely running up to this point
            led.flash_off()
            
            #loop to take a series of 3 pictures
            for x in range(1,4):
                #Paste preview display on top of UI
                self.start_preview()
                self.annotate_text_size = 160 #max value 160 default 32
                
                #Count down from 5 and take photo
                for y in range(5, 0, -1):
                    if(y > 3):
                        self.annotate_text = str(y)
                        sleep(1)
                    elif(y == 3):
                        led.flash_on()
                        self.annotate_text = str(y)
                        sleep(1)
                    elif(y == 2):
                        self.annotate_text = "Ready!"
                        sleep(1)
                    else:
                        self.annotate_text = "Set!"
                        sleep(1)
                self.annotate_text = "Smile!"
                sleep(0.5)
                self.annotate_text = ""
                
                if(debug == True):
                    print("Taking photo " + str(x) + "/3")
                    #Call Camera.takePhoto to capture image and return filename, then add filename to filenames list
                filenames.append(self.takePhoto(imgW, imgH, i = x))
                led.flash_off()
            #Finally return filenames list for display
            return filenames
        
        except:
            if(debug == True):
                print("An error occured in preview method")
                traceback.print_exc()
            
        finally:
            self.stop_preview()
            
    # Call Camera.close to free memory on cleanup
    def cleanup(self):
        self.close()
        if(debug == True):
            print("Camera cleaned up")
