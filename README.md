# Live Transcribe

A tool that provides closed captions for conversations in real-time.
An in depth view into the project architecture can be found [here](link).

## Requirements

- Arduino Nano (other variants of the Arduino Uno also work)
- Raspberry Pi / Personal Computer
- SSD1306

## Wiring Diagram
<img width="1311" height="422" alt="image" src="https://github.com/user-attachments/assets/af09c418-bc76-45ef-a67e-20080caa15e0" />

- 5V - VDD
- GND - GND
- A4 - SDA
- A5 - SCL

## Deployment 

**Option 1 (Arduino IDE)**

1. Open the display folder and open the `display.ino` file
2. Select **Arduino Nano** from the boards menu and connect the board using a USB cable
3. Upload/Flash the file to the Nano
4. Run `main.py`

Note that you may have to update the port parameter in `main.py`.

**Option 2 (Linux / Raspberry Pi)**

If you're deploying directly from the Pi, you must first flash the Arduino Nano using `arduino-cli`. In the `display` folder, run:

```bash
arduino-cli compile --fqbn arduino:avr:nano --output-dir . ~/Live-Transcribe/display
sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:display.ino.hex:i
```

Replace `/dev/ttyUSB0` with the location of the Arduino Nano. After flashing is complete, run `main.py`.
Note that you may have to update the port parameter in `main.py`.
