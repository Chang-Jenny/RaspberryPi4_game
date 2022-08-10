import threading
import RPi.GPIO as GPIO
import requests
import turtle as t
from turtle import Screen, Turtle
import os
import smbus
import sys
import time
import random
import total

sys.modules['smbus'] = smbus
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
TARGET_URL = 'localhost'
FONT = ('Arial', 25, 'normal')

def joy():
    while True:
        x, y, s=total.joystickNum()
        print("X : {}  Y : {}  Switch : {}".format(x,y,s))
        receive=total.position(x,y,s)
        print(receive)
        if receive=="UP":
            upMove()
        elif receive=="DOWN":
            downMove()
        elif receive=="RIGHT":
            rightMove()
        elif receive=="LEFT":
            leftMove()
        elif receive=="UP.RIGHT":
            uprightMove()
        elif receive=="UP.LEFT":
            upleftMove()
        elif receive=="DOWN.RIGHT":
            downrightMove()
        elif receive=="DOWN.LEFT":
            downleftMove()
        else: pass
        time.sleep(delay)
        if back==1:
            break

# 定義元件
def conponentDefine(count):
    global spi, swt_channel, vrx_channel, vry_channel, delay
    global seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g
    global light,seg
    global buzzer
    
    spi, swt_channel, vrx_channel, vry_channel, delay, seg_a, seg_b, seg_c, seg_d, seg_e, seg_f, seg_g, light, seg, buzzer=total.totalDefine()
    GPIO.setmode(GPIO.BOARD)

# 蜂鳴器
music=[262, 294, 330]
tempo=[0.5, 0.25, 0.5]
def voice(music, tempo):
    for i in range(0, len(music)):
        total.play(music[i], tempo[i])

# temp變數為改變潛水人的面向(左或右)
def leftMove():
    global X, temp
    X-=planeSpeed
    temp='img/person.gif'
def rightMove():
    global X, temp
    X+=planeSpeed
    temp='img/personinverse.gif'
def upMove():
    global Y
    Y+=planeSpeed
def downMove():
    global Y
    Y-=planeSpeed
def uprightMove():
    global X, Y, temp
    X+=planeSpeed
    Y+=planeSpeed
    temp='img/personinverse.gif'
def upleftMove():
    global X, Y, temp
    X-=planeSpeed
    Y+=planeSpeed
    temp='img/person.gif'
def downrightMove():
    global X, Y, temp
    X+=planeSpeed
    Y-=planeSpeed
    temp='img/personinverse.gif'
def downleftMove():
    global X, Y, temp
    X-=planeSpeed
    Y-=planeSpeed
    temp='img/person.gif'

# 畫面及數值設置
def drawDefine(person_X, person_Y, uid_decimal):
    global ID
    ID=uid_decimal
    print(ID)
    
    global temp
    temp="img/person.gif"

    global X, Y
    X=person_X
    Y=person_Y
    global enemySpeed, planeSpeed, enemyNum
    global score, stop
    global plane, bullet, enemy
    enemySpeed = 20
    planeSpeed = 50
    enemyNum = 5 #enemy數量5
    score = 0
    stop = 0
    plane = t.Pen()
    bullet = t.Pen()
    enemy = []
    for i in range(enemyNum):
        enemy.append(t.Pen())

    t.addshape('img/person.gif')
    t.addshape('img/personinverse.gif')
    t.addshape('img/fish.gif')
    
    global turtle_time
    turtle_time = Turtle()
    turtle_time.hideturtle()

# 倒數計時
# 若Time's up則發送request
# 使用GET的方式給gameGET.php，包含玩家ID、遊戲編號及分數
def countdown(time):
    global stop, back, seg, light
    turtle_time.clear()
    if time > 0 and back==0:
        turtle_time.penup()
        turtle_time.goto(250,-280)
        for j in range(0,7):
            GPIO.output(seg[j], light[time][j])
        turtle_time.write(time, align='center', font=FONT)
        screenTime.ontimer(lambda: countdown(time - 1), 1000)
    else:
        stop=1
        back=1
        request = requests.get('http://{0}/gameGET.php?playerID={1}&level={2}&score={3}'.format(TARGET_URL,ID,"2",score))
        print("時間Server Return Code :", request.status_code)
        print(ID)
        for k in range(0,7):
            GPIO.output(seg[k], light[0][k])
        turtle_time.hideturtle()
        t.clearscreen()
        t.bgpic('img/timesup.png') 
        lcd.cursor_pos=(0,0)
        lcd.write_string("___TIME's_UP____")
        music=[784]
        tempo=[0.5]
        thread = threading.Thread(target=voice,args=(music,tempo))
        thread.start()
        # ==========印出排行榜=================
        import query
        query.board(2)

# 遊戲初始設置
def start():
    screen = t.Screen()
    global screenTime
    screenTime = Screen()
    global stop #時間等於0
    stop=0
    global back #回去主頁
    back=0
    global score #分數
    score=0
    width,height = 600,720
    screen.setup(width,height)
    screen.bgpic('img/bg_ocean.png')#背景圖
    screen.bgcolor('black')
    t.colormode(255)

    for i in enemy:
        i.speed(0)#最快
        i.penup()
        i.setheading(-90)
        i.goto(random.randint(-200,250),random.randint(-320,150))
        i.shape('img/fish.gif')
    
    plane.penup()
    plane.setheading(90)
    plane.goto(X,Y)
    plane.shape('img/person.gif')
    screen.bgcolor('white')
    
    # global stop
    if stop == 0:
        countdown(15)

# 遊戲畫面
def stageFirst():
    joythread=threading.Thread(target=joy)
    joythread.start()
    global back
    while back==0:
        global stop, s, score, temp
        plane.setx(X)
        plane.sety(Y)
        if stop == 1:
            turtle_time.penup()
            turtle_time.hideturtle()
            
        plane.shape(temp)

        # 設定enemy的狀態
        for i in enemy:
            i.shape('img/fish.gif')
            i.goto(i.xcor()-enemySpeed,i.ycor())
                
            # enemy超出windows的bottom
            if i.xcor() < -300:
                i.goto(random.randint(250,280),random.randint(-320,280))

            # check 碰撞，潛水人抓到章魚則加分
            if i.distance(plane)<50: # enemy和plane的distance<50
                thread = threading.Thread(target=voice,args=(music,tempo))
                thread.start()
                # 重新設置章魚的狀態
                i.goto(random.randint(250,280),random.randint(-320,280)) #使enemy重新回到出發點開始降落
                bullet.hideturtle()
                score = score + 1
                print('score=',score)
                lcd.clear()
                lcd.cursor_pos=(0, 0)
                lcd.write_string(str(ID))
                lcd.cursor_pos=(1, 0)
                lcd.write_string("score: "+str(score))