#Khối khởi tạo
from machine import Pin,SoftI2C
from image import *
import ssd1306
import framebuf
I2c = SoftI2C(scl=Pin(22), sda=Pin(21))
Display = ssd1306.SSD1306_I2C(128, 64, I2c)

def print_emotion(buffer):
    a=framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB)
    Display.fill(0)
    Display.framebuf.blit(a, 8, 0)
    Display.show()
#Khối khởi tạo
    
#Khối hiển thị cảm xúc %d        #%d = Mặt cười ,Mặt buồn, Mặt dận, Mặt hôn gió, Mặt cười lè lưỡi, Mặt đang ngủ
    print_emotion(Mat_cuoi)                #%d = Mat_cuoi, Mat_buon, Mat_dan, Mat_hongio, Mat_cuoileluoi, Mat_dangngu 
#Khối hiển thị cảm xúc %d   

  
