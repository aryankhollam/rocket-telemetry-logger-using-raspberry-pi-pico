from machine import Pin, SPI, I2C, PWM
from imu import MPU6050
from bmp280 import *
import math
import time
import sdcard
import os
import ssd1306  # Import the SSD1306 library

# Initialize SD card
spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
sd = sdcard.SDCard(spi, Pin(13))
os.mount(sd, '/sd')

# Create/Open the log file
log_file = open("/sd/sensor_log.txt", "w")
log_file.write("Seconds\tRoll\tPitch\tAltitude (ft)\n")
log_file.close()

# Initialize Buzzer
buzzer = PWM(Pin(15))

# Define tones
tones = {
    "E5": 659,
    "G5": 784,
    "A5": 880,
}

# Define songs
turn_on_song = ["E5", "G5", "A5"]
turn_off_song = ["A5", "G5", "E5"]

# Function to play a specific tone
def playtone(frequency):
    buzzer.duty_u16(6000)
    buzzer.freq(frequency)

# Function to stop the buzzer
def bequiet():
    buzzer.duty_u16(0)

# Function to play a song
def playsong(mysong):
    for i in range(len(mysong)):
        if mysong[i] == "P":
            bequiet()
        else:
            playtone(tones[mysong[i]])
        time.sleep(0.1)
    bequiet()

# Play the turn on sound when the code starts
playsong(turn_on_song)

# Initialize I2C, MPU6050, BMP280, and OLED
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
mpu = MPU6050(i2c)

ERROR = -3.3
i2c_object = I2C(0, scl=Pin(1), sda=Pin(0), freq=1000000)
bmp280_object = BMP280(i2c_object, addr=0x76)

bmp280_object.power_mode = BMP280_POWER_NORMAL
bmp280_object.oversample = BMP280_OS_HIGH
bmp280_object.temp_os = BMP280_TEMP_OS_8
bmp280_object.press_os = BMP280_TEMP_OS_4
bmp280_object.standby = BMP280_STANDBY_250
bmp280_object.iir = BMP280_IIR_FILTER_2

# Initialize OLED display
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Function to calculate altitude (IBF method)
def altitude_IBF(pressure):
    sea_level_pressure = 1013.25
    pressure_ratio = pressure / sea_level_pressure
    altitude = 44330 * (1 - (pressure_ratio**(1 / 5.255)))
    return altitude

# Start logging
start_time = time.ticks_ms()

try:
    while True:
        # Open the log file in append mode
        log_file = open("/sd/sensor_log.txt", "a")
        
        # Read BMP280 data
        temperature_c = bmp280_object.temperature
        temperature_k = temperature_c + 273.15
        pressure = bmp280_object.pressure
        pressure_hPa = (pressure * 0.01) + ERROR
        altitude = altitude_IBF(pressure_hPa)
        altitude_ft = altitude * 3.28084  # Convert meters to feet

        # Read MPU6050 data
        xAccel = mpu.accel.z
        yAccel = mpu.accel.x
        zAccel = mpu.accel.y

        pitch = math.atan(zAccel / xAccel)
        roll = math.atan(yAccel / xAccel)

        pitchDeg = pitch / (2 * math.pi) * 360
        rollDeg = roll / (2 * math.pi) * 360

        # Log data to the file
        elapsed_time = (time.ticks_ms() - start_time) / 1000  # Get elapsed time in seconds
        log_file.write(f"{elapsed_time:.1f}\t{rollDeg:.2f}\t{pitchDeg:.2f}\t{altitude_ft:.2f}\n")

        # Print data to screen
        print(f"{elapsed_time:.1f}\t\t{rollDeg:.2f}\t\t{pitchDeg:.2f}\t\t{altitude_ft:.2f}")

        # Display data on OLED
        oled.fill(0)  # Clear the display
        oled.text(f"Time: {elapsed_time:.1f}s", 0, 0)
        oled.text(f"Roll: {rollDeg:.2f}°", 0, 10)
        oled.text(f"Pitch: {pitchDeg:.2f}°", 0, 20)
        oled.text(f"Alt: {altitude_ft:.2f}ft", 0, 30)
        oled.show()

        log_file.close()
        
        time.sleep(0.1)  # 10 readings per second

except KeyboardInterrupt:
    print("\nStopping data logging...")

    # Set BMP280 to sleep mode
    bmp280_object.power_mode = BMP280_POWER_SLEEP

    print("Sensors turned off safely.")
