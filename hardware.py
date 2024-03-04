from adafruit_lsm9ds1 import LSM9DS1_I2C
from adafruit_tsl2591 import TSL2591
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
# Initialize sensors
movement_sensors = LSM9DS1_I2C(i2c)
#light_sensor = TSL2591(i2c)
