# rocket-telemetry-logger-using-raspberry-pi-pico
A rocket telemetry logger using Raspberry Pi Pico, MPU6050, BMP280, and an OLED display.
Here’s a comprehensive `README.md` file for your project, including warnings, connections, and all necessary details:

---

# Rocket Telemetry Logger Using Raspberry Pi Pico

![Project Image](avionica+_bb.jpg)

This project is a rocket telemetry logger that uses a Raspberry Pi Pico to log roll, pitch, and altitude data from an MPU6050 accelerometer/gyroscope and a BMP280 barometric pressure sensor. The data is displayed on an SSD1306 OLED screen and logged to an SD card for further analysis.

---

Features
- Logs roll, pitch, and altitude data to an SD card.
- Displays real-time data on an OLED screen.
- Plays a tone sequence on startup and shutdown using a buzzer.
- Uses the IBF method to calculate altitude from barometric pressure.

---

Hardware Requirements
- Raspberry Pi Pico
- MPU6050 (Accelerometer/Gyroscope)
- BMP280 (Barometric Pressure Sensor)
- SSD1306 OLED Display (128x64)
- MicroSD Card Module
- Buzzer
- Breadboard and Jumper Wires
- MicroSD Card (formatted to FAT32)

---

Software Requirements
- MicroPython firmware for Raspberry Pi Pico
- Libraries:
  - `machine` (built-in)
  - `imu` (for MPU6050)
  - `bmp280` (for BMP280)
  - `sdcard` (for SD card)
  - `ssd1306` (for OLED display)
  - `math`, `time`, `os` (built-in)

---

Installation
1. Flash your Raspberry Pi Pico with MicroPython. Follow the official guide [here](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).
2. Install the required libraries:
   ```bash
   pip install micropython-mpu6050
   pip install micropython-bmp280
   pip install micropython-ssd1306
   ```
3. Upload the `main.py` script to your Raspberry Pi Pico.
4. Connect the hardware as per the wiring diagram (see below).

---

Wiring Diagram
| Raspberry Pi Pico | MPU6050 | BMP280 | SSD1306 | SD Card Module | Buzzer |
|-------------------|---------|--------|---------|----------------|--------|
| 3V3 (Pin 36)      | VCC     | VCC    | VCC     | VCC            |        |
| GND (Pin 38)      | GND     | GND    | GND     | GND            | GND    |
| GP0 (Pin 1)       |         | SDA    | SDA     |                |        |
| GP1 (Pin 2)       |         | SCL    | SCL     |                |        |
| GP10 (Pin 14)     | SCL     |        |         |                |        |
| GP11 (Pin 15)     | SDA     |        |         |                |        |
| GP12 (Pin 16)     |         |        |         | MISO           |        |
| GP13 (Pin 17)     |         |        |         | CS             |        |
| GP14 (Pin 19)     |         |        |         | MOSI           |        |
| GP15 (Pin 20)     |         |        |         |                | Buzzer |

---

Usage
1. Power on the Raspberry Pi Pico.
2. The buzzer will play a startup tone sequence.
3. The OLED display will show real-time roll, pitch, and altitude data.
4. Data will be logged to the SD card in the file `/sd/sensor_log.txt`.
5. Press `Ctrl+C` to stop the program. The buzzer will play a shutdown tone sequence.

---

## Warnings
1. Double-Check Wiring: Incorrect wiring can damage your components. Always double-check connections before powering on the circuit.
2. Power Supply: Ensure the Raspberry Pi Pico and all components are powered correctly. Overvoltage can damage the Pico and sensors.
3. SD Card Formatting: The SD card must be formatted to FAT32. Incorrect formatting can cause data logging to fail.
4. BMP280 Calibration: The BMP280 sensor may require calibration for accurate altitude readings. Refer to the datasheet for calibration procedures.
5. MPU6050 Orientation: Ensure the MPU6050 is mounted correctly in your rocket. Incorrect orientation will result in inaccurate roll and pitch calculations.
6. Buzzer Volume: The buzzer can be loud. Use a resistor in series if necessary to reduce the volume.
7. Data Logging: Ensure the SD card has sufficient space for logging. Data loss may occur if the card runs out of space.

---

Libraries and Credits
- MPU6050 Library: [micropython-mpu6050](https://github.com/micropython-IMU/micropython-mpu6050)
- BMP280 Library: [micropython-bmp280](https://github.com/dafvid/micropython-bmp280)
- SSD1306 Library: [micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306)
- SD Card Library: [micropython-sdcard](https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/storage/sdcard)

---

License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.

---

Author
[Aryan Khollam](https://github.com/aryankhollam)

---

