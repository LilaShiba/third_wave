import csv
import json
import requests
from typing import List, Dict

class Transport:

    def __init__(self, file_path: str):
        # Customized for AWS 
        self.file_path = file_path
        self.sensor_data = []
        self.url = 
        self.headers = {'Content-Type': 'application/json'}
        self.formatted_data = []
        self.json_data_with_backslashes = None
        self.response = None

    def read_sensor_data(self) -> List[Dict[str, str]]:
        """
        Read sensor data from a CSV file.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing sensor data.
        """
        with open(self.file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.sensor_data.append(row)
        return self.sensor_data

    def format_sensor_data(self, row: Dict[str, str]) -> str:
        """
        Format sensor data into the required JSON structure.

        Args:
            row (Dict[str, str]): A dictionary containing sensor data for a single row.

        Returns:
            str: A string containing formatted sensor data in the specified JSON style.
        """
        for key, value in row.items():
            if key != 'Timestamp':
                formatted_row = {
                    "sensor": key,
                    "trigger": key.upper(),
                    "value": value,
                    "unit": "",  # You may need to specify units based on sensor type
                    "timestamp": row["Timestamp"]
                }
                self.formatted_data.append(formatted_row)
        json_data = json.dumps(self.formatted_data)
        self.json_data_with_backslashes = json_data.replace('"', '\\"')  # Add backslashes
        return str(self.json_data_with_backslashes)

    def send_sensor_data(self, data) -> None:
        """
        Send sensor data to the specified API endpoint.

        Args:
            formatted_data (str): A string containing formatted sensor data for the object.
        """
       
        response = requests.post(self.url, data=data, headers=self.headers)
        if response.status_code != 200:
            print("Failed to send sensor data. Status code:", response.status_code)

    # Function to clear data in CSV except for headers
    def clear_data_except_headers(self):
        with open(self.file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Readd the header

        with open(self.file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)  # Write back the header only

    def main(self):
        self.read_sensor_data()
        for row in self.sensor_data:
            formatted_data = self.format_sensor_data(row)
            #print(formatted_data)  # Debug print
            self.send_sensor_data('"' + formatted_data + '"')
        self.clear_data_except_headers()



if __name__ == "__main__":
    example_sensor_object = Transport(file_path="data/sensor_data_2024-04-10T16:21.csv")
    example_sensor_object.main()
    



