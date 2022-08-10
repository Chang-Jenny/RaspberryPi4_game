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
        GPIO.add_event_detect(btn_right, GPIO.FALLING, callback=my_callback_right, bouncetime=200)
        GPIO.add_event_detect(btn_left, GPIO.FALLING, callback=my_callback_left, bouncetime=200)
    

def voice(music, tempo):
    for i in range(0, len(music)):
        total.play(music[i], tempo[i])
        
def my_callback_right(channel):
    print("right button pressed!")
    rightMove()
def my_callback_left(channel):
    print("left button pressed!")
    leftMove()

def leftMove():
    global X
    X-=planeSpeed
    music=[392]
    tempo=[0.25]
    thread = threading.Thread(target=voice,args=(music,tempo))
    thread.start()
def rightMove():
    global X
    X+=planeSpeed
    music=[392]
    tempo=[0.25]
    thread = threading.Thread(target=voice,args=(music,tempo))
    thread.start()

# 設置畫面及數值
def drawDefine(person_X, person_Y, uid_decimal):
    global ID
    ID=uid_decimal
    print(ID)
    
    global X, Y
    X=person_X
    Y=person_Y
    
    global enemySpeed, planeSpeed, enemyNum, doublemoneyNum
    global score, stop
    global plane, enemy, money, doublemoney
    enemySpeed = 20
    planeSpeed = 20
    enemyNum = 3 #減分數量
    moneyNum = 5 #加一分
    doublemoneyNum = 1 #加二分
    score = 0
    stop = 0
    
    plane = t.Pen()
    enemy = []
    for i in range(enemyNum):
        enemy.append(t.Pen())
    money = []
    for i in range(moneyNum):
        money.append(t.Pen())
    doublemoney=[]
    for i in range(doublemoneyNum):
        doublemoney.append(t.Pen())

    t.addshape('img/stand.gif')
    t.addshape('img/coin.gif')
    t.addshape('img/bomb.gif')
    t.addshape('img/money.gif')
    
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
        print('countdown_num:',time)
        print("game_over_count:",game_over)
    elif(game_over==0 and time==0):
        print("back:",back)
        stop=1
        back=1
        r = requests.get('http://{0}/gameGET.php?playerID={1}&level={2}&score={3}'.format(TARGET_URL,ID,"3",score))
        print("時間Server Return Code :", r.status_code)
        print(ID)
        for k in range(0,7):
            GPIO.output(seg[k], light[0][k])
        turtle_time.hideturtle()
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
        query.board(3)

def start():
    screen = t.Screen()
    global screenTime
    screenTime = Screen()
    global stop # 時間等於0
    stop=0
    global back # 回去主頁
    back=0
    global score # 分數
    score=0
    global game_over
    game_over=0
    width,height = 600,720
    screen.setup(width,height)
    screen.bgpic('img/bg_bluesky.png') # 背景圖
    screen.bgcolor('white')
    t.colormode(255)

    for i in enemy:
        i.speed(0) # 最快
        i.penup()
        i.setheading(-90)
        i.goto(random.randint(-280,280),random.randint(320,400))
        i.shape('img/bomb.gif')
    
    for i in money:
        i.speed(0)#最快
        i.penup()
        i.setheading(-90)
        i.goto(random.randint(-280,280),random.randint(320,400))
        i.shape('img/coin.gif')
        
    for i in doublemoney:
        i.speed(0)#最快
        i.penup()
        i.setheading(-90)
        i.goto(random.randint(-280,280),random.randint(320,400))
        i.shape('img/money.gif')
        
    plane.penup()   
    plane.setheading(90)
    plane.goto(0,-250)
    plane.shape('img/stand.gif')

# 遊戲畫面
def stageFirst():
    global back,stop

    if stop == 0: 
        countdown(15)
    
    while back==0:
        global score
        plane.setx(X)
        plane.sety(Y)
        if stop == 1:
            turtle_time.penup()
            turtle_time.hideturtle()
        
        # 設定enemy狀態
        for i in enemy:
            i.shape('img/bomb.gif')
            i.goto(i.xcor(),i.ycor()-random.randint(20,50))
                
            #enemy超出windows的bottom
            if i.ycor() < -360:
                i.goto(random.randint(-200,200),random.randint(350,400))
                
            # check 碰撞
            # 如果分數小於0則game over
            if i.distance(plane)<50: #enemy和plane的distance<50
                music=[294]
                tempo=[0.25]
                thread = threading.Thread(target=voice,args=(music,tempo))
                thread.start()
                i.goto(random.randint(250,280),random.randint(-320,280)) #使enemy重新回到出發點開始降落
                score = score- 1
                print('score=',score)
                lcd.clear()
                lcd.cursor_pos=(0, 0)
                lcd.write_string(str(ID))
                lcd.cursor_pos=(1, 0)
                lcd.write_string("score: "+str(score))
                if score<0:
                    stop = 1
                    turtle_time.penup()
                    turtle_time.clear()
                    print('game over')
                    global game_over
                    game_over = 1

                    lcd.cursor_pos=(0,0)
                    lcd.write_string("___GAME_OVER____")
                    print ('game over')
                    back=1
                    t.clearscreen()
                    if(back==1):
                        music=[784,698,658,587]
                        tempo=[0.25,0.25,0.25,0.5]
                        thread = threading.Thread(target=voice,args=(music,tempo))
                        thread.start()
                        t.bgpic('img/gameover.png')
                
                
        # 加分金幣的狀態設定
        for i in money:
            i.shape('img/coin.gif')
            i.goto(i.xcor(),i.ycor()-random.randint(40,60))
            if i.ycor() < -360: #enemy超出windows的bottom
                i.goto(random.randint(-200,200),random.randint(350,400))
                
            # check 碰撞 
            if i.distance(plane)<50: # money和plane的distance<50
                music=[659]
                tempo=[0.25]
                thread = threading.Thread(target=voice,args=(music,tempo))
                thread.start()
                i.goto(random.randint(250,280),random.randint(-320,280)) #使enemy重新回到出發點開始降落
                score = score + 1
                print('score=',score)
                lcd.clear()
                lcd.cursor_pos=(0, 0)
                lcd.write_string(str(ID))
                lcd.cursor_pos=(1, 0)
                lcd.write_string("score: "+str(score))
        
        # 加分福袋的狀態設定        
        for j in doublemoney:
            j.shape('img/money.gif')
            j.goto(j.xcor(),j.ycor()-random.randint(10,30))
            if j.ycor() < -360: #enemy超出windows的bottom
                j.goto(random.randint(-200,200),random.randint(350,400))
                
            # check 碰撞 
            if j.distance(plane)<50: # money和plane的distance<50
                music=[880,988]
                tempo=[0.25,0.5]
                thread = threading.Thread(target=voice,args=(music,tempo))
                thread.start()
                
                # 隨機重新設置位置
                j.goto(random.randint(250,280),random.randint(280,300)) #使enemy重新回到出發點開始降落
                
                # 分數加2
                score = score + 2
                print('score=',score)
                lcd.clear()
                lcd.cursor_pos=(0, 0)
                lcd.write_string(str(ID))
                lcd.cursor_pos=(1, 0)
                lcd.write_string("score: "+str(score))