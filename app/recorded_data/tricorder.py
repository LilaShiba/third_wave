import csv
from datetime import datetime, timedelta
import time
import board
import busio
import adafruit_tsl2591
import adafruit_lsm9ds1
import adafruit_apds9960.apds9960
import adafruit_bme680
from gpiozero import Button
from typing import Tuple

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensors
#sensor_tsl2591 = adafruit_tsl2591.TSL2591(i2c)
sensor_lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
sensor_apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor_bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Enable APDS-9960 sensor
sensor_apds9960.enable_proximity = True
sensor_apds9960.enable_color = True

# Initialize GPIO pin for the flip switch (using GPIO pin 17 as an example)
flip_switch = Button(17)

def read_lsm9ds1() -> Tuple[float, float, float, float, float, float, float, float, float, float]:
    """Reads data from the LSM9DS1 sensor."""
    accel_x, accel_y, accel_z = sensor_lsm9ds1.acceleration
    gyro_x, gyro_y, gyro_z = sensor_lsm9ds1.gyro
    mag_x, mag_y, mag_z = sensor_lsm9ds1.magnetic
    temp = sensor_lsm9ds1.temperature
    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temp

# def read_tsl2591() -> Tuple[float, int, int]:
#     """Reads data from the TSL2591 sensor."""
#     lux = sensor_tsl2591.lux if sensor_tsl2591.lux is not None else 0
#     infrared = sensor_tsl2591.infrared
#     full_spectrum = sensor_tsl2591.full_spectrum
#     return lux, infrared, full_spectrum

def read_apds9960() -> Tuple[int, Tuple[int, int, int, int]]:
    """Reads proximity and color data from the APDS-9960 sensor."""
    proximity = sensor_apds9960.proximity
    color_data = sensor_apds9960.color_data
    return proximity, color_data

def read_bme680() -> Tuple[float, float, float, int]:
    """Reads temperature, gas, humidity, and pressure from the BME680 sensor."""
    temperature = sensor_bme680.temperature
    gas = sensor_bme680.gas
    humidity = sensor_bme680.humidity
    pressure = sensor_bme680.pressure
    return temperature, gas, humidity, pressure

def record_sensor_data(csv_file_path: str, duration_seconds: int, hertz: int = 1) -> None:
    """Records real sensor data to a CSV file."""
    end_time_loop = datetime.now() + timedelta(seconds=duration_seconds)
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Accel_X', 'Accel_Y', 'Accel_Z',
                         'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Mag_X', 'Mag_Y', 'Mag_Z',
                         'LSM9DS1_Temp', 'Proximity',
                         'Color_R', 'Color_G', 'Color_B', 'Color_C', 'BME680_Temp',
                         'Gas', 'Humidity', 'Pressure', 'Switch_Pressed'])

        while datetime.now() < end_time_loop:
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            start_time = datetime.now()
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, lsm9ds1_temp = read_lsm9ds1()
            #ßlux, infrared, full_spectrum = read_tsl2591()
            proximity, (color_r, color_g, color_b, color_c) = read_apds9960()
            bme680_temp, gas, humidity, pressure = read_bme680()
            switch_pressed = 1 if flip_switch.is_pressed else 0

            writer.writerow([timestamp, accel_x, accel_y, accel_z,
                             gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z,
                              lsm9ds1_temp, proximity,
                             color_r, color_g, color_b, color_c, bme680_temp,
                             gas, humidity, pressure, switch_pressed])
            end_time = datetime.now()
            remaining_time = (1/hertz) - (end_time - start_time).total_seconds()
            if remaining_time > 0:
                time.sleep(remaining_time)

if __name__ == "__main__":
    csv_file_path = f'./sensor_data_{datetime.now().strftime("%Y-%m-%dT%H:%M")}.csv'
    duration_seconds = 260  # For example, record data for 4 minutes and 20 seconds
    record_sensor_data(csv_file_path, duration_seconds, 60)  # Adjusted to match the function signature
    print(f'Data recorded to {csv_file_path}')
