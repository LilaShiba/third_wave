import board
import digitalio
import time

class FlipSwitch:
    def __init__(self, pin):
        self.switch = digitalio.DigitalInOut(pin)
        self.switch.direction = digitalio.Direction.INPUT
        self.switch.pull = digitalio.Pull.UP

    @property
    def is_pressed(self):
        return not self.switch.value  # Return True if switch is pressed, False otherwise

# Initialize the flip switch connected to GPIO 17
flip_switch = FlipSwitch(board.D17)

while True:
    if flip_switch.is_pressed:
        print("Switch is ON")
    else:
        print("Switch is OFF")
    time.sleep(0.5)
