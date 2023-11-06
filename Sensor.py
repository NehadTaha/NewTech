from twilio.rest import Client
import RPi.GPIO as GPIO
import requests
import time
import subprocess

# Set up GPIO
led = 17
pir = 20
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(pir, GPIO.IN)

image_list = []  # To store captured image filenames

# Twilio credentials
account_sid = 'My Account SID'
auth_token = 'My Auth Token'
twilio_phone_number = 'my_twilio_phone_number'
your_phone_number = 'my_phone_number'
server_url='http://192.168.12.21:5000'
motion_detected=False


# Flag to track if notification has been sent
notification_sent = False


def send_sms(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=your_phone_number
    )

def capture_image():
  while GPIO.input(pir):
    timestamp = time.strftime("%Y-%m-%d-%H:%M:%S")
    image_filename = f"motion_{timestamp}.jpg"
    # Use fswebcam to capture an image
    subprocess.call(["fswebcam", "-r","640*480","--no-banner", image_filename])
    print(f"Picture saved as {image_filename}")
    image_list.append(image_filename)
    time.sleep(1)
    
try:
    while True:
        if GPIO.input(pir):
            print("Motion Detected")
            
            # Capture an image when motion is detected
           # capture_image()
            
             # Send an SMS notification if it hasn't been sent yet
           # if not notification_sent:
              #  send_sms("Motion detected on Raspberry Pi!")
               # notification_sent = True

            
                
            response = requests.post(f"{server_url}/motion_detected", json={"motion_detected": GPIO.input(pir)})
            print("request sent")
            if response.status_code == 200:
                print(f"Motion detected status sent to server: {motion_detected}")
            else:
                print(f"Failed to send motion detected status to server")
            
            while GPIO.input(pir):
                time.sleep(0)
        else:
            print("Motion stopped")


except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()








