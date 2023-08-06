# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
''''''
import hashlib
import time
import os
import xlrd
import xlwt
from xlutils.copy import copy
import traceback
import re


def test(data):
    print('hello world!')
    print(data)


def md5value(data):
    input_name = hashlib.md5()
    input_name.update(data.encode("utf-8"))
    # print("大写的32位" + (input_name.hexdigest()).upper())
    # print("大写的16位" + (input_name.hexdigest())[8:-8].upper())
    # print("小写的32位" + (input_name.hexdigest()).lower())
    # print("小写的16位" + (input_name.hexdigest())[8:-8].lower())
    token = ((input_name.hexdigest()).upper(),
             (input_name.hexdigest())[8:-8].upper(),
             (input_name.hexdigest()).lower(),
             (input_name.hexdigest())[8:-8].lower(),
             )
    return token


def to_stamp(format_time):
    """
    2016-05-05 20:28:54 ----> 10位时间戳
    :param format_time:
    :return:
    """
    time_tuple = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    timestamp = str(int(time.mktime(time_tuple)))
    # print(timestamp)
    return timestamp


def to_date(start):
    """
    start = ['567100800', '1632844924200'] --->支持10位，13位时间戳转标准时间
    start = '2022-09-06 00:15:01' ---> 支持标准时间转10位时间戳
    :param start:
    :return:
    """
    starttime = []
    if type(start) == list:
        for timestamp in start:
            timestamp = list(timestamp)
            timestamp = int(''.join(timestamp[0: 10:]))
            time_local = time.localtime(timestamp)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            starttime.append(dt)
        return starttime
    if type(start) == str:
        timestamp = list(start)
        timestamp = int(''.join(timestamp[0: 10:]))
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt


def SaveExcel(filename, data, Excel_head):
    """
    file_name = '测试数据'
    a = 'hello'
    b = 'world'
    c = '!'
    data = {
        file_name: [[a], [b], [c]]
    }
    print(data)
    Excel_head = ('你好', '世界', '!!!')
    ku.SaveExcel(file_name, data, Excel_head)

    :param data: Type == dict       -->
    :param filename: Type == str
    :param Excel_head: Type == tuple
    :return: None
    """
    try:
        # 创建保存excel表格的文件夹
        # os.getcwd() 获取当前文件路径
        os_mkdir_path = os.getcwd() + '/数据/'
        # 判断这个路径是否存在，不存在就创建
        if not os.path.exists(os_mkdir_path):
            os.mkdir(os_mkdir_path)
        # 判断excel表格是否存在           工作簿文件名称
        os_excel_path = os_mkdir_path + f'{filename}.xls'

        if not os.path.exists(os_excel_path):
            # 不存在，创建工作簿(也就是创建excel表格)
            workbook = xlwt.Workbook(encoding='utf-8')
            """工作簿中创建新的sheet表"""  # 设置表名
            worksheet1 = workbook.add_sheet(filename, cell_overwrite_ok=True)
            """设置sheet表的表头"""
            sheet1_headers = Excel_head
            # 将表头写入工作簿
            for header_num in range(0, len(sheet1_headers)):
                # 设置表格长度
                worksheet1.col(header_num).width = 2560 * 3
                # 写入            行, 列,           内容
                worksheet1.write(0, header_num, sheet1_headers[header_num])
            # 循环结束，代表表头写入完成，保存工作簿
            workbook.save(os_excel_path)
        # 判断工作簿是否存在
        if os.path.exists(os_excel_path):
            # 打开工作簿
            workbook = xlrd.open_workbook(os_excel_path)
            # 获取工作薄中所有表的个数
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                for name in data.keys():
                    worksheet = workbook.sheet_by_name(sheets[i])
                    # 获取工作薄中所有表中的表名与数据名对比
                    if worksheet.name == name:
                        # 获取表中已存在的行数
                        rows_old = worksheet.nrows
                        # 将xlrd对象拷贝转化为xlwt对象
                        new_workbook = copy(workbook)
                        # 获取转化后的工作薄中的第i张表
                        new_worksheet = new_workbook.get_sheet(i)
                        for num in range(0, len(data[name])):
                            new_worksheet.write(rows_old, num, data[name][num])
                        new_workbook.save(os_excel_path)
    except:
        traceback.print_exc()
        print('异常:', data)


def html_clean(text):
    """
    传入文本  -->  输出清除HTML标签后的文本
    :param text: Type == str
    :return: new text
    """
    text = re.sub(r'<[^>]+>', '', text)
    return text


def filename_clean(filename):
    """
    传入文本 --> 输出清除文件名非法字符后的文本
    :param filename: Type == str
    :return: new name
    """
    replace_str = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_name = re.sub(replace_str, "_", filename)  # 替换为下划线
    return new_name


def SaveExcels(file_name, data, sheet, Excel_head):
    """
file_name = '测试一下了'
Excel_head = ('你', '好', '世', '界', '!')
for i in range(1, 3):
    sheet = f'第{i}页' # 生成每一页的表名
    data = {
        sheet: ['h', 'e', 'l', 'l', 'o']   # [str, str, str, str, str]
    }
    print(data)
    ku.SaveExcels(file_name, data, sheet, Excel_head)


    :param file_name: Type == str
    :param data: Type == dict
    :param sheet: Type == str
    :param Excel_head: Type == tuple
    :return: None
    """
    try:
        # 获取表的名称
        sheet_name = [i for i in data.keys()][0]
        # 创建保存excel表格的文件夹
        # os.getcwd() 获取当前文件路径
        os_mkdir_path = os.getcwd() + '/数据/'
        # 判断这个路径是否存在，不存在就创建
        if not os.path.exists(os_mkdir_path):
            os.mkdir(os_mkdir_path)
        # 判断excel表格是否存在           工作簿文件名称
        os_excel_path = os_mkdir_path + f'{file_name}.xls'
        if not os.path.exists(os_excel_path):
            # 不存在，创建工作簿(也就是创建excel表格)
            workbook = xlwt.Workbook(encoding='utf-8')
            """工作簿中创建新的sheet表"""  # 设置表名
            worksheet1 = workbook.add_sheet(sheet, cell_overwrite_ok=True)
            """设置sheet表的表头"""
            sheet1_headers = Excel_head
            # 将表头写入工作簿
            for header_num in range(0, len(sheet1_headers)):
                # 设置表格长度
                worksheet1.col(header_num).width = 2560 * 3
                # 写入表头        行,    列,           内容
                worksheet1.write(0, header_num, sheet1_headers[header_num])
            # 循环结束，代表表头写入完成，保存工作簿
            workbook.save(os_excel_path)
        """=============================已有工作簿添加新表==============================================="""
        # 打开工作薄
        workbook = xlrd.open_workbook(os_excel_path)
        # 获取工作薄中所有表的名称
        sheets_list = workbook.sheet_names()
        # 如果表名称：字典的key值不在工作簿的表名列表中
        if sheet_name not in sheets_list:
            # 复制先有工作簿对象
            work = copy(workbook)
            # 通过复制过来的工作簿对象，创建新表  -- 保留原有表结构
            sh = work.add_sheet(sheet_name)
            # 给新表设置表头
            excel_headers_tuple = Excel_head
            for head_num in range(0, len(excel_headers_tuple)):
                sh.col(head_num).width = 2560 * 3
                #               行，列，  内容，            样式
                sh.write(0, head_num, excel_headers_tuple[head_num])
            work.save(os_excel_path)
        """========================================================================================="""
        # 判断工作簿是否存在
        if os.path.exists(os_excel_path):
            # 打开工作簿
            workbook = xlrd.open_workbook(os_excel_path)
            # 获取工作薄中所有表的个数
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                for name in data.keys():
                    worksheet = workbook.sheet_by_name(sheets[i])
                    # 获取工作薄中所有表中的表名与数据名对比
                    if worksheet.name == name:
                        # 获取表中已存在的行数
                        rows_old = worksheet.nrows
                        # 将xlrd对象拷贝转化为xlwt对象
                        new_workbook = copy(workbook)
                        # 获取转化后的工作薄中的第i张表
                        new_worksheet = new_workbook.get_sheet(i)
                        for num in range(0, len(data[name])):
                            new_worksheet.write(rows_old, num, data[name][num])
                        new_workbook.save(os_excel_path)
    except Exception:
        traceback.print_exc()
        print('异常：', data)
