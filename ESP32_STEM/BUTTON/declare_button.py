from machine import Pin,SoftI2C
import utime
import pcf8574

i2c = SoftI2C(scl = Pin(22), sda = Pin(21))
pcf = pcf8574.PCF8574(i2c, 0x27)
button_last_debounce_time_0 = 0
button_last_debounce_time_1 = 0
button_last_debounce_time_2 = 0
button_last_debounce_time_3 = 0

button_last_state_0 = 1
button_last_state_1 = 1
button_last_state_2 = 1
button_last_state_3 = 1

button_count_0 = 0
button_count_1 = 0
button_count_2 = 0
button_count_3 = 0

flag_0 = 0
flag_1 = 0
flag_2 = 0
flag_3 = 0

time_1_0 = 0
time_1_1 = 0
time_1_2 = 0
time_1_3 = 0
time_2_0 = 0
time_2_1 = 0
time_2_2 = 0
time_2_3 = 0

def button_debounce(Number):
    global button_last_state_0,button_last_state_1,button_last_state_2,button_last_state_3 
    global button_last_debounce_time_0 ,button_last_debounce_time_1,button_last_debounce_time_2,button_last_debounce_time_3
    global button_count_0,button_count_1,button_count_2,button_count_3
    global flag_0 ,flag_1,flag_2,flag_3
    global time_1_0,time_1_1,time_1_2,time_1_3
    global time_2_0,time_2_1,time_2_2,time_2_3
    
    button_current_state = pcf.pin(Number)
    
    if utime.ticks_ms() - button_last_debounce_time_1 > 200:
        if button_current_state == 0  and  button_last_state_1 == 1 and Number == 1 :
            button_last_debounce_time_1 = utime.ticks_ms()
            button_last_state_1 = 0
            if flag_1 == 0:
                flag_1 = 1
                time_1_1 = utime.ticks_ms()
                return button_last_state_1        
        elif button_current_state == 1 and button_last_state_1 == 0 and Number == 1:
             button_last_state_1 = 1
             button_count_1 += 1
             if flag_1 == 1:
                 flag_1 = 0
                 time_2_1 = utime.ticks_ms()
                 return button_last_state_1
                
        elif button_current_state == 0  and  button_last_state_2 == 1 and Number == 2:
            button_last_debounce_time_2 = utime.ticks_ms()
            button_last_state_2 = 0
            if flag_2 == 0:
                flag_2 = 1
                time_1_2 = utime.ticks_ms()
                return button_last_state_2
        elif button_current_state == 1 and button_last_state_2 == 0 and Number == 2 :
             button_last_state_2 = 1
             button_count_2 += 1
             if flag_2 == 1:
                 flag_2 = 0
                 time_2_2 = utime.ticks_ms()
                 return button_last_state_2
    
        elif button_current_state == 0  and button_last_state_3 == 1 and Number == 3:
            button_last_debounce_time_3 = utime.ticks_ms()
            button_last_state_3 = 0
            if flag_3 == 0:
                flag_3 = 1
                time_1_3 = utime.ticks_ms()
                return button_last_state_3
        elif button_current_state == 1  and button_last_state_3 == 0 and Number == 3:
            button_last_state_3 = 1
            button_count_3 += 1
            if flag_3 == 1:
                flag_3 = 0
                time_2_3 = utime.ticks_ms()
                return button_last_state_3
            
        elif button_current_state == 0  and  button_last_state_0 == 1 and Number == 0:
            button_last_debounce_time_0 = utime.ticks_ms()
            button_last_state_0 = 0
            if flag_0 == 0:
                flag_0 = 1
                time_1_0 = utime.ticks_ms()
                return button_last_state_0
        elif button_current_state == 1  and  button_last_state_0 == 0 and Number == 0:
            button_last_state_0 = 1
            button_count_0 += 1
            if flag_0 == 1:
                flag_0 = 0
                time_2_0 = utime.ticks_ms()
                return button_last_state_0
            