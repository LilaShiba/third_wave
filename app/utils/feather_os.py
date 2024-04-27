import time
import random
import board
import busio
from adafruit_apds9960.apds9960 import APDS9960
import adafruit_bme680
import adafruit_gps
from adafruit_neotrellis.neotrellis import NeoTrellis
import adafruit_tsl2591
import adafruit_lsm9ds1

import time
import board
import busio
import adafruit_lsm9ds1



OFF = (0, 0, 0)

class Device:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor_apds9960 = APDS9960(self.i2c)
        self.sensor_bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
        self.gps = adafruit_gps.GPS_GtopI2C(self.i2c, debug=False)
        self.trellis = NeoTrellis(self.i2c)
        self.sensor_lsm9ds1  = adafruit_lsm9ds1.LSM9DS1_I2C(self.i2c)
        self.trellis.brightness = 0.8
        self.init_trellis()

        self.sensor_tsl2591 = adafruit_tsl2591.TSL2591(self.i2c)
        self.sensor_tsl2591.gain = adafruit_tsl2591.GAIN_LOW
        print('all sensors loaded')

    def init_trellis(self):
        for i in range(16):
            self.trellis.activate_key(i, NeoTrellis.EDGE_RISING)
            self.trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
            self.trellis.callbacks[i] = self.blink

    def blink(self, event):
        """Handles button press events."""
        global button_press_time, any_key_pressed
        # Turn the LED on when a rising edge is detected
        if event.edge == NeoTrellis.EDGE_RISING:
            self.trellis.pixels[event.number] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.trellis.brightness = random.uniform(0.5, 1)
            # Update button press time
            button_press_time = time.monotonic()
            # Update any_key_pressed
            any_key_pressed = event.number
        # Turn the LED off after 2 seconds
        elif event.edge == NeoTrellis.EDGE_FALLING or (event.edge == NeoTrellis.EDGE_RISING and time.monotonic() > button_press_time):
            self.trellis.pixels[event.number] = OFF
            any_key_pressed = -1

    def record_sensor_data(self, print_interval: int = 60):
        idx = 0
        while True:
            start_time = time.time()

            proximity, (color_r, color_g, color_b, color_c), lux = self.read_apds9960()
            bme680_temp, gas, humidity, pressure = self.read_bme680()
            latitude, longitude, speed, gps_timestamp = self.read_gps()
            accel, gyro, magno = self.read_lsm9ds1()
            self.init_trellis()
            if idx % print_interval == 0:
                print(f"Timestamp: {time.time()}")
                print(f"Proximity: {proximity}")
                print(f"Color: ({color_r}, {color_g}, {color_b}, {color_c})")
                print(f"Lux: {lux}")
                print(f"Accel: {accel} | Gyro: {gyro} | Mag: {magno}")
                print(f"BME680 Temperature: {bme680_temp}")
                print(f"Gas: {gas}")
                print(f"Humidity: {humidity}")
                print(f"Pressure: {pressure}")
                print(f"GPS Latitude: {latitude}")
                print(f"GPS Longitude: {longitude}")
                print(f"GPS Speed: {speed}")
                print("-" * 50)

            idx += 1

    def read_apds9960(self):
        proximity = self.sensor_apds9960.proximity
        color_data = self.sensor_apds9960.color_data
        lux = sum(color_data)
        return proximity, color_data, lux
    
    def read_lsm9ds1(self):
        """Reads Accel, Gyro, and Magnometer from the LSM9DS1"""
        

        acc_x, acc_y, acc_z = self.sensor_lsm9ds1.acceleration
        gyro_x, gyro_y, gyro_z = self.sensor_lsm9ds1.gyro
        mag_x, mag_y, mag_z = self.sensor_lsm9ds1.magnetic
  
        return [(acc_x, acc_y, acc_z), (gyro_x, gyro_y, gyro_z), (mag_x, mag_y, mag_z)]

    def read_bme680(self):
        temperature = self.sensor_bme680.temperature
        gas = self.sensor_bme680.gas
        humidity = self.sensor_bme680.humidity
        pressure = self.sensor_bme680.pressure
        return temperature, gas, humidity, pressure

    def read_gps(self):
        self.gps.update()
        latitude = self.gps.latitude if self.gps.latitude is not None else 0.00
        longitude = self.gps.longitude if self.gps.longitude is not None else 0.00
        speed = self.gps.speed_knots if self.gps.speed_knots is not None else 0.00
        timestamp = self.gps.timestamp_utc
        return latitude, longitude, speed, timestamp

    def read_tsl2591(self):
        """Reads data from the TSL2591 sensor."""
        return self.sensor_tsl2591.lux, self.sensor_tsl2591.infrared


    def env_check(self,
                  humidity, pressure, lux, gas,
                  proximity, b, gps, tsl2591_lux, tsl2591_ir, accel, gyro, magno, bme680_temp):
        """Checks environmental parameters and updates indicator lights accordingly."""
        # Define max values for each sensor
        max_values = {
            'humidity': 60,
            'pressure': 1013.25,
            'lux': 5000,
            'gas': 100000,
            'proximity': 14,
            'ir': 100
        }

        # Update indicator lights based on sensor values
        self.trellis.pixels[0] = self.generate_color(humidity, max_values['humidity'])
        self.trellis.pixels[1] = self.generate_color(pressure, max_values['pressure'])
        self.trellis.pixels[2] = self.generate_color(gas, max_values['gas'])
        self.trellis.pixels[3] = self.generate_color(lux, max_values['lux'])
        self.trellis.pixels[4] = self.generate_color(proximity, max_values['proximity'])
        self.trellis.pixels[5] = self.generate_color(float(tsl2591_lux), max_values['lux'])
        self.trellis.pixels[6] = self.generate_color(float(tsl2591_ir), max_values['ir'])
        

        # Handle GPS separately
        if gps is not None:
            self.pretty_stars()

        if b % 10 == 0:
            print(f"  Humidity: {humidity:.2f}%")
            print(f"  Pressure: {pressure:.2f} hPa")
            print(f"  Gas Resistance: {gas:.2f} ohms")
            print(f"  Proximity: {proximity:.2f}")
            print(f"  POS: {gps[0]:.6f} Longitude: {gps[1]:.6f}")
            print(f"  Lux: {tsl2591_lux:.2f} IR: {tsl2591_ir:.2f}")
            print(f"  BME680 Temperature: {bme680_temp:.2f}°C")
            print(f" Accel: {accel} | Gyro: {gyro} | Mag {magno}")

    def generate_color(self, value, max_value):
        """
        Generate a color based on the value and max_value.

        Args:
            value: The sensor value.
            max_value: The maximum threshold for the sensor value.

        Returns:
            Tuple[int, int, int]: The RGB color tuple.
        """
        # Calculate color components
        red = int((value / max_value) * 255)
        green = int(((max_value - value) / max_value) * 255)
        blue = 125  # Fixed blue component for Transgender Pride flag

        # Keep to the valid range (0-255)
        red = max(0, min(red, 255))
        green = max(0, min(green, 255))

        return red, green, blue

    def pretty_stars(self):
        """Set random warm colors (excluding red) for pixels 5 to 9."""
        def generate_warm_color():
            """Generate a random warm color (excluding red)."""
            # Generate random warm colors
            red = random.randint(0, 100)
            green = random.randint(100, 255)
            blue = random.randint(100, 255)
            return red, green, blue

        # Assign random warm colors to pixels 5 to 9
        for i in range(8, 15):
            if random.random() > 0.99:
                self.trellis.pixels[i] = generate_warm_color()
                self.trellis.pixels[i] = OFF

    def main(self):
        frequency = 60 # Default frequency in Hertz
        interval = 1 / frequency
        b = 0
        while True:
            start_time = time.time()

            proximity, color_data, lux = self.read_apds9960()
            bme680_temp, gas, humidity, pressure = self.read_bme680()
            latitude, longitude, speed, gps_timestamp = self.read_gps()
            tsl2591_lux, tsl2591_ir = self.read_tsl2591()
            accel, gyro, magno = self.read_lsm9ds1()

            self.env_check(humidity, pressure, lux, gas, proximity, b, (latitude, longitude), tsl2591_lux, tsl2591_ir, accel, gyro, magno, bme680_temp)

            # Adjust sleep time based on Hertz
            elapsed_time = time.time() - start_time
            b += 1
            if elapsed_time < interval:
                time.sleep(interval - elapsed_time)

if __name__ == "__main__":
    device = Device()
    device.main()
    print('os launch successfull')
