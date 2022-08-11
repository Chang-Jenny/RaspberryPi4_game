import pymysql
import turtle as t
# 以python與MySQL做連線與查詢


# 進行連線
def con():
    global conn
    host = "localhost";
    dbuser = "root";
    dbpasswd = "123456";
    dbname = "project";
    conn = pymysql.connect(host=host, user=dbuser, passwd=dbpasswd, db=dbname, charset='utf8')

# 查詢哪一個遊戲的排行榜
# 以分數遞減排序
def recordGame(g):
    game=g
    print("recordGame", game)
    mycursor = conn.cursor()
    sql = "SELECT * FROM `play` WHERE `level`= '{}' ORDER BY score DESC;".format(game);
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# 印出在time's up後的排行榜單
def board(which):
    con()
    record=recordGame(which)
    output= t.Turtle()
    output.pensize(2)  # pen的粗細
    output.speed(0)  # set draw_speed high
    output.pencolor("white")
    output.hideturtle()
    a=0
    for p in ["Rank", "ID", "Record", "When."]:
        output.penup()
        output.goto(-250+120*a, 50)
        output.pendown()
        output.write(p, align='left', font=('黑體', 18, 'bold'))
        a+=1
    medal=0
    for a in range(len(record)):
        medal+=1
        output.penup()
        output.goto(-250,0-a*50)
        output.write(medal, align='left', font=('黑體', 14, 'bold'))
        output.pendown()
        for b in [0,2,3]:
            output.penup()
            output.goto(-250+80*(b+1),0-a*50)
            output.pendown()
            output.write(record[a][b], align='left', font=('黑體', 14, 'bold'))
    