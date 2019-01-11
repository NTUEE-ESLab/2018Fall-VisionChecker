import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
   inputValue = GPIO.input(18)
   if inputValue == False:
      print("Button pressed")
      while inputValue == False:
         time.sleep(0.3)
