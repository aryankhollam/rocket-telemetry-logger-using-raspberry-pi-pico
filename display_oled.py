from machine import I2C, Pin, PWM
from imu import MPU6050
from bmp280 import *
import math
import time
import utime
from ssd1306 import SSD1306_I2C
from time import sleep

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
        sleep(0.1)
    bequiet()

# Play the turn on sound when the code starts
playsong(turn_on_song)

# Initialize I2C, MPU6050, and BMP280
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
mpu = MPU6050(i2c)

ERROR = -3.3
sclPin = Pin(1)
sdaPin = Pin(0)

i2c_object = I2C(0, scl=sclPin, sda=sdaPin, freq=1000000)
bmp280_object = BMP280(i2c_object, addr=0x76, use_case=BMP280_CASE_WEATHER)

bmp280_object.power_mode = BMP280_POWER_NORMAL
bmp280_object.oversample = BMP280_OS_HIGH
bmp280_object.temp_os = BMP280_TEMP_OS_8
bmp280_object.press_os = BMP280_TEMP_OS_4
bmp280_object.standby = BMP280_STANDBY_250
bmp280_object.iir = BMP280_IIR_FILTER_2

def altitude_HYP(hPa, temperature):
    sea_level_pressure = 1013.25
    pressure_ratio = sea_level_pressure / hPa
    h = (((pressure_ratio**(1/5.257)) - 1) * temperature) / 0.0065
    return h

def altitude_IBF(pressure):
    sea_level_pressure = 1013.25
    pressure_ratio = pressure / sea_level_pressure
    altitude = 44330 * (1 - (pressure_ratio**(1 / 5.255)))
    return altitude

# Function to draw a line that rotates based on the X-axis angle (pitch)
def draw_linep(angle, length):
    xCenter = 96  # Center of the display in X (128px wide, so middle is 64)
    yCenter = 16  # Center of the display in Y (64px high, so middle is 32)
    # Convert the angle to radians for trigonometric functions
    rad = math.radians(angle)
    # Calculate the end points of the line for both directions
    xEnd1 = int(xCenter + length * math.sin(rad))  # End point in one direction
    yEnd1 = int(yCenter - length * math.cos(rad))  # Corresponding Y for that direction
    xEnd2 = int(xCenter - length * math.sin(rad))  # End point in the opposite direction
    yEnd2 = int(yCenter + length * math.cos(rad))  # Corresponding Y for the other end
    dsp.line(xEnd1, yEnd1, xEnd2, yEnd2, 1)
    
def draw_liner(angle, length):
    xCenter = 96  # Center of the display in X (128px wide, so middle is 64)
    yCenter = 48  # Center of the display in Y (64px high, so middle is 32)
    # Convert the angle to radians for trigonometric functions
    rad = math.radians(angle)
    # Calculate the end points of the line for both directions
    xEnd1 = int(xCenter + length * math.sin(rad))  # End point in one direction
    yEnd1 = int(yCenter - length * math.cos(rad))  # Corresponding Y for that direction
    xEnd2 = int(xCenter - length * math.sin(rad))  # End point in the opposite direction
    yEnd2 = int(yCenter + length * math.cos(rad))  # Corresponding Y for the other end
    dsp.line(xEnd1, yEnd1, xEnd2, yEnd2, 1)

# Initialize the OLED display
i2c2 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
dsp = SSD1306_I2C(128, 64, i2c2)
dsp.fill(0)

try:
    while True:
        dsp.fill(0)
        temperature_c = bmp280_object.temperature
        temperature_k = temperature_c + 273.15
        pressure = bmp280_object.pressure
        pressure_hPa = ( pressure * 0.01 ) + ERROR
        h = altitude_HYP(pressure_hPa, temperature_k)
        altitude = altitude_IBF(pressure_hPa)
        altitudef = altitude*3.28084
        tem=round(mpu.temperature,2)
        xAccel=mpu.accel.z
        yAccel=mpu.accel.x
        zAccel=mpu.accel.y
        pitch=math.atan(zAccel/xAccel)
        roll=math.atan(yAccel/xAccel)
        pitchDeg=pitch/(2*math.pi)*360
        rollDeg=roll/(2*math.pi)*360
        time.sleep(.1)
        dsp.text('Pitch:', 0, 0)
        dsp.text(str(round(pitchDeg, 1)), 0, 10)
        dsp.text('Roll:', 0, 20)
        dsp.text(str(round(rollDeg, 1)), 0, 30)
        dsp.text('Altitude:', 0, 43)
        dsp.text(str(round(altitudef, 1)), 0, 53)
        draw_linep(pitchDeg, 10)
        draw_liner(rollDeg, 10)
        dsp.show()
        time.sleep(0.1)

except KeyboardInterrupt:
    # This block will run when Ctrl + C is pressed
    print("Turning off sensors and display...")

    # Play the turn off sound
    playsong(turn_off_song)

    # Clear the display and turn it off
    dsp.fill(0)
    dsp.show()

    # Set BMP280 to sleep mode
    bmp280_object.power_mode = BMP280_POWER_SLEEP

    print("Sensors and display turned off safely.")
