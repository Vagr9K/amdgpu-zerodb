#!/usr/bin/python3 -u

# Adds 0dB workaround for AMDGPU (tested on RX580)

import time
import signal
import sys
import os
import configparser

# Check for root
if os.getuid() is not 0:
    print('ERROR: Root required for access to sysfs.')
    sys.exit(-1)

# Temparature state
MAX_TEMP = 55.0
MIN_TEMP = 45.0
IS_COOLLING_DOWN = False
FORCE_DPM = 'auto'
# Sleep time in seconds
REFRESH_DELAY = 1
# Filenodes for sysfs
NODE_PWM = None
NODE_FANMODE = None
NODE_TEMP = None
NODE_DPM = None

# State
CURRENT_MODE = None


# Init sysfs filenodes
def init_sysfs():
    global NODE_FANMODE
    global NODE_PWM
    global NODE_TEMP
    global NODE_DPM
    print('Initializing sysfs nodes.')
    while True:
        try:
            hwmonPath = 'hwmon3'
            if not os.path.isdir(
                    '/sys/class/drm/card0/device/hwmon/{}'.format(hwmonPath)):
                hwmonPath = 'hwmon2'
                print('Switching to Hwmon2.')
            NODE_PWM = open(
                "/sys/class/drm/card0/device/hwmon/{}/pwm1".format(hwmonPath),
                "w")
            NODE_FANMODE = open(
                "/sys/class/drm/card0/device/hwmon/{}/pwm1_enable".format(
                    hwmonPath), "w")
            NODE_TEMP = open(
                "/sys/class/drm/card0/device/hwmon/{}/temp1_input".format(
                    hwmonPath), "r")
            NODE_DPM = open(
                '/sys/class/drm/card0/device/power_dpm_force_performance_level',
                "w")
        except Exception as e:
            print(
                "Failed to initialize sysfs file nodes. Retrying in 1 second.")
            print(e)
            time.sleep(1)
            continue
        break


# Check for configuration
def check_config():
    global MAX_TEMP
    global MIN_TEMP
    global REFRESH_DELAY
    global FORCE_DPM
    config = configparser.ConfigParser()
    try:
        config.read('/etc/amdgpu-zerodb.conf')
        MAX_TEMP = float(config['TEMPERATURES']['MAX_TEMP'])
        MIN_TEMP = float(config['TEMPERATURES']['MIN_TEMP'])
        REFRESH_DELAY = float(config['MAIN']['REFRESH_DELAY'])
        FORCE_DPM = config['GPU']['FORCE_DPM']
    except Exception as e:
        print('Failed to apply amdgpu-zerodb.conf.')
        print(e)
    finally:
        if MAX_TEMP > 55:
            originalSetting = MAX_TEMP
            MAX_TEMP = 55
            print(
                'MAX_TEMP is higher than 55 C (originally set to {}). Limiting to prevent hardware damage.'
                .format(originalSetting))
        if MIN_TEMP > 55:
            originalSetting = MIN_TEMP
            MIN_TEMP = 55
            print(
                'MIN_TEMP is higher than 55 C (originally set to {}). Limiting to prevent hardware damage.'
                .format(originalSetting))
        if REFRESH_DELAY > 10:
            originalSetting = REFRESH_DELAY
            REFRESH_DELAY = 10
            print(
                'REFRESH_DELAY is higher than 10 seconds (originally set to {}). Limiting to prevent hardware damage.'
                .format(originalSetting))
        print(
            'Final configuration is: MAX_TEMP: {}, MIN_TEMP: {}, REFRESH_DELAY: {}, FORCE_DPM: {}.'
            .format(MAX_TEMP, MIN_TEMP, REFRESH_DELAY, FORCE_DPM))


# Set DPM
def set_dpm():
    if FORCE_DPM is not 'auto':
        print('Setting DPM mode to {}.'.format(FORCE_DPM))
        NODE_DPM.seek(0)
        NODE_DPM.write(FORCE_DPM)
        NODE_DPM.flush()


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
        NODE_FANMODE.seek(0)
        NODE_FANMODE.write('1')
        NODE_FANMODE.flush()
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
check_config()

try:
    init_sysfs()
    set_dpm()
    print("Monitoring GPU temp for 0dB mode.")
    while True:
        select_mode()
        time.sleep(REFRESH_DELAY)
except Exception as e:
    print('ERROR: {}'.format(e))
    print(
        'An error occurred. Attempting to switch AMDGPU fan control to AUTO.')
finally:
    exit_handler()
