import time
import board
from adafruit_neotrellis.neotrellis import NeoTrellis
import random
# create the i2c object for the trellis
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# create the trellis
trellis = NeoTrellis(i2c_bus)

# Set the brightness value (0 to 1.0)
trellis.brightness = 0.5

# some color definitions
OFF = (0, 0, 0)
CYAN = (0, 255, 255)

# Variable to track button press time
button_press_time = 0

# this will be called when button events are received
def blink(event):
    global button_press_time
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        time.sleep(0.3)
    # turn the LED off after 2 seconds
    elif event.edge == NeoTrellis.EDGE_FALLING or (event.edge == NeoTrellis.EDGE_RISING and time.monotonic() > button_press_time):
        trellis.pixels[event.number] = OFF

for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    trellis.pixels[i] = OFF
    time.sleep(0.05)

while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 milliseconds or so
    time.sleep(0.02)
