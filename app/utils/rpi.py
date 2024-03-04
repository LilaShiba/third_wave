import logging
import numpy as np
import csv
from datetime import datetime
import time
from typing import Dict, Any
import requests

import board
import busio
from adafruit_lsm9ds1 import LSM9DS1_I2C
from adafruit_tsl2591 import TSL2591

# Uncomment if using GPIO functionality
# import RPi.GPIO as GPIO


class Sensors:
    def __init__(self, sensor_pin: int) -> None:
        self.sensor_pin: int = sensor_pin
        self.url: str = f"http://127.0.0.1:5000/sensors?sensor_id={sensor_pin}&frames=100"

        # Initialize I2C bus
        i2c: busio.I2C = busio.I2C(board.SCL, board.SDA)

        # Initialize sensors
        self.movement_sensors: LSM9DS1_I2C = LSM9DS1_I2C(i2c)
        #self.light_sensor: TSL2591 = TSL2591(i2c)

    def read_i2c_sensor(self) -> Dict[str, Any]:
        """Read I2C sensors on RPi's bus (SCL, SDA)"""
        sensor_data: Dict[str, Any] = {
            "acceleration": list(self.movement_sensors.acceleration),
            "magnetic": list(self.movement_sensors.magnetic),
            "gyro": list(self.movement_sensors.gyro),
            # "light_sensor": {
            #     "lux": self.light_sensor.lux,
            #     "infrared": self.light_sensor.infrared,
            #     "visible": self.light_sensor.visible
            # }
        }
        return sensor_data

    def read_sensor(self) -> Dict[str, float]:
        """Simulate reading sensor data"""
        simulated_data: Dict[str, float] = {'value': np.random.random()}
        logging.debug(f"Simulated sensor data: {simulated_data}")
        return simulated_data

    def manual_run_sensor(self, time_stop: int, hertz: float = 1.0) -> None:
        """Runs sensor for X frames once per second"""
        logging.info(f"Starting sensor data collection for {time_stop} seconds at {hertz} hertzs.")
        try:
            with open('manual_sensor_data.csv', mode='w', newline='') as file:
                first_res: Dict[str, Any] = self.read_i2c_sensor()
                fieldnames: list = ['timestamp', 'id', 'hertz'] + list(first_res.keys())
                writer: csv.DictWriter = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                hertz_interval: float = 1 / hertz
                frames: float = time.time() + time_stop
                while time.time() < frames:
                    sample_start: float = time.time()
                    res: Dict[str, Any] = self.read_i2c_sensor()
                    res['timestamp'] = datetime.now().isoformat()
                    res['id'] = self.sensor_pin
                    res['hertz'] = hertz
                    writer.writerow(res)

                    sample_end: float = time.time()
                    processing_time: float = sample_end - sample_start
                    remaining_time: float = hertz_interval - processing_time

                    if remaining_time > 0:
                        time.sleep(remaining_time)
                    else:
                        print("Warning: Processing took longer than the sample interval")
                        time.sleep(hertz_interval)
            logging.info("Manual Sensor data collection complete.")
        except Exception as e:
            logging.error(f"Failed to write to CSV: {e}")


def make_api_call(sensor_pin: int, time_stop: int, hertz: int) -> None:
    """Makes a GET request to the Flask API endpoint"""
    url: str = f"http://127.0.0.1:5000/sensors?sensor_id={sensor_pin}&time_stop={time_stop}&hertz={hertz}"
    response: requests.Response = requests.get(url)
    if response.status_code == 200:
        data: Dict[str, Any] = response.json()
        print(data)
    else:
        print("Failed to retrieve data", response.status_code)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sensor_pin: int = 17  # Specify the GPIO pin number
    sensor: Sensors = Sensors(sensor_pin=sensor_pin)
    sensor.manual_run_sensor(time_stop=30, hertz=150)

    # Example API call
    make_api_call(sensor_pin=sensor_pin, time_stop=30, hertz=150)
