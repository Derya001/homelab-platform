import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)  # LOW = kikapcs
time.sleep(1)
GPIO.output(17, GPIO.HIGH)  # bekapcs
time.sleep(5)
GPIO.output(17, GPIO.LOW)   # kikapcs
GPIO.cleanup()

