import RPi.GPIO as GPIO
import time
led=17
pir=23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(pir,GPIO.IN)

currentState=0
try:
    while True:
        if GPIO.input(pir):
          GPIO.output(led,GPIO.LOW)
          
          print ("Motion Detected")
          while GPIO.input(pir):
              time.sleep(0)
        else:
          GPIO.output(led,GPIO.HIGH)
          print("Motion stopped")
        
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
