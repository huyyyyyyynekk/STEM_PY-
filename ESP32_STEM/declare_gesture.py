from machine import Pin, SoftI2C
from const import *
from device import uAPDS9960 as APDS9960
import time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
apds= APDS9960(i2c)
i2c.start()
slave_address = 0x39  
i2c.writeto(slave_address, bytes([0x80, 0x03]))
NONE = 0
TRÁI = 1
PHẢI = 2
TRÊN = 3
DƯỚI = 4
ĐỎ = 5
LỤC = 6
LAM = 7

def apds_read_color():
    i2c.writeto(slave_address, bytes([0x96]))  
    red_data = i2c.readfrom(slave_address, 2)
    red_value =  red_data[1] 
    red_value = min(255,red_value)
    
    i2c.writeto(slave_address, bytes([0x98]))  
    green_data = i2c.readfrom(slave_address, 2)
    green_value = green_data[1] * 255 + green_data[0] // 4
    green_value = green_value // 4
    green_value = min(255,green_value)

    i2c.writeto(slave_address, bytes([0x9A]))  
    blue_data = i2c.readfrom(slave_address, 2)
    blue_value = blue_data[1] * 255 + blue_data[0] // 4
    blue_value = blue_value // 4
    blue_value = min(255,blue_value)
    
    if red_value == 1 or red_value >= 10 :
        return ĐỎ
    if green_value >= 120:
        return LỤC
    if blue_value >= 130:
        return LAM
    
def apds_read_gesture():
    apds.setProximityIntLowThreshold(50)
    apds.enableGestureSensor()
    if apds.isGestureAvailable():
        motion = apds.readGesture()
        if motion == 1:
            return TRÁI
        if motion == 2:
            return PHẢI
        if motion == 4:
            return DƯỚI
        if motion == 3:
            return TRÊN
        if motion == 0:
            return NONE
