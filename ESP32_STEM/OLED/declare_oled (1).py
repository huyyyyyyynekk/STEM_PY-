from machine import Pin
from machine import SoftI2C
import ssd1306
import framebuf
import time
from image import *

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 64
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def oled_print_emotion(buffer):
  a=framebuf.FrameBuffer(buffer, 64, 64, framebuf.MONO_HLSB)
  oled.fill(0)
  oled.framebuf.blit(a, 0, 8)
  oled.show()

def oled_print_char(text, a, b):
  oled.fill(0)
  x = a
  y = b
  for char in text:
    oled.text(char, x, y)
    x += 8
    if x >= 64:
      x = 0
      y += 8
      if y >= 64:
        break
  oled.show()
  time.sleep(2)

def oled_print_char_run(text, a, b):
  screen = [[a, b, text]]
  for i in range (0, (64+1)*2, 1):
    for line in screen:
      oled.text(line[2], -64 + i, line[1])
    oled.show()
    if i != 64:
      oled.fill(0)
