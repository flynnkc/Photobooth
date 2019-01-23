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

#Method to take picture
#Parameters:
#camera (PiCamera) :: Camera object
#res1 (int) :: Width of image capture (Does not affect preview resolution) :: max 2592
#res2 (int) :: Height of image capture (Does not affect preview resolution) :: max 1944
#currentTime (str) :: capture of current time using datetime library :: default %m_%d_%Y_%H_%M_%S
#i (int) :: Iteration of photo since datetime is only taken once when run in for loop :: default 0
#folder (str) :: Folder where pictures will be saved
#saveAs (str) :: Complete filepath and filename of image

def takePhoto(camera, res1, res2, i = 0, currentTime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S-")):
    try:
        folder = os.path.dirname(os.getcwd()) + "/photos"
        saveAs = folder + "/" + currentTime + str(i) + ".jpg"
        camera.resolution = (res1, res2)
        sleep(0.1)
        
        #Make photos folder if does not exist
        if(not os.path.isdir(folder)):
            try:
                os.mkdir(folder)
            except:
                if(debug == True):
                    print("Folder does not exist and could not be created")
            
        #Capture image
        camera.capture(saveAs)
        if(debug == True):
            print("Image saved to " + saveAs)
    
    except:
        if(debug == True):
            print("Error in takePhoto method")
            traceback.print_exc()
        

#Point and Shoot method to create countdown overlay then take picture 3 times
#imgW (int) :: Width of image in pixels :: Default 1920
#imgH (int) :: Height of image in pixels :: Default 1080
        
def pointShoot(led, imgW = 1920, imgH = 1080):
    try:
        if(debug == True):
            print("Begin pointShoot")
        camera = PiCamera()
        led.flash_off()
        
        #loop to take a series of 3 pictures
        for x in range(1,4):
            camera.resolution = (1920, 1080)
            camera.start_preview(fullscreen=False, window=(100, 100, 1720, 880))
            camera.annotate_text_size = 160 #max value 160 default 32
            
            #Count down from 5 and take photo
            for y in range(5, 0, -1):
                if(y > 3):
                    camera.annotate_text = str(y)
                    sleep(1)
                elif(y == 3):
                    led.flash_on()
                    camera.annotate_text = str(y)
                    sleep(1)
                elif(y == 2):
                    camera.annotate_text = "Ready!"
                    sleep(1)
                else:
                    camera.annotate_text = "Set!"
                    sleep(1)
            camera.annotate_text = "Smile!"
            sleep(0.5)
            camera.annotate_text_size = 100
            camera.annotate_text = ""
            
            if(debug == True):
                print("Taking photo " + str(x) + "/3")
            takePhoto(camera, imgW, imgH, i = x)
            led.flash_off()
            camera.resolution = (1920, 1080)
    
    except:
        if(debug == True):
            print("An error occured in preview method")
            traceback.print_exc()
        
    finally:
        camera.stop_preview()
        camera.close()
        if(debug == True):
            print("Camera closed")
    