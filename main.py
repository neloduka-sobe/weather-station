#!/usr/bin/env python3

# Imports
import RPi.GPIO as GPIO
import time
from datetime import datetime
import math

# Constants
PIN_NUMBER = 23
RADIOUS = 0.04 # in meters
SIGNALS_PER_REVOLUTION = 4 # signals received from hardware per one revolution

# Globals
global counter
counter = 0

# Functions
def increase_counter(channel):
    """Incerases number of spins"""
    global counter
    counter += 1

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(PIN_NUMBER, GPIO.FALLING, callback=increase_counter)

# Main loop
try:
    while True:
        time.sleep(60)
        print(f"RPM is {counter/SIGNALS_PER_REVOLUTION}")
        # calculating speed of wind
        speed = (2 * math.pi * RADIOUS * (counter/SIGNALS_PER_REVOLUTION)) / 60
        print(f"Speed is equal to {speed} m/s")
        print("Writing data into wind_speed.csv")
        with open("wind_speed.csv", "a") as f:
            f.writelines(f"{datetime.now()}, {speed}, {counter/SIGNALS_PER_REVOLUTION}\n")
        counter = 0
except:
    # Cleaning ports
    GPIO.cleanup()
