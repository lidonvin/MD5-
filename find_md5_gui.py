#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :2020/2/6 21:01
# @Author   :Donvin.li
# @File     :encodergui.py

import tkinter as tk
from tkinter.filedialog import askopenfilename
from hashlib import md5
import xlrd
import xlwt
import time
import os
import threading
import shutil
import base64

# 定义GUI主体框架

def base_desk(window):
    window.title('MD5弱密码查询工具v4.0')
    window.geometry('810x355')
    path=tk.StringVar()

    def upload_file():
        select_file=askopenfilename()
        path.set(select_file)
        #print(path.get())

    def update_info():
        update_info = '更新历史：\nv1.0更新内容:\n1、解决大文件界面卡死问题；\n2、调整查询按钮的布局。\nv2.0更新内容：\n' \
                      '1、输出报告不再保存到当前目录，而是保存到用户导入的文件所在目录。\nv3.0更新内容：\n1、增加进度显示；' \
                      '2、增加纯数字MD5查询功能。\nv4.0更新内容：\n1、增加计时器；2、增加剩余时间。'
        t1.insert(tk.INSERT, update_info)
    window.after(1,update_info)
    l1 = tk.Label(window, text='批量查询', font=('Arial', 10))
    l1.place(x=10, y=10)

    frm = tk.Frame(window)
    frm.grid(padx='20', pady='30')
    l2 = tk.Label(frm, text="目标路径：").grid(row=0, column=0)
    e1 = tk.Entry(frm, width=80, textvariable=path).grid(row=0, column=1)
    b1 = tk.Button(frm, text="选择文件", command=upload_file).grid(row=0, column=2, ipadx='3', ipady='3', padx='10')

    b2 = tk.Button(window, text='批量查询', width=10, height=1, command=lambda :thread_make(path,t1,t0,e0,e01,t2))
    b2.place(x=650, y=70)

    l0 = tk.Label(window, text='数字密码：起', font=('Arial', 9))
    l0.place(x=20, y=70)
    num = tk.StringVar(value=0)
    e0 = tk.Entry(window,textvariable=num, width=10, show=None)  # 数字密码起始
    e0.place(x=100, y=70)
    l0 = tk.Label(window, text='止', font=('Arial', 9))
    l0.place(x=170, y=70)
    num0 = tk.StringVar(value=0)
    e01 = tk.Entry(window,textvariable=num0, width=10, show=None)  # # 数字密码结束
    e01.place(x=190, y=70)


    t2 = tk.Text(window, bg='green', fg='white', font=('Arial', 10), width=12, height=1)
    t2.place(x=270, y=70)
    #输出进度提示
    t0 = tk.Text(window, bg='green', fg='white', font=('Arial', 10), width=40, height=1)
    t0.place(x=358,y=70)

    l3 = tk.Label(window, text='MD5值查询', font=('Arial', 10))
    l3.place(x=10, y=110)
    e2 = tk.Entry(window, width=90, show=None)  # 显示成明文形式
    e2.place(x=10, y=140)
    b3 = tk.Button(window, text='查询', width=10, height=1, command=lambda :main(e2,t1))
    b3.place(x=650, y=140)

    l4 = tk.Label(window, text='输出', font=('Arial', 10))
    l4.place(x=10, y=170)

    # l4=tk.Label(window, bg='yellow', width=111, text='empty')
    # l4.place(x=10,y=300)

    t1 = tk.Text(window, bg='green', fg='white', width=111, height=9)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    t1.place(x=10, y=200)

    l5 = tk.Label(window, text='版权：李东锋', font=('Arial', 10))
    l5.place(x=350, y=330)

# 单独查询函数
def main(e2,t1):
    md5_str = e2.get()
    if len(md5_str)!=32:
        output_err1='[*] MD5值不合法\n'
        t1.delete('1.0', 'end')
        t1.insert(tk.INSERT, output_err1)
    else:
        file = open('ruo4.txt', 'r')

        lis=[]
        for x in file:
            rs = x.strip()
            hsh = md5()
            hsh.update(rs.encode('utf-8'))
            hashmd5 = hsh.hexdigest()

            if hashmd5 == str(md5_str).lower():
                output_suss='[*] 查询成功：'+str(x)
                t1.delete('1.0', 'end')
                t1.insert(tk.INSERT, output_suss)
                lis.append(x)
                break
        if len(lis)==0:
            output_err2='[*] 查询失败或非标准MD5'
            t1.delete('1.0', 'end')
            t1.insert(tk.INSERT, output_err2)
# 子线程函数
def thread_make(path,t1,t0,e0,e01,t2):
    output_err02 = '[*] 批量查询程序开始......\n'
    t1.delete('1.0', 'end')
    t1.insert(tk.INSERT, output_err02)
    Thread1 = threading.Thread(target=main_piliang, args=((path,t1,t0,e0,e01)))
    Thread1.start()
    Thread2 = threading.Thread(target=seconds, args=((t2,)))
    Thread2.start()

# 批量查询函数
def main_piliang(path,t1,t0,e0,e01):
    file_path_name=path.get()
    file_name=os.path.basename(file_path_name)
    file_path=os.path.dirname(file_path_name)
    file_name_1=file_name.split('.')[0]
    try:
        wb = xlrd.open_workbook(file_path_name)  # 打开excel文件创建对象
        sheef_name = wb.sheet_names()[0]
        sheet = wb.sheet_by_name(sheef_name)  # 获取表内容
    except:
        output_err1='[*] 错误！你提供的文件格式不合法，请核对。\n'
        t1.insert(tk.INSERT, output_err1)
        exit()

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建对象
    sheet1 = book.add_sheet('弱密码', cell_overwrite_ok=True)
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True  # 黑体
    style.font = font  # 设定样式
    sheet1.write(0, 0, 'ID', style)  # 首行第一列
    sheet1.write(0, 1, 'LOGIN_NAME', style)  # 首行第二列
    sheet1.write(0, 2, 'PASSWORD', style)  # 首行第三列
    # sheet1.write(0, 3, 'NAME', style)
    # sheet1.write(0, 4, 'ROLENAME', style)
    try:
        start_num=int(e0.get())
        stop_num=int(e01.get())
    except:
        output_err0 = '[*] 数字密码起止只能输入数字！\n'
        t1.insert(tk.INSERT, output_err0)
        exit()
    if start_num>stop_num:
        output_err01 = '[*] 你是傻逼吗？大小分不清！\n'
        t1.insert(tk.INSERT, output_err01)
        exit()

    a = 0
    b=sheet.nrows - 1
    start_time=time.time()
    end_time=0
    for i in range(b):  # 遍历所有的行
        #计算百分比
        c='%.2f%%' % ((i+1)/b*100)
        #计算剩余时间
        seconds=round(end_time - start_time, 0)
        d=seconds/(i+1)*(b-i)
        m, s = divmod(d, 60)
        h, m = divmod(m, 60)
        e = "%d:%02d:%02d" % (h, m, s)
        output_0='进度:'+str(i+1)+'/'+str(b)+'|百分比:'+c+'|剩余:'+str(e)
        t0.delete('1.0', 'end')
        t0.insert(tk.INSERT, output_0)
        flag=False
        # output_1='[*]当前第' + str(i)+'行\n'
        # t1.insert(tk.INSERT, output_1)
        md5_str = sheet.cell(i + 1, 1).value
        if len(md5_str)!=32:
            output_err2='[*] 错误！第'+str(i+1)+'行MD5值不合法，请核对。\n'
            t1.insert(tk.INSERT, output_err2)
        else:
            #在密码本中查询
            file = open('ruo4.txt', 'r')
            for x in file:
                rs = x.strip()

                # 普通MD5加密
                hsh = md5()
                hsh.update(rs.encode('utf-8'))
                hashmd5 = hsh.hexdigest()
                if hashmd5 == str(md5_str).lower():

                # MD5两轮加密MD5(MD5(pass)
                # hsh2=md5()
                # hsh2.update(hashmd5.encode('utf-8'))
                # hashmd5_2=hsh2.hexdigest()
                # if hashmd5_2 == str(md5_str).lower():   #MD5(MD5(pass))

                # MD5(BASE64)加密
                # m = md5()
                # m.update(rs.encode('utf-8'))
                # result = m.digest()
                # md5_base64 = base64.b64encode(result).decode('utf-8')
                # print(md5_base64)
                # if md5_base64 == str(md5_str).lower():

                    flag=True
                    a += 1
                    ID = a
                    # ID=sheet.cell(i+1, 0).value
                    LOGIN_NAME = str(sheet.cell(i + 1, 0).value)
                    PASSWORD = x

                    output_2='['+str(a)+']'+' 密码本发现弱密码：'+LOGIN_NAME+'：'+PASSWORD
                    t1.insert(tk.INSERT, output_2)

                    sheet1.write(a, 0, ID)
                    sheet1.write(a, 1, LOGIN_NAME)
                    sheet1.write(a, 2, PASSWORD)
                    # sheet1.write(a, 3, NAME)
                    # sheet1.write(a, 4, ROLENAME)

                    break  # 当匹配成功后结束当前整个循环进入上层的下一循环

            # 查询1个的结束时间(如果有continue)
            end_time = time.time()
            if flag or stop_num==0:
                continue    #如果查询成功后面的语句就不要执行了(不在数字集合中查了，继续下一个)

            #在数字集合中查询
            for num in range(start_num,stop_num):
                num_pass = str(num)

                # 普通MD5加密
                hsh0 = md5()
                hsh0.update(num_pass.encode('utf-8'))
                hashmd5_0 = hsh0.hexdigest()
                if hashmd5_0 == str(md5_str).lower():

                # MD5两轮加密MD5(MD5(pass)
                # hsh02=md5()
                # hsh02.update(hashmd5_0.encode('utf-8'))
                # hashmd5_02=hsh02.hexdigest()
                # if hashmd5_02 == str(md5_str).lower():   #MD5(MD5(pass))

                # MD5(BASE64)加密
                # m0 = md5()
                # m0.update(num_pass.encode('utf-8'))
                # result0 = m0.digest()
                # md5_base640 = base64.b64encode(result0).decode('utf-8')
                # if md5_base640 == str(md5_str).lower():

                    a += 1
                    ID = a
                    LOGIN_NAME = str(sheet.cell(i + 1, 0).value)
                    PASSWORD = num_pass

                    output_2 = '[' + str(a) + ']' + ' 数字集合发现弱密码：' + LOGIN_NAME + '：' + PASSWORD+'\n'
                    t1.insert(tk.INSERT, output_2)

                    sheet1.write(a, 0, ID)
                    sheet1.write(a, 1, LOGIN_NAME)
                    sheet1.write(a, 2, PASSWORD)
                    break
            #查询1个的结束时间(如果没有continue，我就更新)
            end_time = time.time()

    sheet1.col(0).width = 5000  # 第1列宽度
    sheet1.col(1).width = 10000
    sheet1.col(2).width = 10000
    # sheet1.col(3).width = 10000
    # sheet1.col(4).width = 10000
    now=time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
    result_name=file_name_1+'-'+now+'-report.xls'
    output_3='[*] 查询结束，开始生成报告......\n'
    t1.insert(tk.INSERT, output_3)
    book.save(result_name)  # 保存excel文件
    shutil.move(result_name,file_path)
    output_4='[*] 已生成报告：'+file_path+result_name
    t1.insert(tk.INSERT, output_4)

def seconds(t2):
    starttime = time.time()
    while True:
        time.sleep(1)
        seconds = round(time.time() - starttime, 0)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        sec="%d:%02d:%02d" % (h, m, s)
        output_02 = '时长：'+str(sec)
        t2.delete('1.0', 'end')
        t2.insert(tk.INSERT, output_02)

if __name__=='__main__':
    window = tk.Tk()
    base_desk(window)
    window.mainloop()
#client_backdoor()
