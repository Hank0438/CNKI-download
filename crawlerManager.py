#!/usr/bin/bash
# -*- coding: utf-8 -*-

import os, shutil, time
from main import startCrawler

crawl_stepWaitTime = 3
select_dict = {
    'A': 'Standard',
    'B': 'Error Recovery',
    'C': 'Create List',
}
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )
print( '請選擇爬蟲模式（單選）：' )
print( ' (A) Standard (B) Error Recovery (C) Check Data' )
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )
select_condition = input( "請選擇：" )
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )
print( '您選擇的是：', select_dict[select_condition])
if (select_condition is 'A'):
    startPosition = int(input( '請設定起始位置：'))
    endPosition = int(input( '請設定結束位置：'))
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )



if os.path.isdir('data') is not True:
    #刪除資料夾 #shutil.rmtree('data')
    #新增空資料夾
    os.mkdir('data')



if select_condition is 'A':
    f = open('patent', 'r', encoding='utf-8')
    for line in f.readlines()[startPosition:endPosition]:
        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
        line = line.strip()
        print('下載: ', line)
        ### os.system("python main.py " + line)
        startCrawler(line, '')
        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
        time.sleep(crawl_stepWaitTime)



if select_condition is 'B':

    # 處理網路錯誤的
    part = input('第幾份:')
    f = open('referenceDetail' + part + '000.txt', 'r', encoding='utf-8')
    for detail in f.readlines():
        detail = detail.strip().split(' ')
        idx = detail[0]
        line = detail[1]
        print('檢查: ', idx, line)
        if len(detail) == 3:
            numVerify = detail[2]

            if os.path.isfile('data/' + line + '.txt'):
                try:
                    ftxt = open('data/' + line + '.txt', 'r', encoding='utf-8')
                    ftxt_lines = ftxt.readlines()
                    num = len(ftxt_lines)
                    ftxt.close()
                    print('num: ', num)
                    print('numVerify: ', int(numVerify) )
                    
                    if(num != int(numVerify)):
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                        print("網路錯誤:", line + '.txt')
                        print("重新下載: ", line)
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                        ### os.system("python main.py " + line + " --repair")
                        startCrawler(line, "--repair")
                        time.sleep(crawl_stepWaitTime)
                    
                except:
                    print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                    print('打不開 ' + line + '.txt')
                    print("重新下載: ", line)
                    print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                    if os.path.isfile('data/' + line + '.txt'):
                        ###os.system("python main.py " + line + " --repair")
                        startCrawler(line, "--repair")
                    else:
                        ###os.system("python main.py " + line + " --recover")
                        startCrawler(line, "--recover")
                    time.sleep(crawl_stepWaitTime)

            else:
                print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                print('下載: ', line)
                ###os.system("python main.py " + line)
                startCrawler(line, "")
                print('－－－－－－－－－－－－－－－－－－－－－－－－－－')


refCount, repeatCount, disappearCount = 0, 0, 0
if select_condition is 'C':
    part = input('第幾份:')
    f = open('referenceDetail' + part + '000.txt', 'r', encoding='utf-8')
    for detail in f.readlines():
        detail = detail.strip().split(' ')
        idx = detail[0]
        line = detail[1]
        #print('檢查: ', idx, line)
        
        if len(detail) == 3:
            numVerify = detail[2]
            if os.path.isfile('data/' + line + '.txt'):
                ftxt = open('data/' + line + '.txt', 'r', encoding='utf-8')
                ftxtLines = ftxt.readlines()
                ftxt.close()
                for ftxt_idx, ftxt_line in enumerate(ftxtLines):
                    ftxt_line = ftxt_line.strip().split(' ')
                    if ftxt_idx+1 != int(ftxt_line[1]):
                        print('='*10 + '文件有重複爬取' + '='*10)
                        repeatCount += 1
                        print(idx, ' '+line, ' 目前總行數: ', len(ftxtLines), ' 中斷行數: ', ftxt_idx+1, ' <<< ', numVerify)
                        break
            else:
                print('='*10, idx, ' ' + line + '  不存在' + '='*10)
                disappearCount += 1
        else:
            refCount += 1

    f = open('referenceDetail' + part + '000.txt', 'r', encoding='utf-8')





    print('refCount: ', refCount)               ### referenceDetail0000.txt上沒有數目
    print('repeatCount: ', repeatCount)         ### 簡單判斷文件的idx不是連續
    print('disappearCount: ', disappearCount)   ### 還沒抓的文件

