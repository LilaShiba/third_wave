import csv
from datetime import datetime, timedelta
import time
import board
import busio
import adafruit_lsm9ds1
import adafruit_apds9960.apds9960
import adafruit_bme680
import adafruit_gps
from gpiozero import Button
from typing import Tuple
from adafruit_neotrellis.neotrellis import NeoTrellis
import random

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize a bunch of sensors
sensor_lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
sensor_apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor_bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Enable APDS-9960 sensor features
sensor_apds9960.enable_proximity = True
sensor_apds9960.enable_color = True

# Initialize GPS module with I2C
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)

# Initialize pin for flip switch (17)
flip_switch = Button(17)

# Create the NeoTrellis object
trellis = NeoTrellis(i2c)

# Set the brightness value (0 to 1.0)
trellis.brightness = 0.8
OFF = (0, 0, 0)

# Global variable to track button press time
button_press_time = 0
any_key_pressed = False


def read_lsm9ds1() -> Tuple[float, float, float, float, float, float, float, float, float, float]:
    """Reads data from the LSM9DS1 sensor."""
    accel_x, accel_y, accel_z = sensor_lsm9ds1.acceleration
    gyro_x, gyro_y, gyro_z = sensor_lsm9ds1.gyro
    mag_x, mag_y, mag_z = sensor_lsm9ds1.magnetic 
    temp = sensor_lsm9ds1.temperature
    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temp


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


def read_gps() -> Tuple[float, float, float, str]:
    """Reads data from the GPS module."""
    gps.update()
    latitude = gps.latitude
    longitude = gps.longitude
    speed = gps.speed_knots
    timestamp = gps.timestamp_utc
    timestamp_str = f"{timestamp.tm_hour}:{timestamp.tm_min}:{timestamp.tm_sec}" if timestamp else "N/A"
    return latitude, longitude, speed, timestamp_str

def init_trellis():
        # Initialize NeoTrellis buttons
    for i in range(16):
        trellis.activate_key(i, NeoTrellis.EDGE_RISING)
        trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
        trellis.callbacks[i] = blink
        trellis.pixels[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def env_check(humidity, pressure):
    if humidity > 40:
        trellis.pixels[0] = (random.randint(150, 255), 0,0)
    else:
        trellis.pixels[0] = (0, random.randint(150, 255),0)
            
    if pressure > 1400:
        trellis.pixels[1] = (random.randint(150, 255), 0,0)
    else:
        trellis.pixels[1] = (0, random.randint(150, 255),0)


def blink(event):
    """Handles button press events."""
    global button_press_time, any_key_pressed
    # Turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        trellis.brightness = random.uniform(0.5, 1)
        # Update button press time
        button_press_time = time.monotonic()
        # Update any_key_pressed
        any_key_pressed = event.number
    # Turn the LED off after 2 seconds
    elif event.edge == NeoTrellis.EDGE_FALLING or (event.edge == NeoTrellis.EDGE_RISING and time.monotonic() > button_press_time):
        trellis.pixels[event.number] = OFF
        any_key_pressed = -1

def record_sensor_data(csv_file_path: str, duration_seconds: int, hertz: int = 1) -> None:
    """Records real sensor data to a CSV file, including GPS data."""
    init_trellis()

    # Set end time
    end_time_loop = datetime.now() + timedelta(seconds=duration_seconds)

    # Open CSV file for writing
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Accel_X', 'Accel_Y', 'Accel_Z',
                         'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Mag_X', 'Mag_Y', 'Mag_Z',
                         'LSM9DS1_Temp', 'Proximity',
                         'Color_R', 'Color_G', 'Color_B', 'Color_C', 'BME680_Temp',
                         'Gas', 'Humidity', 'Pressure', 'Switch_Pressed',
                         'GPS_Latitude', 'GPS_Longitude', 'GPS_Speed', 'GPS_Timestamp', 'Pad_press'])

        # Record sensor data until end time is reached
        while datetime.now() < end_time_loop:
            # Get current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            # Read sensor data
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, lsm9ds1_temp = read_lsm9ds1()
            proximity, (color_r, color_g, color_b, color_c) = read_apds9960()
            bme680_temp, gas, humidity, pressure = read_bme680()
            latitude, longitude, speed, gps_timestamp = read_gps()
            switch_pressed = 1 if flip_switch.is_pressed else 0

            # Read button press
            trellis.sync()


            # Write data to CSV
            writer.writerow([timestamp, accel_x, accel_y, accel_z,
                             gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z,
                             lsm9ds1_temp, proximity,
                             color_r, color_g, color_b, color_c, bme680_temp,
                             gas, humidity, pressure, switch_pressed,
                             latitude, longitude, speed, gps_timestamp, any_key_pressed])

            # ENV triggers
            env_check(humidity, pressure)

            # Calculate remaining time and sleep
        
            end_time = datetime.now()
            remaining_time = (1 / hertz) - (end_time - datetime.now()).total_seconds()
            if remaining_time > 0:
                time.sleep(remaining_time)
                        
            # if random.random() < 0.1:
            #         for i in range(16):
            #             trellis.activate_key(i, NeoTrellis.EDGE_RISING)
            #             trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
            #             trellis.callbacks[i] = blink
            #             trellis.pixels[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


                





if __name__ == "__main__":
    # Define CSV file path and duration
    csv_file_path = f'./sensor_data_{datetime.now().strftime("%Y-%m-%dT%H:%M")}.csv'
    duration_seconds = 11260  # Example duration: 4 hours and 20 minutes

    # Record sensor data
    record_sensor_data(csv_file_path, duration_seconds, 60)  # Example frequency
    print(f'Data recorded to {csv_file_path}')
