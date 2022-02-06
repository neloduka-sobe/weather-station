#!/usr/bin/env python3

# Imports
import RPi.GPIO as GPIO
import time
from datetime import datetime
import math

# Constants
PIN_NUMBER = 5
RADIOUS = 0.05 # in meters

# Globals
global counter
counter = 0

# Functions
def increase_counter():
    """Incerases number of spins"""
    global counter
    counter += 1

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NUMBER, GPIO.IN)
GPIO.add_event_detect(PIN_NUMBER, GPIO.RISING, callback=increase_counter)

# Main loop
while True:
    time.sleep(60)
    print(f"RPM is {counter}")
    # calculating speed of wind
    speed = (2 * math.pi * RADIOUS * counter) / 60
    print(f"Speed is equal to {speed} m/s")
    print("Writing data into wind_speed.csv")
    with open("wind_speed.csv", "a") as f:
        f.writelines(f"{datetime.now()}, {speed}, {counter}\n")
    counter = 0

# Cleaning ports
GPIO.cleanup()
