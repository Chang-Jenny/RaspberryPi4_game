import time
import RPi.GPIO as GPIO
import mfrc522 as MFRC522
import signal
import threading
import requests
import subtract, playgame
# 在LCD印出提示使用者感應卡片
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
lcd.clear()
lcd.cursor_pos=(0, 0)
lcd.write_string("____GA_M___E____")
lcd.cursor_pos=(1, 0)
lcd.write_string("___HOLD_A_TAG___")

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# 設定RFID使用spi.open(0,0)
import spidev
spi = spidev.SpiDev()
spi.open(0,0)
TARGET_URL = 'localhost'

# set LED
LED0 = 7   
LED1 = 11
buzzer = 16

# set output
GPIO.setup(LED0,GPIO.OUT)
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

# 蜂鳴器播放音效
def play(pitch, sec):
    half_pitch = (1 / pitch) / 2
    t = int(pitch * sec)
    for i in range(t):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(half_pitch)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(half_pitch)
def voice(music, tempo):
    for i in range(0, len(music)):
        play(music[i], tempo[i])     
        
# 是否結束讀取
continue_reading = True
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Hold a tag near the reader")
print("Press Ctrl-C to stop.")

# 利用again判斷是第幾次執行read.py的函式
again=0
# chcek the UID
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        print("UID length: ",len(uid))
        uid_len=len(uid)-1
        uid_decimal=0;
        for x in range(0,uid_len):
                uid_decimal = uid_decimal + uid[x]*256**(uid_len-1-x)
        print("Card read UID decimal: "+str(uid_decimal))
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        # 利用先前作業寫編號8為名字印出在LCD上
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # check OK?
        if status == MIFAREReader.MI_OK:
            rdData = MIFAREReader.MFRC522_Read(8)
            name=""
            for i in range(0,16):
                temp = chr(rdData[i])
                name+=temp
            print(name)
            lcd.clear()
            lcd.cursor_pos=(0, 0)
            lcd.write_string(name)
            GPIO.output(LED0,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED0,GPIO.LOW)
        else:
            print ("Authentication error")
            GPIO.output(LED1,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED1,GPIO.LOW)
            
        # 讀取卡片餘額
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12, key, uid)
        if status == MIFAREReader.MI_OK:
            rdData = MIFAREReader.MFRC522_Read(12)
            money=""
            for i in range(0,16):
                temp = chr(rdData[i])
                money+=temp
            print("Now money:",end=" ")
            print(money,"\n")
            
            # 要寫回去RFID，呼叫subtract中的sub函式判斷是否小於0並組合數字
            data=subtract.sub(money)
            MIFAREReader.MFRC522_Write(12, data)
            rd = MIFAREReader.MFRC522_Read(12)
            re=""
            for i in range(0,16):
                temp = chr(rd[i])
                re+=temp
            judge=int(money)
            lcd.cursor_pos=(1,0)
            lcd.write_string("money: "+re)
            
            # 檢查是否大於0元
            if(judge!=0):
                buzzer = 16
                GPIO.setup(buzzer,GPIO.OUT)
                print("write back:",end=" ")
                print(re,"\n")
                MIFAREReader.MFRC522_StopCrypto1()
                # 將扣款紀錄寫到資料庫中
                r = requests.get('http://{0}/LogRecord_GET.php?NAME={1}&ID={2}'.format(TARGET_URL,name,uid_decimal))
                print("Server Return Code :", r.status_code)
                time.sleep(1)

                # 呼叫函式繼續執行
                playgame.playtest(name, uid_decimal)
                # 重新設定spi.open(0,0)，因為MCP3008改設為spi.open(0,1)
                spi.open(0,0)
                print("again: ",again)
                again+=1
                if(again>0):
                    print("Hold a tag near the reader")
                    print("Press Ctrl-C to stop.")
                    
            # 若餘額小於等於0則跳出結束read.py，提醒使用者執行write.py
            # 蜂鳴器以thread發出提醒
            # LED閃爍
            else: 
                for i in range(3):
                    music=[659, 659, 659]
                    tempo=[0.25, 0.25, 0.25]
                    thread = threading.Thread(target=voice,args=(music,tempo))
                    thread.start()
                    GPIO.output(LED1,GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(LED1,GPIO.LOW)
                    time.sleep(0.5)
                    
                continue_reading = False
                lcd.clear()
                break
            
        else:
            print ("Authentication error")
            GPIO.output(LED1,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED1,GPIO.LOW)
            time.sleep(0.5)
            
# 結束前在LCD上印字
lcd.clear()
lcd.cursor_pos=(0, 0)
lcd.write_string("___THANK_YOU____")
lcd.cursor_pos=(1, 0)
lcd.write_string("HAVE A GOOD DAY.") 
time.sleep(2)
lcd.clear()
GPIO.cleanup()
            