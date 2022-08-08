import os
import chooseLevel
# 設定 os.environ中的DISPLAY，否則turtle視窗無法開啟
def display():
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')
# 印出名字並呼叫選擇遊戲編號的函數
def playtest(name, uid_decimal):
    print("Hello ", name)
    display()
    chooseLevel.do(uid_decimal)
    
    