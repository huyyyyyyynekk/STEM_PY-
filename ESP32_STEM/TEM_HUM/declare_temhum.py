from machine import Pin,SoftI2C
from am2320 import AM2320
import utime
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
sensor = AM2320(i2c)        

def am2320_read_temperature():
    sensor.measure()
    temp=sensor.temperature()
    utime.sleep_ms(100)
    return temp

def am2320_read_humidity():
    sensor.measure()
    humi=sensor.humidity()
    return humi

def am2320_high_temperature():
    return am2320_read_temperature() >= 32

def am2320_low_temperature():
    return am2320_read_temperature() <= 12

def am2320_high_humidity():
    return am2320_read_humidity() >= 70

def am2320_low_humidity():
    return am2320_read_humidity()  <= 40

def am2320_delay_time():
    utime.sleep(2)
    
while True:
    huy = am2320_read_temperature()
    print(huy)
    