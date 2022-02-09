#!/usr/bin/env python3

# Imports
import RPi.GPIO as GPIO
import time
from datetime import datetime
import math
import sys

# Constants
RADIUS = 0.037 # in meters
SIGNALS_PER_REVOLUTION = 4 # signals received from hardware per one revolution

# Globals
global counter
counter = 0

# Functions
def increase_counter(channel):
    """Incerases number of spins"""
    global counter
    counter += 1

def print_help(program_name):
    """Prints help for the user"""
    print("Wind meter (https://github.com/neloduka-sobe/wind-meter)")
    print("Usage: ")
    print(f"{program_name} <GPIO-pin> <path-to-csv-file> [debug]")
    print("Examples: ")
    print(f"{program_name} 5 /path/to/csvfile")
    print(f"{program_name} 5 /path/to/csvfile debug")
    sys.exit(1)

def print_debug(rpm, speed, date):
    """Prints debug information"""
    print(f"RPM is {rpm}")
    print(f"Speed is equal to {speed} m/s")
    print(f"Date is {date}")

# Getting GPIO pin and /path/to/file from sys.argv()
debug = False
try:
    pin_number = int(sys.argv[1])
    path_to_file = sys.argv[2]
    if len(sys.argv) == 4:
        debug = "debug" == sys.argv[3]

except (IndexError, ValueError):
    print_help(sys.argv[0])

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pin_number, GPIO.FALLING, callback=increase_counter)

# Main loop
try:
    while True:
        # Waiting for data to be collected
        time.sleep(60)

        # Calculating speed of wind, rpm and saving date into variables
        speed = (2 * math.pi * RADIUS * (counter/SIGNALS_PER_REVOLUTION)) / 60
        rpm = counter/SIGNALS_PER_REVOLUTION
        date = datetime.now()

        # Printing debug info
        if debug:
            print_debug(rpm, speed, date)

        # Writing data into the file
        with open(path_to_file, "a") as f:
            f.writelines(f"{date}, {speed}, {rpm}\n")

        counter = 0
except KeyboardInterrupt:
    # Cleaning ports
    GPIO.cleanup()
    sys.exit(0)
