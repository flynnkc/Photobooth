These scripts have been written so that I can use them as a photo booth for my wedding. I'm running them off of a Raspberry Pi 3b+ with Camera Module v2. For a flash I am using a 24 LED RGBW Adafruit Neopixel Ring. To activate an arcade button will be mounted for the subject to push to begin the picture-capture process. After the pictures are taken they will be stored locally and pushed remotely to an outside service such as Twitter, Google Photos, or a Wordpress site.

This is a work in progress and subject to change frequently. Not all features that I would like to add are present or working. I'm a student so this is just something I've been doing in my free time.

Credit to Irina Iriser for open licence background image.

Environment: Python 3.5.3

Libraries Used:
- Adafruit-Blinka==1.1.0
- adafruit-circuitpython-neopixel==3.3.4
- Adafruit-PlatformDetect==0.0.9
- Adafruit-PureIO==0.2.3
- picamera==1.13
- pygame==1.9.3
- RPi.GPIO==0.6.5
- rpi-ws281x==4.1.0

Hardware Used:
- Raspberry Pi 3 B+
- Raspberry Pi Camera Module v2
- Adafruit NeoPixel Ring 24 RGBW
- 74AHCT125 - Quad Level-Shifter (3V to 5V)
- LED Arcade Button
- 5V 2A Power Supply
- Halfsize breadboard

For Raspberry Pi setup see https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
For wiring see https://learn.adafruit.com/assets/64121
If attempting to test scripts remotely without HDMI connected, onboard RPi audio must be turned off or conflict with rpi_ws281x lib:
    - Create /etc/modprobe.d/snd-blacklist.conf and add "blacklist snd_bcm2835"
    - In /boot/config.txt add:
        hdmi_force_hotplug=1
        hdmi_force_edid_audio=1

Thanks,
KC Flynn
