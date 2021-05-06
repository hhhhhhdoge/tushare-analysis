from source import *
import tushare as tss
import matplotlib.pyplot as plt
import pandas as pd
from pylab import *
from sqlite3 import *
import numpy as np
from dtw import dtw
import os
mpl.rcParams['font.sans-serif'] = ['SimHei']
database = connect('C:/Users/admin/Desktop/database.db')
open, low, high, close = [], [], [], []
open1, low1, high1, close1 = [], [], [], []
close_his, close_fut = [], []
def main():
    industry_samedb = database.execute("SELECT * from industry_same")
    self_hisdb = database.execute('select * from self_history')
    self_futdb = database.execute('select * from self_future')
    dis_industry_same, code_industry_same = [], []
    for it in self_hisdb:
        for i in range(len(it)):
            if i == 6:
                if close_his == []: c = float(it[i])
                close_his.append(float(it[i]) / c)
    for it in self_futdb:
        for i in range(len(it)):
            if i == 6:
                if close_fut == []: c = float(it[i])
                close_fut.append(float(it[i]) / c)
    ty = 0
    h = 1
    for it in industry_samedb:
        ty += 1
        if str(it[1]) == name:
            for i in range(len(it)):
                if i == 3:
                    if open == []: o = float(it[i])
                    open.append(float(it[i]) / o)
                if i == 4:
                    if high == []: h = float(it[i])
                    high.append(float(it[i]) / h)
                if i == 5:
                    if low == []: l = float(it[i])
                    low.append(float(it[i]) / l)
                if i == 6:
                    if close == []: c = float(it[i])
                    close.append(float(it[i]) / c)
        else:
            for i in range(len(it)):
                if i == 3:
                    if open1 == []: o = float(it[i])
                    open1.append(float(it[i]) / o)
                if i == 4:
                    if high1 == []: o = float(it[i])
                    high1.append(float(it[i]) / h)
                if i == 5:
                    if low1 == []: l = float(it[i])
                    low1.append(float(it[i]) / l)
                if i == 6:
                    if close1 == []: c = float(it[i])
                    close1.append(float(it[i]) / c)
            if ty % 38 == 0:
                p = dtw(close, close1, keep_internals=True)
                dis_industry_same.append(p.distance)
                code_industry_same.append(it[1])
                open1.clear()
                high1.clear()
                close1.clear()
                low1.clear()
    for i in range(len(dis_industry_same)):
        for j in range(i, len(dis_industry_same)):
            if dis_industry_same[i] > dis_industry_same[j]:
                dis_industry_same[i], dis_industry_same[j] = dis_industry_same[j], dis_industry_same[i]
                code_industry_same[i], code_industry_same[j] = code_industry_same[j], code_industry_same[i]
    i = 0
    ty = 0
    file_name1 = "C:/Users/admin/Desktop/picsrc/industry_same/"
    file_name2 = "C:/Users/admin/Desktop/picsrc/self_history/"
    file_name3 = "C:/Users/admin/Desktop/picsrc/self_future/"
    try:
        for root, dirs, files in os.walk(file_name1):
            for namee in files:
                if namee.endswith(".png"): os.remove(os.path.join(root, namee))
    except: pass
    try:
        for root, dirs, files in os.walk(file_name2):
            for namee in files:
                if namee.endswith(".png"): os.remove(os.path.join(root, namee))
    except: pass
    try:
        for root, dirs, files in os.walk(file_name3):
            for namee in files:
                if namee.endswith(".png"): os.remove(os.path.join(root, namee))
    except: pass
    NAME = []

    #insustr_same
    for i in range(10):
        df = ts.query('daily', ts_code=code_industry_same[i], start_date=start, end_date=end)
        data2 = df['close']
        closee = data2.values.tolist()
        close2 = []
        close2.clear()
        for j in range(len(closee)): close2.append(closee[j] / closee[0])
        plt.figure(figsize=(4, 2))
        p1, = plt.plot(close, 'b')
        p2, = plt.plot(close2, 'r')
        Index = data[(data['ts_code'] == code_industry_same[i])].index
        name_industry_same = str(data.loc[Index]['name'].values[0])
        plt.legend([p1, p2], [Name+name, name_industry_same+code_industry_same[i]], loc = 1)
        NAME.append(name_industry_same+code_industry_same[i])
        close2.clear()
        plt.savefig('C:/Users/admin/Desktop/picsrc/industry_same/'+str(i + 1)+'.png', dpi=100)
        plt.close()

    #self_his
    num = 0
    self_his_list = []
    dis_his, begindate = [], []
    dstart_his = datetime.datetime(int(start_history[:4]), int(start_history[4:6]), int(start_history[6:]))
    d1 = datetime.datetime(int(start[:4]), int(start[4:6]), int(start[6:]))
    d2 = datetime.datetime(int(end[:4]), int(end[4:6]), int(end[6:]))
    interval = d2 - d1
    days = interval.days
    for i in range(len(close_his)):
        if num == days:
            num = 0
            p = dtw(close, self_his_list, keep_internals=True)
            dis_his.append(p.distance)
            begindate.append(i)
            self_his_list.clear()
        num += 1
        self_his_list.append(close_his[i])
    for i in range(len(dis_his)):
        for j in range(i, len(dis_his)):
            if dis_his[i] > dis_his[j]:
                dis_his[i], dis_his[j] = dis_his[j], dis_his[i]
                begindate[i], begindate[j] = begindate[j], begindate[i]
    close2 = []
    for i in range(6):
        close2.clear()
        delta1 = datetime.timedelta(days=begindate[i])
        delta2 = datetime.timedelta(days=begindate[i]+days)
        n1 = dstart_his + delta1
        n2 = dstart_his + delta2
        n1 = n1.strftime('%Y%m%d')
        n2 = n2.strftime('%Y%m%d')
        df = ts.query('daily', ts_code=name, start_date=n1, end_date=n2)
        data2 = df['close']
        closee = data2.values.tolist()
        for j in range(len(closee)): close2.append(closee[j] / closee[0])
        plt.figure(figsize=(4, 2))
        p1, = plt.plot(close, 'b')
        p2, = plt.plot(close2, 'r')
        plt.legend([p1, p2], [str(d1.strftime('%Y%m%d'))+'-'+str(d2.strftime('%Y%m%d')), str(n1)+'-'+str(n2)], loc=1)
        plt.savefig('C:/Users/admin/Desktop/picsrc/self_history/' + str(i + 1) + '.png', dpi=100)
        plt.close()

    #self_future
    num = 0
    self_fut_list = []
    dis_fut, begindate = [], []
    begindate.clear()
    for i in range(len(close_fut)):
        if num == days:
            num = 0
            p = dtw(close, self_fut_list, keep_internals=True)
            dis_fut.append(p.distance)
            begindate.append(i)
            self_fut_list.clear()
        num += 1
        self_fut_list.append(close_fut[i])
    for i in range(len(dis_fut)):
        for j in range(i, len(dis_fut)):
            if dis_fut[i] > dis_fut[j]:
                dis_fut[i], dis_fut[j] = dis_fut[j], dis_fut[i]
                begindate[i], begindate[j] = begindate[j], begindate[i]
    close2 = []
    for i in range(6):
        close2.clear()
        delta1 = datetime.timedelta(days=begindate[i])
        delta2 = datetime.timedelta(days=begindate[i] + days)
        n1 = d1 + delta1
        n2 = d1 + delta2
        n1 = n1.strftime('%Y%m%d')
        n2 = n2.strftime('%Y%m%d')
        df = ts.query('daily', ts_code=name, start_date=n1, end_date=n2)
        data2 = df['close']
        closee = data2.values.tolist()
        for j in range(len(closee)): close2.append(closee[j] / closee[0])
        plt.figure(figsize=(4, 2))
        p1, = plt.plot(close, 'b')
        p2, = plt.plot(close2, 'r')
        plt.legend([p1, p2], [str(d1.strftime('%Y%m%d')) + '-' + str(d2.strftime('%Y%m%d')), str(n1) + '-' + str(n2)], loc=1)
        plt.savefig('C:/Users/admin/Desktop/picsrc/self_future/' + str(i + 1) + '.png', dpi=100)
        plt.close()
    print('Analysis done!')
    database.close()
from tkinter import *
from PIL import ImageTk, Image
def industry_same_picshow():
    rt = Tk()
    rt.title('9支同领域最相近的股票')
    rt.geometry('1500x1300')
    canvas = Canvas(rt, bg='white', height=1500, width=1300)
    Label(canvas, text='9支同领域最相近的股票', font=('楷体', 30)).place(relx=0.3, rely=0)
    image_file1 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/1.png')
    canvas.create_image(0, 50, anchor='nw', image=image_file1)
    canvas.pack()
    image_file2 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/2.png')
    canvas.create_image(400, 50, anchor='nw', image=image_file2)
    canvas.pack()
    image_file3 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/3.png')
    canvas.create_image(800, 50, anchor='nw', image=image_file3)
    canvas.pack()
    image_file4 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/4.png')
    canvas.create_image(0, 250, anchor='nw', image=image_file4)
    canvas.pack()
    image_file5 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/5.png')
    canvas.create_image(400, 250, anchor='nw', image=image_file5)
    canvas.pack()
    image_file6 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/6.png')
    canvas.create_image(800, 250, anchor='nw', image=image_file6)
    canvas.pack()
    image_file7 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/7.png')
    canvas.create_image(0, 450, anchor='nw', image=image_file7)
    canvas.pack()
    image_file8 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/8.png')
    canvas.create_image(400, 450, anchor='nw', image=image_file8)
    canvas.pack()
    image_file9 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/industry_same/9.png')
    canvas.create_image(800, 450, anchor='nw', image=image_file9)
    canvas.pack()
    rt.mainloop()
def his_picshow():
    rh = Tk()
    rh.title('历史可重复性')
    rh.geometry('1500x1300')
    canvas = Canvas(rh, bg='white', height=1500, width=1300)
    Label(canvas, text='历史可重复性', font=('楷体', 30)).place(relx=0.4, rely=0)
    image_file1 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_history/1.png')
    canvas.create_image(0, 50, anchor='nw', image=image_file1)
    canvas.pack()
    image_file2 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_history/2.png')
    canvas.create_image(400, 50, anchor='nw', image=image_file2)
    canvas.pack()
    image_file3 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_history/3.png')
    canvas.create_image(800, 50, anchor='nw', image=image_file3)
    canvas.pack()
    image_file4 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_history/4.png')
    canvas.create_image(0, 350, anchor='nw', image=image_file4)
    canvas.pack()
    image_file5 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_history/5.png')
    canvas.create_image(400, 350, anchor='nw', image=image_file5)
    canvas.pack()
    image_file6 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_history/6.png')
    canvas.create_image(800, 350, anchor='nw', image=image_file6)
    canvas.pack()
    rh.mainloop()
def fut_picshow():
    rf = Tk()
    rf.title('未来可预测性')
    rf.geometry('1500x1300')
    canvas = Canvas(rf, bg='white', height=1500, width=1300)
    Label(canvas, text='未来可预测性', font=('楷体', 30)).place(relx=0.4, rely=0)
    image_file1 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_future/1.png')
    canvas.create_image(0, 50, anchor='nw', image=image_file1)
    canvas.pack()
    image_file2 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_future/2.png')
    canvas.create_image(400, 50, anchor='nw', image=image_file2)
    canvas.pack()
    image_file3 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_future/3.png')
    canvas.create_image(800, 50, anchor='nw', image=image_file3)
    canvas.pack()
    image_file4 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_future/4.png')
    canvas.create_image(0, 350, anchor='nw', image=image_file4)
    canvas.pack()
    image_file5 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_future/5.png')
    canvas.create_image(400, 350, anchor='nw', image=image_file5)
    canvas.pack()
    image_file6 = PhotoImage(file='C:/Users/admin/Desktop/picsrc/self_future/6.png')
    canvas.create_image(800, 350, anchor='nw', image=image_file6)
    canvas.pack()
    rf.mainloop()
def Show():
    industry_same_picshow()
    his_picshow()
    fut_picshow()
if __name__ == '__main__':
    main()
    Show()