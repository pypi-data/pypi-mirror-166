# -*- coding:utf-8 -*-
"""
Author: Wdataorg
Date: .09.04
Project Name: Wdata
"""
import tkinter as tk
from tkinter import *
import easygui as g

from tkinter import filedialog, dialog

import os
import random
import tkinter
import tkinter.messagebox as messagebox
import requests

win = tk.Tk()
win.title("cn语言-打造全中文编程")
# win.wm_iconbitmap('1.ico')
win.geometry('800x600')
lb = tk.Label(win, text='cn语言-全中文编程')
lb.pack()
text = tk.Text(win, width=300, height=20, font=20)
text.pack()
lb = tk.Label(win, text='输出框')
lb.pack()
chu = tk.Text(win, width=300, height=10, font=20)
chu.pack()
text.insert(tk.END, "打印：你好，世界\n''示例代码")


def opena():
    filename = filedialog.askopenfilename()
    f = open(filename, 'r')
    f2 = f.read()
    f.close()
    text.insert(INSERT, f2)


def zuozhe():
    messagebox.showerror("作者", "黑客零")


def quit():
    win.destroy()


def file():
    filename = filedialog.asksaveasfilename(filetypes=[("TXT", ".txt")])
    with open(filename + '.txt', 'w') as f:
        f.write(text.get('1.0', 'end'))


def run():
    dm = text.get('1.0', 'end')
    with open('dm.txt', 'w') as f:
        f.write(dm)
    for line in open("dm.txt"):
        if "''" in line:
            pass

        elif '打印：获得答复' in line:
            chu.insert(tk.END, huida + '\n')
        elif '打印：' in line:
            p = line.strip("打印：")
            chu.insert(tk.END, p)
        elif '询问：' in line:
            huida = g.enterbox(line.strip('询问：'))


        elif '新建变量：' in line:
            a = 1
        elif '设置变量名：' in line and a == 1:
            name = line.strip('设置变量名：')
            a = 2

        elif '设置变量值：' in line and a == 2:
            zhi = line.strip('设置变量值：')
            i = 1



        elif "引用：请求" in line:
            request = 1

        elif '请求网站源码：' in line and request == 1:
            ym = requests.get(line.strip('请求网站源码：'))

            g.msgbox('ym,text')
            print(ym.text)
        elif '请求网页状态' in line and request == 1:
            z = requests.get(line.strip('请求网站状态：'))
            chu.insert(tk.END, z)
        elif '引用：终端' in line:
            a = 3
        elif '终端输入：' in line and a == 3:
            os.system(line.strip('终端输入：'))
        elif '引用：随机：' in line:
            a = 4
        elif '随机数一：' in line:
            sa = line.strip('随机数一：')
            sa = int(sa)
        elif '随机数二：' in line:
            sb = line.strip('随机数二：')
            sb = int(sb)
            s = random.randint(sa, sb)
        elif '打印随机数' in line:
            s = str(s)
            chu.insert(tk.END, s + '\n')


menubar = Menu(win)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='运行', menu=filemenu)
filemenu.add_command(label='运行调试', command=run)
filemenu.add_command(label='打开', command=opena)
filemenu.add_command(label='保存', command=file)
filemenu.add_command(label='作者', command=zuozhe)
win.config(menu=menubar)
win.mainloop()
