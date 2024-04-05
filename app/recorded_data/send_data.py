import csv
import json
import requests
from typing import List, Dict

def read_sensor_data(file_path: str) -> List[Dict[str, str]]:
    """
    Read sensor data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing sensor data.
    """
    sensor_data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            sensor_data.append(row)
    return sensor_data

def format_sensor_data(row: Dict[str, str]) -> str:
    """
    Format sensor data into the required JSON structure.

    Args:
        row (Dict[str, str]): A dictionary containing sensor data for a single row.

    Returns:
        str: A string containing formatted sensor data in the specified JSON style.
    """
    formatted_data = []
    for key, value in row.items():
        if key != 'Timestamp':
            formatted_row = {
                "sensor": key,
                "trigger": key.upper(),
                "value": value,
                "unit": "",  
                "timestamp": row["Timestamp"]
            }
            formatted_data.append(formatted_row)
    json_data = json.dumps(formatted_data)
    json_data_with_backslashes = json_data.replace('"', '\\"')  # Add backslashes
    return str(json_data_with_backslashes)

def send_sensor_data(formatted_data: str) -> None:
    """
    Send sensor data to the specified API endpoint.

    Args:
        formatted_data (str): A string containing formatted sensor data.
    """
    url = "http://3.228.67.119:5000/sensordata/insert-sensor-data"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=formatted_data, headers=headers)
    if response.status_code == 200:
        print("Sensor data sent successfully.")
    else:
        print("Failed to send sensor data. Status code:", response.status_code)

if __name__ == "__main__":
    file_path = "sensor_data_2024-04-02T10:21.csv"  # Replace with your actual CSV file path
    sensor_data = read_sensor_data(file_path)
 
    for row in sensor_data:
        formatted_data = format_sensor_data(row)
        print(formatted_data)  # Debug print
        send_sensor_data('"' + formatted_data + '"')
