# Modified slightly from the learning video, but should work well.
# Distance Sensing Luminaria - note we import math here, too!
# video for the build is available as part of Prof. John Gallaugher's
# CircuitPython School on YouTube: https://bit.ly/circuitpython-tutorials
import board, neopixel, time, adafruit_vl53l1x, math

# Prior video also shows setup code changes for Raspberry Pi Pico & QT Py RP2040
i2c = board.I2C()
distance_sensor = adafruit_vl53l1x.VL53L1X(i2c)
distance_sensor.distance_mode = 1

# larger timing_budget increases the maximum distance 
# the device can range and improves the accuracy. 
# Vendor says timing budget can be up to 1000, but short distance
# seems to only allow 200.
# Power consumption will also go up w/higher timing budget. 
# Adafruit had 100 in their example. I set it to 200, below.

distance_sensor.timing_budget = 200 

distance_sensor.start_ranging()

strip_pin = board.A1 # LED clipped to A1. Change as needed for other boards
strip_num_of_LEDs = 30 # 30 lights on a strip, Change to 20 for strands
strip = neopixel.NeoPixel(strip_pin, strip_num_of_LEDs, brightness=0.5, auto_write=False)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SELECTED_COLOR = RED # Define & use any colors you want

strip.fill(BLACK) # Turn off all lights
strip.write() # REMEMBER to call .write each time you want to write changes to neopixels

MAX_DISTANCE = 100 # was 150
MIN_DISTANCE = 10 # was 30
cm_per_light = (MAX_DISTANCE-MIN_DISTANCE)/strip_num_of_LEDs

# BELOW IS SOME SAMPLE CODE FROM ADAFRUIT TO PRINT OUT SENSOR STATUS
print("VL53L1X Simple Test.")
print("--------------------")
model_id, module_type, mask_rev = distance_sensor.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Mask Revision: 0x{:0X}".format(mask_rev))
print("Distance Mode: ", end="")
if distance_sensor.distance_mode == 1:
    print("SHORT")
elif distance_sensor.distance_mode == 2:
    print("LONG")
else:
    print("UNKNOWN")
print("Timing Budget: {}".format(distance_sensor.timing_budget))
print("--------------------")

while True:
    if distance_sensor.data_ready:
        distance = distance_sensor.distance
        print(f"Distance: {distance_sensor.distance} cm")

        if distance == None: # do nothing if 0 reading, which shows up if nothing is in front of sensor
            continue # this skips the rest of the code & restarts the loop
        if distance == 0: # assume it's at max distance
            distance = MAX_DISTANCE
        distance = min(distance, MAX_DISTANCE)
        distance = max(distance, MIN_DISTANCE)

        leds_off = math.ceil((distance-MIN_DISTANCE)/cm_per_light)
        leds_on = strip_num_of_LEDs-leds_off
        print(f"Distance: {distance}, LEDs to turn on: {leds_on}")

        for i in range(strip_num_of_LEDs):
            if i < leds_on:
                strip[i] = SELECTED_COLOR
            else:
                strip[i] = BLACK
        strip.write()
        distance_sensor.clear_interrupt()
        time.sleep(0.05)
