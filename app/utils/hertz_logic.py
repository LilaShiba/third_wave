import time
from app.utils.rpi import Sensors

hertz = 50
durentation = 60

hertz = 1 / hertz
frames = time.time() + durentation
sensor = Sensors(sensor_pin=21)

while time.time() < frames:
    sample_start = time.time()
    res = sensor.read_sensor()
    sample_end = time.time()
    remaining_time = hertz - (sample_end - sample_start)

    # If there's remaining time, sleep for that duration
    if remaining_time > 0:
        time.sleep(remaining_time)
    else:
        print("Warning: Processing took longer than the sample interval")
        time.sleep(hertz)
