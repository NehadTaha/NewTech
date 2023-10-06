from twilio.rest import Client
import RPi.GPIO as GPIO
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
account_sid = 'ACc227270a36945835122743f400429062'
auth_token = '03a729d8919882f0eebe5d6febde717b'
twilio_phone_number = '+12565884577'
your_phone_number = '+18193498430'

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
            GPIO.output(led, GPIO.LOW)
            print("Motion Detected")
            
            # Capture an image when motion is detected
            capture_image()
             # Send an SMS notification if it hasn't been sent yet
            if not notification_sent:
                send_sms("Motion detected on Raspberry Pi!")
                notification_sent = True
            
            while GPIO.input(pir):
                time.sleep(0)
        else:
            GPIO.output(led, GPIO.HIGH)
            print("Motion stopped")

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()








