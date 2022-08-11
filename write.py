#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import mfrc522 as MFRC522
import signal
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
lcd.clear()
lcd.cursor_pos=(0,0)
lcd.write_string("...ADD MONEY....")
continue_reading = True
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

money=str(input("Input a value: "))

# Welcome message
print("Hold a tag near the reader")
print("Press Ctrl-C to stop.")


# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
        
        
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        # print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        print("UID length: ",len(uid))
        uid_len=len(uid)-1
        uid_decimal=0;
        for x in range(0,uid_len):
                uid_decimal = uid_decimal + uid[x]*256**(uid_len-1-x)
        print("Card read UID decimal: "+str(uid_decimal))
        
        
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12, key, uid)
        print("\n")
        
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            # Variable for the data to write
            
            # 印出餘額
            rdData = MIFAREReader.MFRC522_Read(12)
            print ("餘額: ", end=" ")
            remains=""
            for i in range(0,16):
                temp = chr(rdData[i])
                remains+=temp
            print(remains,"\n")
            lcd.clear()
            lcd.cursor_pos=(0,0)
            lcd.write_string("you have: "+remains)
            
            # 加總後的金額
            cal=int(money)+int(remains)
            temp=str(cal)
            print("total: ",temp)
            lcd.cursor_pos=(1, 0)
            lcd.write_string("total money: "+temp)
            
            # 再寫回去RFID
            data=[]
            for i in range(0, len(temp)):
               data.append(ord(temp[i]))
            # temp=16-len(money)
            for i in range(len(temp), 16):
                data.append(ord(" "))

            MIFAREReader.MFRC522_Read(12)
            MIFAREReader.MFRC522_Write(12, data)
            print("\n")
            print("It now looks like this:")
            # Check to see if it was written
            rdData = MIFAREReader.MFRC522_Read(12)
            print ("No. 12")
            money=""
            for i in range(0,16):
                temp = chr(rdData[i])
                money+=temp
            print("money:",end=" ")
            print(money,"\n")

            MIFAREReader.MFRC522_StopCrypto1()
            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print("Authentication error")