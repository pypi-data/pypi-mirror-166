# RPi-BlinkPico Library

Instructions and example code for using BlinkPico with MicroPython and RaspberryPI Pico.


## Matrix Display

You can get access of the LED matrix display through the variable `display`.

* **blink_rate(rate=None)**

Choose the blink rate of the LEDs from these options: `Matrix.NO_BLINK`, `Matrix.BLINK_SLOW`, `Matrix.BLINK_MEDIUM`, and `Matrix.BLINK_FAST`.
    
* **brightness(brightness)**

Set the value of the brigthness of the LEDs from `0` to `100`.

* **fill(value)**

Set all the LEDs of the display `on` if the value is `1`, or `off` if value is `0`.

* **show()**

Update the LEDs of the display.

* **clear()**

Set all pixels off (same as fill(0))

* **auto_show(show=False)**

Automatically update the LEDs of the display upon changes.


### Note

This code is adapted from the [AdaFruit Circuitpython library](https://github.com/adafruit/Adafruit_CircuitPython_HT16K33).



### Examples

Here an example of how to use the LED display to draw a smily face

```py
from pyblinkpico import *
import time

display.brightness(50)
display.blink_rate(Matrix.NO_BLINK)
display.auto_show(True)
display.clear()

# smile
for row in range(2, 6):
    display[row, 0] = 1
    display[row, 7] = 1
    time.sleep_ms(100)

for column in range(2, 6):
    display[0, column] = 1
    display[7, column] = 1
    time.sleep_ms(100)

display[1,1] = 1
display[1,6] = 1
display[6,1] = 1
display[6,6] = 1

# eyes
display[2,2] = 1
display[2,5] = 1

# mouth
display[4,2] = 1
display[4,5] = 1
display[5,3] = 1
display[5,4] = 1
```

## Button

There are three buttons available: `button_a`, `button_b` and `button_c`.

* **is_pressed**

Returns _True_ if the specified button is currently being held down, and _False_ otherwise.

* **was_pressed**

Returns _True_ or _False_ to indicate if the button was pressed (went from up to down) since the device started or the last time this method was called. Calling this method will clear the press state so that the button must be pressed again before this method will return _True_ again.

* **get_presses**

Returns the running total of button presses, and resets this total to zero before returning.


### Note

Buttons behave as described in [this page](https://microbit-micropython.readthedocs.io/en/v1.0.1/button.html).


### Examples

Here an example of how to use the buttons

```py
from pyblinkpico import *
import time

while True:
  print(button_a.is_pressed())
  print(button_b.is_pressed())
  print(button_c.is_pressed())
  time.sleep(2)
```

