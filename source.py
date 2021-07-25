import tushare as tss
from tkinter import *
from tkinter import ttk
from time import *
from datetime import *
from sqlite3 import *
import pandas as pd
database = connect('database.db')
try:
    SQL = 'DROP TABLE industry_same'
    database.execute(SQL)
    database.commit()
except: print('industry_same fail')
try:
    SQL = 'drop table self_history'
    database.execute(SQL)
    database.commit()
except: print("self_history fail")
try:
    SQL = 'drop table self_future'
    database.execute(SQL)
    database.commit()
except: print('self_future fail')
tss.set_token('08f1ea6fc533276b375d37c530901794da7ce1074e239e7f5754b153')
ts = tss.pro_api()
data = ts.query('stock_basic', exchange='', list_status='L', fields='ts_code,name,industry')
def get():
        global name, start, end, index, year
        start = str(Start.get())
        end = str(End.get())
        name = str(Code.get())
        Index = int(numberChosen.current())
        if Index == 0: index = 'open'
        elif Index == 1: index = 'close'
        elif Index == 2: index = 'high'
        elif Index == 3: index = 'low'
        elif Index == 4: index = 'pre_close'
        year = int(Year.get())
        root.destroy()
root = Tk()
root.geometry('500x300')
root.title('基于Python的股票价格序列相似性分析')
Label(root, text='股票代码：').place(relx=0.25, rely=0.0)
Code = Entry(root)
Code.place(relx=0.37, rely=0.0)
Label(root, text='开始时间(如20180405)：').place(relx=0.1, rely=0.1)
Start = Entry(root)
Start.place(relx=0.37, rely=0.1)
Label(root, text='结束时间(如20180506)：').place(relx=0.1, rely=0.2)
End = Entry(root)
End.place(relx=0.37, rely=0.2)
Label(root, text='评价指标').place(relx=0.1, rely=0.3)
number = StringVar()
numberChosen = ttk.Combobox(root, width=12, textvariable=number)
numberChosen['values'] = ('开盘价', '收盘价', '最高价', '最低价', '昨收价')
numberChosen.place(relx=0.37, rely=0.3)
numberChosen.current(1)
Label(root, text='历史可重复性分析追溯年数：').place(relx=0.05, rely=0.4)
Year = ttk.Combobox(root, width=12, textvariable=StringVar())
Year['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
Year.place(relx=0.37, rely=0.4)
Year.current(0)
Button(root, text='确定', command=get).place(relx=0.5, rely=0.5)
root.mainloop()
start_history = str(int(end[:4])-year) + end[4:6] + end[6:]
end_future = datetime.date.today()
end_future = str(end_future).replace('-', '')
Index = data[(data['ts_code'] == name)].index
a = str(data.loc[Index]['industry'].values[0])
Name = str(data.loc[Index]['name'].values[0])
try:
    df = ts.query('daily', ts_code=name, start_date=start_history, end_date=end)
    pd.io.sql.to_sql(df, 'self_history', con=database, if_exists='append')
    df = ts.query('daily', ts_code=name, start_date=start, end_date=end_future)
    pd.io.sql.to_sql(df, 'self_future', con=database, if_exists='append')
    for i in (data[(data['industry'] == a)]['ts_code']):
        df = ts.query('daily', ts_code=i, start_date=start, end_date=end)
        pd.io.sql.to_sql(df, 'industry_same', con=database, if_exists='append')
    print("data written successfully!")
except: print("data error!")
database.close()