import csv
from datetime import datetime, timedelta

# Function to generate dummy sensor data
def generate_sensor_data(start_time, duration_seconds):
    time_stamp = start_time
    time_delta = timedelta(seconds=1)
    data = []

    for _ in range(duration_seconds):
        # Generate dummy data: adjust these values as needed for your simulation
        accel_x = round(0.01 + 0.01 * (_ % 2), 2)  # Alternating slight variation
        accel_y = round(-0.02 + 0.01 * (_ % 3), 2)  # Alternating slight variation
        accel_z = 9.81  # Assuming constant gravity with slight variations
        gyro_x = round(0.5 - 0.1 * (_ % 2), 2)  # Alternating slight variation
        gyro_y = round(-0.1 + 0.1 * (_ % 4), 2)  # Alternating slight variation
        gyro_z = round(0.2 - 0.1 * (_ % 5), 2)  # Alternating slight variation
        mag_x = 30 + (_ % 3)  # Simulating minor fluctuations
        mag_y = -60 + (_ % 4)  # Simulating minor fluctuations
        mag_z = 50 - (_ % 5)  # Simulating minor fluctuations

        data.append([time_stamp.strftime('%Y-%m-%dT%H:%M:%S'), accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z])
        time_stamp += time_delta

    return data

# Start time of the data
start_time = datetime(2024, 2, 17, 12, 0, 0)
# Duration in seconds (2 minutes)
duration_seconds = 120

# Generate the data
sensor_data = generate_sensor_data(start_time, duration_seconds)


if __name__ == "__main__":
# Write the data to a CSV file
    csv_file_path = './dummy_data_scripts/acc_mag.csv'
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Accel_X', 'Accel_Y', 'Accel_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Mag_X', 'Mag_Y', 'Mag_Z'])
        writer.writerows(sensor_data)

    print(f'Data written to {csv_file_path}')
