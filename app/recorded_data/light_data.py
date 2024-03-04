import csv
from datetime import datetime, timedelta
import random

def generate_luminosity_data(start_time, duration_seconds, min_lux, max_lux):
    time_stamp = start_time
    time_delta = timedelta(seconds=1)
    data = []

    for _ in range(duration_seconds):
        # Generate a random luminosity value within the specified range
        luminosity_lux = random.randint(min_lux, max_lux)

        data.append([time_stamp.strftime('%Y-%m-%dT%H:%M:%S'), luminosity_lux])
        time_stamp += time_delta

    return data
if __name__ == "__main__":
    # Start time of the data
    start_time = datetime(2024, 2, 17, 12, 0, 0)
    # Duration in seconds (2 minutes)
    duration_seconds = 120
    # Luminosity range in lux (example range, adjust as needed)
    min_lux = 0
    max_lux = 100000

    # Generate the data
    luminosity_data = generate_luminosity_data(start_time, duration_seconds, min_lux, max_lux)

    # Write the data to a CSV file
    csv_file_path = './dummy_data_scripts/luminosity.csv'
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Luminosity_Lux'])
        writer.writerows(luminosity_data)

    print(f'Data written to {csv_file_path}')
