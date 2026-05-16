#!/usr/bin/env python3
import sys, time, signal
import RPi.GPIO as GPIO

PIN = 27  # GPIO27
SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 30

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)

def cleanup(*_):
    GPIO.output(PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

try:
    GPIO.output(PIN, GPIO.HIGH)   # szivattyú BE
    time.sleep(SECONDS)           # működés ideje
finally:
    cleanup()                     # KI

