#!/usr/bin/env python

# import board
# from adafruit_pca9685 import PCA9685

import PCA9685
import time

pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)
pwm.setServoPulse(0,100)

# Define temperature thresholds and corresponding pulse values
temp_pulse_pairs = [(65, 100), (60, 90), (55, 75), (50, 50), (40, 40)]

try:
  while True:
    
    with open("/sys/class/thermal/thermal_zone0/temp") as file:
      temp = float(file.read()) / 1000.00
      temp = float('%.2f' % temp)
    print(f"{ temp = }")
    for threshold, pulse in reversed(temp_pulse_pairs):
        if temp > threshold:
            print(f"{ threshold = }")
            pwm.setServoPulse(0, pulse)
            break
    else:
        pwm.setServoPulse(0, 0)

    sleep_time = 30  # seconds
    time.sleep(sleep_time)
except KeyboardInterrupt:    
  print("Program interrupted by user. Exiting..")
