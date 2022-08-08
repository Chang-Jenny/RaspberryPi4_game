import os
import turtle as t
from turtle import Screen, Turtle
from time import time

import game1, game2, game3
FONT = ('Arial', 25, 'normal')
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

game_over=0
count_1=0
count_2=0
count_3=0

IR_PIN=12 #IR pin in physical Pin 12 
KEY_1=0xff30cf
KEY_2=0xff18e7
KEY_3=0xff7a85
KEY_exit=0xff629d

def setup():
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def binary_aquire(pin, duration):
    # aquires data as quickly as possible
    t0 = time()
    results = []
    while (time() - t0) < duration:
        results.append(GPIO.input(pin))
    return results
def on_ir_receive(pinNo, bouncetime=150):
    # when edge detect is called (which requires less CPU than constant
    # data acquisition), we acquire data as quickly as possible
    data = binary_aquire(pinNo, bouncetime/1000.0)
    if len(data) < bouncetime:
        return
    rate = len(data) / (bouncetime / 1000.0)
    pulses = []
    i_break = 0
    # detect run lengths using the acquisition rate to turn the times in to microseconds
    for i in range(1, len(data)):
        if (data[i] != data[i-1]) or (i == len(data)-1):
            pulses.append((data[i-1], int((i-i_break)/rate*1e6)))
            i_break = i
    # decode ( < 1 ms "1" pulse is a 1, > 1 ms "1" pulse is a 1, longer than 2 ms pulse is something else)
    # does not decode channel, which may be a piece of the information after the long 1 pulse in the middle
    outbin = ""
    for val, us in pulses:
        if val != 1:
            continue
        if outbin and us > 2000:
            break
        elif us < 1000:
            outbin += "0"
        elif 1000 < us < 2000:
            outbin += "1"
    try:
        return int(outbin, 2)
    except ValueError:
        # probably an empty code
        return None
def destroy():
    GPIO.cleanup()

# 選擇遊戲編號
# 判斷讀取到的值code等於哪個KEY，並呼叫該遊戲的函數
def level_init(uid_decimal):
    lcd.clear()
    lcd.cursor_pos=(0,0)
    lcd.write_string(str(uid_decimal))
    lcd.cursor_pos=(1,0)
    lcd.write_string("__CHOOSE_GAME___")
    setup()
    X=0 
    Y=-250
    bullet_X=0
    bullet_Y=-250
    uid=uid_decimal
    global count_1
    global count_2
    global count_3
    global game_over
    
    while True:
        try:
            while True:
                print("Starting IR Listener")
                print("Waiting for signal")
                GPIO.wait_for_edge(IR_PIN, GPIO.FALLING)
                code = on_ir_receive(IR_PIN)
                print(code)
                if (code==KEY_1):
                    print("remote control press1")
                    lcd.clear()
                    lcd.cursor_pos=(0,0)
                    lcd.write_string(str(uid_decimal))
                    lcd.cursor_pos=(1,0)
                    lcd.write_string("_____GAME_1______")
                    game1.drawDefine(X, Y, bullet_X, bullet_Y, uid)
                    game1.conponentDefine(count_1)
                    count_1+=1
                    game1.start()
                    game1.stageFirst()
                    game_over=0
                    print("game_over:",game_over)
                    break
                elif (code==KEY_2):
                    print("remote control press2")
                    X=200
                    Y=250
                    lcd.clear()
                    lcd.cursor_pos=(0,0)
                    lcd.write_string(str(uid_decimal))
                    lcd.cursor_pos=(1,0)
                    lcd.write_string("_____GAME_2______")
                    game2.drawDefine(X, Y, uid)
                    game2.conponentDefine(count_2)
                    count_2+=1
                    game2.start()
                    game2.stageFirst()
                    game_over=0
                    print("game_over:",game_over)
                    break
                elif (code==KEY_3): 
                    print("remote control press3")
                    lcd.clear()
                    lcd.cursor_pos=(0,0)
                    lcd.write_string(str(uid_decimal))
                    lcd.cursor_pos=(1,0)
                    lcd.write_string("_____GAME_3______")
                    game3.drawDefine(X, Y, uid)
                    game3.conponentDefine(count_3)
                    count_3+=1
                    game3.start()
                    game3.stageFirst() 
                    game_over=0
                    print("game_over:",game_over)
                    break
                elif (code==KEY_exit): 
                    lcd.clear()
                    lcd.cursor_pos=(0,0)
                    lcd.write_string(str(uid_decimal))
                    lcd.cursor_pos=(1,0)
                    lcd.write_string("_____NEXT_______")
                    break
                else:
                    print("Invalid code")
            print("end_of_game123 and break the while_")
            break
        except KeyboardInterrupt:
            # User pressed CTRL-C
            # Reset GPIO settings
            print("Ctrl-C pressed!")
        except RuntimeError:
            # this gets thrown when control C gets pressed
            # because wait_for_edge doesn't properly pass this on
            print('runtime error')
            pass
        print("Quitting")

# 執行do()選擇遊戲
def do(uid_decimal):
    t.clearscreen()
    uid=uid_decimal
    global count_1,count_2,count_3
    screen = t.Screen()
    width,height = 600,720
    screen.setup(width,height)
    screen.bgpic('img/main.png') #遊戲說明背景圖
    screen.bgcolor('white')
    t.colormode(255)  

    level_init(uid)
    print("count_1: ", count_1)
    print("count_2: ", count_2)
    print("count_3: ", count_3)
