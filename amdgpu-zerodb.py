#!/usr/bin/python3 -u

# Adds 0dB workaround for AMDGPU (tested on RX580)

import time
import signal
import sys
import os

# Check for root
if os.getuid() is not 0:
    print('ERROR: Root required for access to sysfs.')
    sys.exit()

# Temparature state
MAX_TEMP = 55.0
MIN_TEMP = 45.0
IS_COOLLING_DOWN = False
# Sleep time in seconds
SLEEP_TIME = 1
# Filenodes for sysfs
NODE_PWM = open("/sys/class/drm/card0/device/hwmon/hwmon3/pwm1", "w")
NODE_FANMODE = open("/sys/class/drm/card0/device/hwmon/hwmon3/pwm1_enable",
                    "w")
NODE_TEMP = open("/sys/class/drm/card0/device/hwmon/hwmon3/temp1_input", "r")

# State
CURRENT_MODE = None


# Set automatic handling of fan PWM via AMDGPU
def set_auto(currentTemp=-1):
    global CURRENT_MODE
    if CURRENT_MODE is not 'AUTO':
        print("Switching to AMDGPU fan PWM handling. Current temp: {}".format(
            currentTemp))
        NODE_FANMODE.seek(0)
        NODE_FANMODE.write('2')
        NODE_FANMODE.flush()
        CURRENT_MODE = 'AUTO'


# Disable fans
def set_zero(currentTemp=-1):
    global CURRENT_MODE
    if CURRENT_MODE is not 'ZERO':
        print("Disabling GPU fans for 0dB mode. Current temp: {}".format(
            currentTemp))
        NODE_PWM.seek(0)
        NODE_PWM.write('0')
        NODE_PWM.flush()
        CURRENT_MODE = 'ZERO'


# Get current temp
def get_temp():
    NODE_TEMP.seek(0)
    temp = float(NODE_TEMP.read().rstrip()) / 1000
    return temp


# Set correct operation mode based on temp
def select_mode():
    global IS_COOLLING_DOWN
    currentTemp = get_temp()
    EFFECTIVE_MAX_TEMP = MAX_TEMP
    if IS_COOLLING_DOWN:
        EFFECTIVE_MAX_TEMP = MIN_TEMP
    if currentTemp >= EFFECTIVE_MAX_TEMP:
        IS_COOLLING_DOWN = True
        set_auto(currentTemp)
    else:
        IS_COOLLING_DOWN = False
        set_zero(currentTemp)


# Handle exiting
def exit_handler():
    print("Received exit command. Switching to auto mode.")
    set_auto()
    sys.exit()


# Setup
signal.signal(signal.SIGTERM, exit_handler)
try:
    print("Monitoring GPU temp for 0dB mode.")
    while True:
        select_mode()
        time.sleep(SLEEP_TIME)
finally:
    exit_handler()
