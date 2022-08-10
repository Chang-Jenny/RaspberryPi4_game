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
FONT = ('Arial', 25, 'normal')
TARGET_URL = 'localhost'

game_over=0
# 搖桿根據回傳方向呼叫不同函數去操控角色
def joy():
    while True:
        x, y, s=total.joystickNum()
        print("X : {}  Y : {}  Switch : {}".format(x,y,s))
        receive=total.position(x,y,s)
        print(receive)
        print('back_joy:',back)
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
    # 定義按鈕
    global btn_right, btn_left, btn_shoot
    btn_right=35
    btn_left=37
    btn_shoot=15
    GPIO.setup(btn_right, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(btn_left, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(btn_shoot, GPIO.IN, GPIO.PUD_UP)
    if(count==0):
        GPIO.add_event_detect(btn_shoot, GPIO.FALLING, callback=my_callback_shoot, bouncetime=200)
# 蜂鳴器函數
music=[262, 294, 330]
tempo=[0.5, 0.25, 0.5]
def voice(music, tempo):
    for i in range(0, len(music)):
        total.play(music[i], tempo[i])

def my_callback_shoot(channel):
    print("shoot button pressed!")
    shoot()

def leftMove():
    global X
    X-=planeSpeed
def rightMove():
    global X
    X+=planeSpeed
def upMove():
    global Y
    Y+=planeSpeed
def downMove():
    global Y
    Y-=planeSpeed
def uprightMove():
    global X, Y
    X+=planeSpeed
    Y+=planeSpeed
def upleftMove():
    global X, Y
    X-=planeSpeed
    Y+=planeSpeed
def downrightMove():
    global X, Y
    X+=planeSpeed
    Y-=planeSpeed
def downleftMove():
    global X, Y
    X-=planeSpeed
    Y-=planeSpeed
def shoot():
    global s, bullet_Y
    bullet_Y+=bulletSpeed
    s=1
    music=[659]
    tempo=[0.25]
    thread = threading.Thread(target=voice,args=(music,tempo))
    thread.start()
        
# 遊戲畫面及數值設置
def drawDefine(person_X, person_Y, b_X, b_Y, uid_decimal):
    global ID
    ID=uid_decimal
    print(ID)
    
    global X, Y, bullet_X, bullet_Y
    X=person_X
    Y=person_Y
    bullet_X=b_X
    bullet_Y=b_Y
    
    global bulletSpeed, enemySpeed, planeSpeed, enemyNum
    global bulletPower, s, score, stop
    global plane, bullet, enemy
    bulletSpeed = 120
    enemySpeed = 10
    planeSpeed = 20
    enemyNum = 5 #enemy數量5
    bulletPower = 40 #威力大小40
    s = 0 #是否發射子彈
    score = 0
    stop = 0
    plane = t.Pen()
    bullet = t.Pen()
    enemy = []
    for i in range(enemyNum):
        enemy.append(t.Pen())

    t.addshape('img/plane.gif')
    t.addshape('img/enemy.gif')
    t.addshape('img/bullet.gif')
    t.addshape('img/explosion.gif')
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
        print('countdown_num:',time)
        print("game_over_count:",game_over)
        screenTime.ontimer(lambda: countdown(time - 1), 1000)
    elif(game_over==0 and time==0):
        print("back:",back)
        stop=1
        back=1
        r = requests.get('http://{0}/gameGET.php?playerID={1}&level={2}&score={3}'.format(TARGET_URL,ID,"1",score))
        print("時間Server Return Code :", r.status_code)
        print(ID)
        for k in range(0,7):
            GPIO.output(seg[k], light[0][k])
        turtle_time.hideturtle()
        # GPIO.cleanup()
        t.clearscreen()
        print("after_clear_screen")
        t.bgpic('img/timesup.png') 
        lcd.cursor_pos=(0,0)
        lcd.write_string("___TIME's_UP____")
        music=[784]
        tempo=[0.5]
        thread = threading.Thread(target=voice,args=(music,tempo))
        thread.start()
        # ==========印出排行榜=================
        import query
        query.board(1)
        
    
# 遊戲初始值的設定
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
    global game_over
    game_over=0
    width,height = 600,720
    screen.setup(width,height)
    screen.bgpic('img/bg_star.png') #game1背景圖
    screen.bgcolor('black')
    t.colormode(255)

    for i in enemy:
        i.speed(0) #最快
        i.penup()
        i.setheading(-90)
        i.goto(random.randint(-280,280),random.randint(320,400))
        i.shape('img/enemy.gif')
    
    plane.penup()   
    plane.setheading(90)
    plane.goto(0,-250)
    plane.shape('img/plane.gif')
    bullet.speed(0)
    bullet.penup()
    bullet.hideturtle()
    bullet.setheading(90)
    bullet.goto(0,-250)
    bullet.shape('img/bullet.gif')
    screen.bgcolor('white')

        
# 遊戲畫面
def stageFirst():
    # 以thread執行搖桿
    joythread=threading.Thread(target=joy)
    joythread.start()
    global back,stop
    
    # 開始倒數
    if stop == 0: 
        countdown(15)

    while back==0: # 如果主角碰到enemy則back=1回去感應卡
        global s, score
        global bullet_Y
        plane.setx(X)
        plane.sety(Y)
        if stop == 1: # 判斷時間到了嗎(到了等於1)
            turtle_time.penup()
            turtle_time.hideturtle()
            print("if stop==1 countdown(0)")
        
        if s==0: #未發射子彈
            bullet_Y=-250
            bullet.goto(plane.xcor(),plane.ycor()-20) #不發射子彈
        if s==1:
            bullet.showturtle()
            bullet.setx(X)
            bullet.sety(bullet.ycor()+bulletSpeed)

        if bullet.ycor() > 360: # 子彈超出windows
            bullet.hideturtle()
            s = 0 #重設定為未發射

        # 設定enemy狀態
        for i in enemy:
            i.shape('img/enemy.gif')
            i.goto(i.xcor(),i.ycor()-enemySpeed)

            # 子彈打到enemy
            if i.distance(bullet) < bulletPower:
                # 先設定為爆炸
                i.shape('img/explosion.gif')
                # 蜂鳴器發出音效
                music=[587,880]
                tempo=[0.25,0.25]
                thread = threading.Thread(target=voice,args=(music,tempo))
                thread.start()
                # 重新設定enemy狀態
                i.goto(random.randint(-200,200),random.randint(350,400)) #使enemy重新回到出發點開始降落
                i.shape('img/enemy.gif')
                bullet.hideturtle()

                score = score + 1
                print('score=',score)
                lcd.clear()
                lcd.cursor_pos=(0, 0)
                lcd.write_string(str(ID))
                lcd.cursor_pos=(1, 0)
                lcd.write_string("score: "+str(score))
                s = 0
                
            # enemy超出window的bottom
            if i.ycor() < -360:
                i.goto(random.randint(-200,200),random.randint(350,400))

            # check 碰撞 
            if i.distance(plane)<50: #enemy和plane的distance<50
                stop = 1 # 讓時間停止計算
                turtle_time.penup()
                turtle_time.clear()
                print('game over')
                global game_over
                game_over = 1
                lcd.clear()
                lcd.cursor_pos=(0,0)
                lcd.write_string("___GAME_OVER____")
                lcd.cursor_pos=(1,0)
                lcd.write_string("score: "+str(score))
                
                back=1 #要回去while迴圈重新感應卡
                t.clearscreen()
                t.bgpic('img/gameover.png') #gameover背景圖
                if(back==1):
                    music=[784,698,658,587]
                    tempo=[0.25,0.25,0.25,0.5]
                    thread = threading.Thread(target=voice,args=(music,tempo))
                    thread.start()