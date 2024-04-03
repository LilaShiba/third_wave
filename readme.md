# 🌈🤖 RPI Server Documentation 🌟🔧

## OS Selection for RPI 🌟

After evaluating Raspbian, Ubuntu, and Fedora IoT (FIoT), Raspbian was chosen for its optimal balance of lightweight design and reliability. Raspbian did encounter issues with I2C interfacing, and Ubuntu was deemed too resource-intensive. Documentation for Raspbian is retained in anticipation of future improvements and for showing the work-arounds.

## Documentation Links ❤️🔥⚡

- **Main Landing Page** ❤️✨: [Readme.md](https://github.com/LilaShiba/third_wave/blob/main/readme.md)
- **RPI Board** ⚡: [RPI Documentation](https://github.com/LilaShiba/third_wave/blob/main/board_readme.md)
- **OS Choice** 🌟: [os.md](https://github.com/LilaShiba/third_wave/blob/main/os.md)

# High-Level System Overview ✨

## Environmental Monitoring System

The Environmental Monitoring System described here integrates various sensors to monitor environmental parameters and log data to a CSV file. Additionally, it utilizes indicator lights for real-time visualization of sensor readings.

## Overview

The system includes sensors for measuring acceleration, gyroscope data, magnetometer data, temperature, gas, humidity, pressure, proximity, color, and GPS data. It records sensor data at regular intervals and updates indicator lights based on the sensor readings.

## Components

The following components are utilized in the system:

- **Sensors**:
  - LSM9DS1: Accelerometer, gyroscope, and magnetometer.
  - APDS-9960: Proximity and color sensor.
  - BME680: Temperature, gas, humidity, and pressure sensor.
  - GPS module: For GPS data acquisition.

- **Indicator Lights**: NeoTrellis buttons with RGB LEDs are used to visualize sensor readings in real-time.

- **Other Components**:
  - Flip switch: Input device to trigger certain actions.
  - CSV file: Data is logged to a CSV file for further analysis.

## Operation

1. **Initialization**:
   - The system initializes the I2C connection and sets up various sensors and components.

2. **Sensor Data Reading**:
   - Sensor data is continuously read from the LSM9DS1, APDS-9960, BME680, and GPS module.
   - The read data includes accelerometer, gyroscope, magnetometer, temperature, gas, humidity, pressure, proximity, color, and GPS coordinates.

3. **Indicator Light Control**:
   - The system calculates color values for each sensor reading based on predefined thresholds.
   - Indicator lights are updated to reflect the current sensor readings in real-time.
   - Each sensor has its unique thresholds, ensuring that the color representation is optimized for its specific range.

4. **Data Logging**:
   - Sensor data along with GPS data and indicator state is logged to a CSV file at regular intervals.
   - The CSV file contains timestamped sensor readings, GPS coordinates, and the state of the flip switch.

5. **User Interaction**:
   - Users can interact with the system through the flip switch to trigger certain actions.
   - NeoTrellis buttons allow users to activate certain features or modify the behavior of the system.

6. **End of Operation**:
   - The system continues to record sensor data until the predefined duration is reached.
   - Once the recording duration is complete, the CSV file containing logged data is saved.

## Indicator Light Explanation

The following table explains the colors and ranges for each indicator light:

| Indicator  | Blue (Low)       | Green        | Yellow       | Orange       | Red (High)   |
| ---------- | ---------------- | ------------ | ------------ | ------------ | ------------ |
| Humidity   | 0% - 25%         | 26% - 50%    | 51% - 75%    | 76% - 100%   | N/A          |
| Pressure   | 0 hPa - 1250 hPa | 1251 hPa - 2500 hPa | 2501 hPa - 3750 hPa | 3751 hPa - 5000 hPa | N/A |
| Lux        | 0 lux - 1250 lux | 1251 lux - 2500 lux | 2501 lux - 3750 lux | 3751 lux - 5000 lux | N/A |
| Gas        | 0 ppm - 50000 ppm | 50001 ppm - 100000 ppm | 100001 ppm - 150000 ppm | 150001 ppm - 200000 ppm | N/A |
| Proximity  | 0 cm - 2.5 cm    | 2.6 cm - 5 cm| 5.1 cm - 7.5 cm| 7.6 cm - 10 cm| N/A          |
| GPS        | N/A              | N/A          | N/A          | N/A          | N/A          |

This table provides a visual representation of the indicator lights, their corresponding colors, and the ranges they represent for each sensor parameter.


### Sensor Integration

- **Adafruit LSM9DS1:** Accelerometer, Gyro, Magnetometer [Info](https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/pinouts)
- **Adafruit TSL2591:** Ultra-high-range luminosity sensor [Info](https://learn.adafruit.com/adafruit-tsl2591)
- **MAX4466:** Microphone [Info](https://learn.adafruit.com/adafruit-tsl2591)

### Hardware Connection Guide

[Hardware Wiring Instructions](https://www.circuito.io/app?components=639,9443,44359,200000,779831)

## Development Guide 🛠🧰

### Connecting Hardware

- **Module:** `app/utils/rpi.py`
  - Acts as the bridge for communication with I2C sensors and devices connected to the Raspberry Pi.

### Expanding the Application

- **Module:** `app/api/new_route.py`
  - Implement new routes here and register them within `app/__init__.py`.

### Running the Application 🚀

1. Install dependencies:

## 🚀 Run App 🎮

- **From the Root Directory (Command Spells):**

  - Install packages

    ```
    pip3 install -r requirements.txt
    ```
  
  - Summon the Flask server into existence:

    ```
    python3 app.py
    ```

  - 🌟 This activates the Flask server.

## 📜 Check Logs 📚

- **Location:** `logs` folder
  - 📖 The logs can easily be added to any file by importing from the config folder

# 🔌 API Endpoints 🎇

# Sensor Data Collection API Documentation ✨🧙‍♀️✨

This documentation provides details on the `/sensors` endpoint of our Flask application, designed for initiating sensor data collection asynchronously, with sensors communicating over the I2C bus.

## Overview

Sensors connected via the I2C bus can be controlled and their data collected through this API. The I2C bus allows multiple sensors to be connected to the same bus lines, each sensor having a unique address.

## Registering Sensor Routes

To make the sensor data collection endpoint available, we first register it with a Flask `Blueprint`. This is accomplished in the `register_sensors_routes` function, which accepts a `Blueprint` instance as an argument.

<pre><code>def register_sensors_routes(api_bp: Blueprint) -> None:
    ...
</code></pre>

## Endpoint Details

- **URL:** `/sensors`
- **Method:** `GET`
- **Auth Required:** No
- **Permissions Required:** None

## Query Parameters

- `sensor_id` (int): The ID of the sensor to collect data from, corresponding to its I2C address. (Required)
- `time_stop` (int): Duration in seconds for how long the sensor data collection should run. (Required)
- `hertz` (int): The frequency at which data should be collected, affecting how data is read from the I2C bus. (Optional)

## Success Response

- **Code:** 200 OK
- **Content example:**

<pre><code>{
  "message": "Sensor run initiated"
}
</code></pre>

## Error Response

- **Code:** 400 BAD REQUEST
- **Content example:**

<pre><code>{
  "error": "Error description"
}
</code></pre>

## Example Queries

1. **Initiating Sensor Data Collection**

To start collecting data from a sensor with ID 1 for 60 seconds, send a GET request to the `/sensors` endpoint with the required query parameters:

<pre><code>GET /sensors?sensor_id=1&time_stop=60</code></pre>

2. **Specifying Data Collection Frequency**

To specify the frequency of data collection, include the `hertz` parameter in your query:

<pre><code>GET /sensors?sensor_id=1&time_stop=60&hertz=5</code></pre>

This request collects data from sensor ID 1 for 60 seconds at a frequency of 5 Hz.

## Notes on I2C Communication

- Sensors on the I2C bus are addressed using their unique I2C addresses. Ensure the `sensor_id` matches the sensor's I2C address.
- The I2C bus allows for efficient communication with multiple sensors, but care must be taken to manage bus traffic and avoid collisions.
- The `hertz` parameter can influence how often the I2C bus is queried, which is crucial for sensors that require time to refresh their data.

✨🧙‍♀️✨
