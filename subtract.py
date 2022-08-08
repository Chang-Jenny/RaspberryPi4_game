def sub(money):
    m=int(money)
    if(m>0):
        m-=10
        calculate=str(m)
        data=[]
        # 將扣款後的金額經過字串轉換，再轉成RFID儲存的格式
        # 非數字則存" "以利重新計算為數字
        for i in range(0, len(calculate)):
            data.append(ord(calculate[i]))
        for i in range(len(calculate), 16):
            data.append(ord(" "))
    else:
        data=[]
        for i in range(0, 1):
            data.append(ord("0"))
        for i in range(1, 16):
            data.append(ord(" "))
        print("現在是0元快去加值吧!!!")
    return data