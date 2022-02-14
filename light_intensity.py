#!/usr/bin/env python3

# Imports
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import sys

# Globals
global pin_a, pin_b

# Setup
GPIO.setmode(GPIO.BCM)

# Functions
def print_help(program_name):
    """Prints help for the user"""
    print("Light intensity (https://github.com/neloduka-sobe/weather-station)")
    print("Usage: ")
    print(f"{program_name} <GPIO-pin-a> <GPIO-pin-b> <path-to-csv-file> [debug]")
    print("Examles: ")
    print(f"{program_name} 5  6 /path/to/csvfile")
    print(f"{program_name} 5  6 /path/to/csvfile debug")
    sys.exit(1)

def print_debug(time, percentage):
    """Prints debug information"""
    print(f"Time is {time}")
    print(f"Percentage is {percentage}%")

def discharge():
        """Function responsible for discharging capacitor"""
        GPIO.setup(pin_a, GPIO.IN)
        GPIO.setup(pin_b, GPIO.OUT)
        GPIO.output(pin_b, False)
        sleep(0.004) # wait for capacitor to discharge

def measure_charge_time():
    """Recharges capacitor and returns time of recharging"""
    GPIO.setup(pin_b, GPIO.IN)
    GPIO.setup(pin_a, GPIO.OUT)
    counter = 0
    GPIO.output(pin_a, True)
    while not GPIO.input(pin_b):
        counter += 1
    return counter


def read_data():
    """Reads data from sensor"""
    discharge()
    return measure_charge_time()

def calculate_percentage(time):
    """Calculates light intensity in %"""
    result = (10000-time)/(100)
    if result < 0:
        return 0
    return result

# Main function execution
if __name__ == "__main__":

    # Getting GPIO pins and /path/to/file from sys.argv[]
    debug = False
    try:
        pin_a = int(sys.argv[1])
        pin_b = int(sys.argv[2])
        path_to_file = sys.argv[3]
        if len(sys.argv) == 5:
            debug = "debug" == sys.argv[4]

    except (IndexError, ValueError):
        print_help(sys.argv[0])

    try:
        last = -1
        while True:
            # saves data from sensor to the variable
            time = read_data()
            percentage = calculate_percentage(time)
            date = datetime.now()

            # printing debug info
            if debug:
                print_debug(time, percentage)

            # if following percentage results differ write it into the file
            if last != int(percentage):
                with open(path_to_file, "a") as f:
                    f.writelines(f"{date}, {int(percentage)}\n")
            last = int(percentage)
            sleep(60)

    except KeyboardInterrupt:
        # Cleaning ports
        GPIO.cleanup()
        sys.exit(0)
