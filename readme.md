# 🌈🤖 🌟🔧

Video Demo of larger product: [video](https://www.youtube.com/watch?v=wGUgLWJEKcA)

## OS Selection for RPI 🌟

After evaluating Raspbian, Ubuntu, and Fedora IoT (FIoT), Raspbian was chosen for its optimal balance of lightweight design and reliability. Raspbian did encounter issues with I2C interfacing, and Ubuntu was deemed too resource-intensive. Documentation for Raspbian is retained in anticipation of future improvements and for showing the work-arounds.

## Documentation Links ❤️🔥⚡

- **Main Landing Page** ❤️✨: [Readme.md](https://github.com/LilaShiba/third_wave/blob/main/readme.md)
- **RPI Board** ⚡: [RPI Documentation](https://github.com/LilaShiba/third_wave/blob/main/board_readme.md)

# High-Level System Overview ✨
The main files are located in 'app/utils' and included the [main.py](https://github.com/LilaShiba/third_wave/blob/main/app/utils/main.py) & [send_code.py](https://github.com/LilaShiba/third_wave/blob/main/app/utils/send_code.py)


## Environmental Monitoring System

The Environmental Monitoring System described here integrates various sensors to monitor environmental parameters and log data to a CSV file. Additionally, it utilizes indicator lights for real-time visualization of sensor readings.

## Overview

The system includes sensors for measuring acceleration, gyroscope data, magnetometer data, temperature, gas, humidity, pressure, proximity, color, and GPS data. It records sensor data at a specified hertz rate, and updates indicator lights based on the sensor readings. The computing power is best kept in a range of 1-90 hertzs.

## Components

The following components are utilized in the system:

- **Sensors**:
  - LSM9DS1: Accelerometer, gyroscope, and magnetometer.
  - APDS-9960: Proximity and color sensor.
  - BME680: Temperature, gas, humidity, and pressure sensor.
  - GPS module: For GPS data.

- **Indicator Lights**: NeoTrellis buttons with RGB LEDs are used to visualize sensor readings in real-time, and as an actuator for stemming.

- **Other Components**:
  - Flip switch: Input device to trigger certain actions.
  - CSV file: Data is logged to a CSV file for further analysis.

## Operation

1. **Initialization**:
   - The system initializes the I2C connection and sets up the various sensors and components.

2. **Sensor Data Reading**:
   - Sensor data is continuously read from the LSM9DS1, APDS-9960, BME680, and GPS module.

3. **Indicator Light Control**:
   - The system calculates color values for each sensor reading based on predefined thresholds.
   - Indicator lights are updated to reflect the current sensor readings in real-time.
   - Each sensor has its unique thresholds, ensuring that the color representation is optimized for its specific range.
   - The color representation is bounded in a range to represent the transgender pride flag.

4. **Data Logging**:
   - Sensor data along with GPS data and indicator state is logged to a CSV file at the hertz rate provided.
   - The CSV file contains timestamped sensor readings, GPS coordinates, and the state of the flip switch.

5. **User Interaction**:
   - Users can interact with the system through the flip switch to trigger certain actions.
   - NeoTrellis buttons allow users to interact with the device via stimming.

6. **End of Operation**:
   - The system continues to record sensor data until the predefined duration is reached.
   - Once the recording duration is complete, the CSV file containing logged data is sent to the AWS backend.
   - The CSV file is then earsed to ensure ample space on the RPi. For example, it's common for csv files to reach over 20 megabites!

### Sensor Integration and Sources

- **Adafruit LSM9DS1:** Accelerometer, Gyro, Magnetometer [Info](https://learn.adafruit.com/adafruit-lsm9ds1-accelerometer-plus-gyro-plus-magnetometer-9-dof-breakout/pinouts)
- **Adafruit TSL2591:** Ultra-high-range luminosity sensor [Info](https://learn.adafruit.com/adafruit-tsl2591)
- **MAX4466:** Microphone [Info](https://learn.adafruit.com/adafruit-tsl2591)

### Hardware Connection Guide

[Hardware Wiring Instructions](https://www.circuito.io/app?components=9443,12787,164792,200000,243599,488167,763365,779831)

### Running the Application 🚀

1. Install dependencies:

## 🚀 Run App 🎮

- **From the Root Directory (Command Spells):**

  - Install packages

    ```
    pip3 install -r requirements.txt
    ```
  
  - Run main file!

    ```
    python3 app/utils/main.py
    ```

  - 🌟 This activates the environment check subroutines.


## Notes on I2C Communication

- Sensors on the I2C bus are addressed using their unique I2C addresses. Ensure the device has I2C enabled! 
- The `hertz` parameter can influence how often the I2C bus is queried, which is crucial for sensors that require time to refresh their data.
- The GPS and sensors take about 5-10 seconds to "initalize". That is, callibrate their own readings.

✨🧙‍♀️✨
