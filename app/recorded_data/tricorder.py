import csv
import time
from datetime import datetime, timedelta
import board
import busio
# Import for TSL2591 light sensor
import adafruit_tsl2591
# Hypothetical imports for other sensors - adjust these according to your actual sensors
import adafruit_lsm9ds1  # Assuming LSM9DS1 for Accel, Gyro, Mag

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensors
sensor_tsl2591 = adafruit_tsl2591.TSL2591(i2c)
sensor_lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)


def record_sensor_data(csv_file_path, duration_seconds):
    """Records real sensor data to a CSV file."""
    end_time = datetime.now() + timedelta(seconds=duration_seconds)
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Accel_X', 'Accel_Y', 'Accel_Z',
                         'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Mag_X', 'Mag_Y', 'Mag_Z',
                         'Lux', 'IR', 'Full_Spectrum', 'Gain', 'Temp'])

        while datetime.now() < end_time:
            # Read data from LSM9DS1 (Accel, Gyro, Mag)
            accel_x, accel_y, accel_z = sensor_lsm9ds1.acceleration
            gyro_x, gyro_y, gyro_z = sensor_lsm9ds1.gyro
            mag_x, mag_y, mag_z = sensor_lsm9ds1.magnetic
            temp = sensor_lsm9ds1.temperature

            # Read data from TSL2591 (Lux, IR, Full Spectrum)
            lux = sensor_tsl2591.lux if sensor_tsl2591.lux is not None else 0
            infrared = sensor_tsl2591.infrared
            full_spectrum = sensor_tsl2591.full_spectrum
            gain = sensor_lsm9ds1.gain

            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            writer.writerow([timestamp, accel_x, accel_y, accel_z,
                             gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z,
                             lux, infrared, full_spectrum, gain, temp])

            time.sleep(1)


if __name__ == "__main__":
    csv_file_path = './sensor_data_' + \
        datetime.now().strftime('%Y-%m-%dT%H:%M') + '.csv'
    duration_seconds = 120  # For example, record data for 2 minutes
    record_sensor_data(csv_file_path, duration_seconds)
    print(f'Data recorded to {csv_file_path}')
