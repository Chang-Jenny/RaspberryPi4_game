import RPi.GPIO as GPIO
import turtle as t
from turtle import Screen, Turtle
import os
import smbus
import sys
import time
sys.modules['smbus'] = smbus
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# 定義一些不會改變的函數，避免重複過多
# 以return回傳
def totalDefine():
    GPIO.setmode(GPIO.BOARD)
    # 搖桿
    import spidev
    global spi, swt_channel, vrx_channel, vry_channel, delay
    spi = spidev.SpiDev()
    spi.open(0,1)
    spi.max_speed_hz=1000000
    swt_channel = 0
    vrx_channel = 1
    vry_channel = 2
    delay = 0.5
    
    global seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g
    global light,seg
    global buzzer
    
    # 七段顯示器
    seg_a=38
    seg_b=40
    seg_c=33
    seg_d=31
    seg_e=29
    seg_f=36
    seg_g=32
    GPIO.setup(seg_a,GPIO.OUT)
    GPIO.setup(seg_b,GPIO.OUT)
    GPIO.setup(seg_c,GPIO.OUT)
    GPIO.setup(seg_d,GPIO.OUT)
    GPIO.setup(seg_e,GPIO.OUT)
    GPIO.setup(seg_f,GPIO.OUT)
    GPIO.setup(seg_g,GPIO.OUT)
    # buzzer
    buzzer = 16
    GPIO.setup(buzzer,GPIO.OUT)
    light=[[1,1,1,1,1,1,0], [0,1,1,0,0,0,0], [1,1,0,1,1,0,1], [1,1,1,1,0,0,1], 
    [0,1,1,0,0,1,1], [1,0,1,1,0,1,1], [1,0,1,1,1,1,1], [1,1,1,0,0,0,0], 
    [1,1,1,1,1,1,1], [1,1,1,1,0,1,1], [1,1,1,0,1,1,1], [0,0,1,1,1,1,1], 
    [1,0,0,1,1,1,0], [0,1,1,1,1,0,1], [1,0,0,1,1,1,1],[1,0,0,0,1,1,1]]
    seg=[ seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g]
    # 初始值
    for i in range(0,7):
        GPIO.output(seg[i], light[0][i])
    return spi, swt_channel, vrx_channel, vry_channel, delay, seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g, light,seg,buzzer

# 蜂鳴器   
def play(pitch, sec):
    half_pitch = (1 / pitch) / 2
    t = int(pitch * sec)
    for i in range(t):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(half_pitch)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(half_pitch)
        
# 搖桿
def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data
def joystickNum():
    vrx_pos = ReadChannel(vrx_channel)
    vry_pos = ReadChannel(vry_channel)
    swt_val = ReadChannel(swt_channel)
    return (vrx_pos, vry_pos, swt_val)

# 搖桿判斷操控方向並回傳自己定義好的上下左右或斜的方向
def position(a,b,s):
    printPos=""
    if a>=0 and a<100:
        if b>200 and b<750:
            printPos="UP"
        elif b>=0 and b<200:
            printPos="UP.RIGHT"
        elif b>750 and b<1024:
            printPos="UP.LEFT"
    elif a>300 and a<600:
        if b>=0 and b<200:
            printPos="RIGHT"
        elif b>900 and b<1024:
            printPos="LEFT"
    elif a>900 and a<1024:
        if b>200 and b<750:
            printPos="DOWN"
        elif b>=0 and b<200:
            printPos="DOWN.RIGHT"
        elif b>750 and b<1024:
            printPos="DOWN.LEFT"
    elif a>100 and a<300:
        if b>=0 and b<20:
            printPos="UP.RIGHT"
        elif b>1004 and b<1024:
            printPos="UP.LEFT"
    elif a>600 and a<900:
        if b>=0 and b<20:
            printPos="DOWN.RIGHT"
        elif b>1004 and b<1024:
            printPos="DOWN.LEFT"
    if s<700:
        printPos="PRESSED"
    return(printPos)