import sqlite3
import tkinter as tk
from datetime import datetime
from functools import partial

import serial
from PIL import ImageTk,Image
from matplotlib import pyplot as plt


fig, (ax1,ax2) = plt.subplots(2, 1)

def getDataFromArduino():
    try:
        ser = serial.Serial('COM3', 9600)
        data = ser.readline()
        print(data)
        mas = str(data).replace("b'", "").replace("\\r\\n'", "").split()
        return mas
        t = float(mas[0])
        pt = float(mas[1])
    except:
        print('Ошибка подключения к Ардуино')
        temperature.config(text=f"Ошибка связи")
        pressure.config(text=f"")


def update_time():
    global H
    label.config(text=f"{datetime.now():%H:%M:%S}")
    root.after(1000, update_time)  # Запланировать выполнение этой же функции через 100 миллисекунд


def update_data():
    try:
        dataFromArduino = getDataFromArduino()
        print(dataFromArduino)
        H = (float(dataFromArduino[2]) / 240) * 100
        H = round(H, 2)
        print(H)
        temperature.config(text=f"Температура: {dataFromArduino[0]} °C")
        humidity.config(text=f"Влажность: {H} %")
        pressure.config(text=f"Давление: {dataFromArduino[1]} мм.рт.ст.")
        moveDataToDB(H)
        root.after(2000, update_data)  # Запланировать выполнение этой же функции через 100 миллисекунд
    except:
        print("bad connection")


def getDataFromDB(COUNT=60):
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    res = [[], [], []]
    sqlite_select_query = """SELECT * from sqlitedb_developers ORDER BY id DESC LIMIT {}""".format(COUNT)
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print("Всего строк:  ", len(records))
    print("Вывод каждой строки")
    for row in records:
        res[0].insert(0, row[1])
        res[1].insert(0, row[2])
        res[2].insert(0, row[3])
        # print("ID:", row[0])
        # print("Имя:", row[1])
        # print("Почта:", row[2])
    return res
    cursor.close()

def createPicture(COUNT=60):
    graphData = getDataFromDB(COUNT)
    X1 = range(len(graphData[0]))
    Y1 = graphData[0]
    X2 = range(len(graphData[1]))
    Y2 = graphData[1]
    X3 = range(len(graphData[2]))
    Y3 = graphData[2]
    plt.subplots_adjust(plt.subplots_adjust(wspace=1, hspace=0.3))
    ax1.plot(X2, Y2)
    ax1.set_title('График температуры')
    ax2.plot(X3, Y3)
    ax2.set_title('График влажности')
    plt.savefig('graphics.png')
    ax1.cla()
    ax2.cla()
    img2 = ImageTk.PhotoImage(Image.open('graphics.png'))
    labelImg.configure(image=img2)
    labelImg.image = img2
def show_graphics():
    global labelImg
    graphics = tk.Toplevel(root)
    graphics.title("Вывод графиков")
    graphics.geometry("600x550")

    graphData = getDataFromDB(60)
    X1 = range(len(graphData[0]))
    Y1 = graphData[0]
    X2 = range(len(graphData[1]))
    Y2 = graphData[1]
    X3 = range(len(graphData[2]))
    Y3 = graphData[2]
    plt.subplots_adjust(plt.subplots_adjust(wspace=1, hspace=0.3))
    ax1.plot(X2, Y2)
    ax1.set_title('График температуры')
    ax2.plot(X3, Y3)
    ax2.set_title('График влажности')
    plt.savefig('graphics.png')
    ax1.cla()
    ax2.cla()

    img = tk.PhotoImage(file='graphics.png')
    labelImg = tk.Label(graphics, image=img)
    labelImg.image_ref = img
    labelImg.pack()

    min=tk.Button(graphics, text='Час',command=partial(createPicture,60)).place(x = 100, y = 500, width = 100)
    hour=tk.Button(graphics, text='День',command=partial(createPicture,1440)).place(x = 250, y = 500, width = 100)
    day=tk.Button(graphics, text='Неделя',command=partial(createPicture,10080)).place(x = 400, y = 500, width = 100)

def moveDataToDB(H):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        dataFromArduino = getDataFromArduino()
        sqlite_insert_query = """INSERT INTO sqlitedb_developers(t,p,h) VALUES (?,?,?);"""
        data_tuple = (dataFromArduino[0], dataFromArduino[1], H)
        cur = cursor.execute(sqlite_insert_query, data_tuple)
        sqlite_connection.commit()
    except:
        print("Не записал")


root = tk.Tk()
root.geometry('400x300+{}+{}'.format(500, 400))
label = tk.Label(root, font=("helvetica", 15))
label.pack()
temperature = tk.Label(root, font=("helvetica", 15))
pressure = tk.Label(root, font=("helvetica", 15))
humidity = tk.Label(root, font=("helvetica", 15))
temperature.pack()
humidity.pack()
pressure.pack()
btn = tk.Button(root, text="Просмотр графиков", font=("helvetica", 15), command=show_graphics)
btn.pack()
update_time()
update_data()

root.mainloop()
