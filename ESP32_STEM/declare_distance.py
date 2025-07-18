nfrom machine import Pin,SoftI2C
from vl53l1x import VL53L0X
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
tof = VL53L0X(i2c)

def vl53l1x_read():
    tof.start()
    distance=tof.read()
    tof.stop()
    return distance

def vl53l1x_close_distance():
    return vl53l1x_read() < 15

def vl53l1x_far_distance():
    return  vl53l1x_read() > 300

