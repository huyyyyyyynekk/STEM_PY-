from machine import SoftI2C, Pin
import time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)

PCA9685_ADDRESS = 0x5F
MODE1 = 0x00
PRESCALE = 0xFE

i2c.writeto_mem(PCA9685_ADDRESS, MODE1, bytes([0x10]))
time.sleep(0.005)
desired_freq = 1000
prescale = int(25000000 / (4096 * desired_freq)) - 1
i2c.writeto_mem(PCA9685_ADDRESS, PRESCALE, bytes([prescale]))
i2c.writeto_mem(PCA9685_ADDRESS, MODE1, bytes([0xA0]))

def set_pwm(channel, on, off):
    channel_reg_base = 0x06 + 4 * channel
    data = [on & 0xFF, on >> 8, off & 0xFF, off >> 8]
    i2c.writeto_mem(PCA9685_ADDRESS, channel_reg_base, bytearray(data))

def set_motor_speed(channel, speed):
    pwm_value = int(speed * 40.95)
    set_pwm(channel, 0, pwm_value)

def motor_moveon():
    motor_right_moveon()
    motor_left_moveon()
    
def motor_backdown():
    motor_right_backdown()
    motor_left_backdown()
    
def motor_turn_left():
    set_motor_speed(2,0)
    set_motor_speed(3,0)
    set_motor_speed(4,100)
    set_motor_speed(5,0)
    
def motor_turn_right():
    set_motor_speed(2,100)
    set_motor_speed(3,0)
    set_motor_speed(4,0)
    set_motor_speed(5,0)
    
def motor_right_moveon():
    set_motor_speed(4,100)
    set_motor_speed(5,0)
  
def motor_right_backdown():
    set_motor_speed(4,0)
    set_motor_speed(5,100)

def motor_left_moveon():
    set_motor_speed(2,0)
    set_motor_speed(3,100)
    
def motor_left_backdown():
    set_motor_speed(2,100)
    set_motor_speed(3,0)
     
