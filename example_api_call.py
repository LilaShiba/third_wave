import logging
from app.utils.rpi import Sensors

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sensor_pin = 1  # Example sensor pin
    frames = 100  # Example frame count

    sensor = Sensors(sensor_pin=sensor_pin)
    sensor.run_sensor(frames=frames)
