#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, shutil, time

select_dict = {
    'A': 'Standard',
    'B': 'Error Recovery',
    'C': 'Detail Page'
}
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )
print( '請選擇爬蟲模式（單選）：' )
print( ' (A) Standard (B) Error Recovery (C) Detail Page' )
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )
select_condition = input( "請選擇：" )
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )
print( '您選擇的是：', select_dict[select_condition])
if select_condition is not 'C':
    startPosition = int(input( '請設定起始位置：'))
    endPosition = int(input( '請設定結束位置：'))
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )


'''
if os.path.isdir('data'):
    #刪除資料夾
    shutil.rmtree('data')
#新增空資料夾
os.mkdir('data')
'''

f = open('patent', 'r', encoding='utf-8')

if select_condition is 'A':
    for line in f.readlines()[startPosition:endPosition]:
        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
        line = line.strip()
        print('下載: ', line)
        os.system("python main.py " + line)
        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
        time.sleep(3)

if select_condition is 'B':
    # 處理網路錯誤的
    for line in f.readlines()[startPosition:endPosition]:

        line = line.strip()
        #print('檢查: ', line)
        try:
            ftxt = open('data/' + line + '.txt', 'r', encoding='utf-8')
            ftxt_lines = ftxt.readlines()
            num = len(ftxt_lines)
            numVerify = ftxt_lines[0]
            #print('num: ', num)
            #print('numVerify: ', (int(numVerify)//20) + 1 + int(numVerify))
            if(num != (int(numVerify)//20) + 1 + int(numVerify)):
                print("網路錯誤:", line)
        except:
            print('打不開 ' + line + '.txt')

if select_condition is 'C':
    #os.remove('bid6920.txt')
    pass