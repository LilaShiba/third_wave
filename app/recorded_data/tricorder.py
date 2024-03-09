import csv
from datetime import datetime, timedelta
import time
import board
import busio
import adafruit_tsl2591
import adafruit_lsm9ds1
import adafruit_dht
from gpiozero import Button
from typing import Tuple

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensors
sensor_tsl2591 = adafruit_tsl2591.TSL2591(i2c)
sensor_lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
#sensor_dht11 = adafruit_dht.DHT11(board.D16)

# Initialize GPIO pin for the flip switch (using GPIO pin 17 as an example)
flip_switch = Button(4)

def read_lsm9ds1() -> Tuple[float, float, float, float, float, float, float]:
    """Reads data from the LSM9DS1 sensor."""
    accel_x, accel_y, accel_z = sensor_lsm9ds1.acceleration
    gyro_x, gyro_y, gyro_z = sensor_lsm9ds1.gyro
    mag_x, mag_y, mag_z = sensor_lsm9ds1.magnetic
    temp = sensor_lsm9ds1.temperature
    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temp

def read_tsl2591() -> Tuple[float, int, int]:
    """Reads data from the TSL2591 sensor."""
    lux = sensor_tsl2591.lux if sensor_tsl2591.lux is not None else 0
    infrared = sensor_tsl2591.infrared
    full_spectrum = sensor_tsl2591.full_spectrum
    return lux, infrared, full_spectrum

def record_sensor_data(csv_file_path: str, duration_seconds: int) -> None:
    """Records real sensor data to a CSV file."""
    end_time = datetime.now() + timedelta(seconds=duration_seconds)
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Accel_X', 'Accel_Y', 'Accel_Z',
                         'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Mag_X', 'Mag_Y', 'Mag_Z',
                         'Lux', 'IR', 'Full_Spectrum', 'Temp', 'Switch_Pressed'])

        while datetime.now() < end_time:
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temp = read_lsm9ds1()
            lux, infrared, full_spectrum = read_tsl2591()
            #humidity = sensor_dht11.humidity
            switch_pressed = 1 if flip_switch.is_pressed else 0

            writer.writerow([timestamp, accel_x, accel_y, accel_z,
                             gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z,
                             lux, infrared, full_spectrum, temp, switch_pressed])

            time.sleep(1)  # Adjust based on your needs

if __name__ == "__main__":
    csv_file_path = f'./sensor_data_{datetime.now().strftime("%Y-%m-%dT%H:%M")}.csv'
    duration_seconds = 260  # For example, record data for 4 minutes and 20 seconds
    record_sensor_data(csv_file_path, duration_seconds)
    print(f'Data recorded to {csv_file_path}')
