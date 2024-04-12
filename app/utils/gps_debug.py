import time
import board
import busio
import adafruit_gps

# Initialize I2C connection.
i2c = busio.I2C(board.SCL, board.SDA)

# Create a GPS module instance.
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Set debug to True to print out more details.

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()

    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print('Waiting for fix...')
            continue

        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print('=' * 40)  # Print a separator line.
        print(f"Fix timestamp: {gps.timestamp_utc.tm_hour}:{gps.timestamp_utc.tm_min}:{gps.timestamp_utc.tm_sec}")
        print(f"Latitude: {gps.latitude:.6f} degrees")
        print(f"Longitude: {gps.longitude:.6f} degrees")
        print(f"Fix quality: {gps.fix_quality}")
        if gps.satellites is not None:
            print(f"# satellites: {gps.satellites}")
