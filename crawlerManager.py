#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, shutil, time

crawl_stepWaitTime = 3
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
        time.sleep(crawl_stepWaitTime)

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
            ftxt.close()
            #print('num: ', num)
            #print('numVerify: ', (int(numVerify)//20) + 1 + int(numVerify))
            if(num != (int(numVerify)//20) + 1 + int(numVerify)):
                print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                print("網路錯誤:", line + '.txt')
                os.remove('data/' + line + '.txt')
                print("重新下載: ", line)
                print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                os.system("python main.py " + line + " --repair")
                time.sleep(crawl_stepWaitTime)
        except:
            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
            print('打不開 ' + line + '.txt')
            try:
                os.remove('data/' + line + '.txt')
            except:
                print('找不到 ' + line + '.txt')
            print("重新下載: ", line)
            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
            os.system("python main.py " + line)
            time.sleep(crawl_stepWaitTime)

if select_condition is 'C':
    #os.remove('bid6920.txt')
    pass