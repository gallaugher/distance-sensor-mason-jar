# Distance Sensing Luminaria - note we import math here, too!
# video for the build is available as part of Prof. John Gallaugher's
# CircuitPython School on YouTube: https://bit.ly/circuitpython-tutorials
import board, neopixel, time, adafruit_vl53l1x, math

# Prior video also shows setup code changes for Raspberry Pi Pico & QT Py RP2040
i2c = board.I2C()
distance_sensor = adafruit_vl53l1x.VL53L1X(i2c)
distance_sensor.distance_mode = 1
distance_sensor.timing_budget = 100

distance_sensor.start_ranging()

strip_pin = board.A1 # LED clipped to A1. Change as needed for other boards
strip_num_of_LEDs = 20 # 30 lights on a strip, Change to 20 for strands
strip = neopixel.NeoPixel(strip_pin, strip_num_of_LEDs, brightness=0.5, auto_write=False)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SELECTED_COLOR = RED # Define & use any colors you want

strip.fill(BLACK) # Turn off all lights
strip.write() # REMEMBER to call .write each time you want to write changes to neopixels

MAX_DISTANCE = 150
MIN_DISTANCE = 30
cm_per_light = (MAX_DISTANCE-MIN_DISTANCE)/strip_num_of_LEDs

while True:
    if distance_sensor.data_ready:
        distance = distance_sensor.distance
        print(f"Distance: {distance}")
        if distance == 0: # do nothing if 0 reading, which shows up if nothing is in front of sensor
            continue # this skips the rest of the code & restarts the loop
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
