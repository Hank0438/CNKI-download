#!/usr/bin/bash
# -*- coding: utf-8 -*-

import os, shutil, time
from main import startCrawler

crawl_stepWaitTime = 3
select_dict = {
    'A': 'Standard',
    'B': 'Error Recovery',
    'C': 'Check Data',
    'D': 'Check Large',
}
print( '－－－－－－－－－－－－－－－－－－－－－－－－－－' )
print( '請選擇爬蟲模式（單選）：' )
print( ' (A)Standard (B)Error Recovery (C)Check Data (D)Large Crawler' ) 
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
    checkLarge = 1000
    f = open('referenceDetail' + part + '000.txt', 'r', encoding='utf-8')
    for detail in f.readlines():
        detail = detail.strip().split(' ')
        idx = detail[0]
        line = detail[1]
        print('檢查: ', idx, line)
        if len(detail) == 3:
            numVerify = detail[2]
            if int(numVerify.replace(',', '')) < checkLarge:
                if os.path.isfile('data/' + line + '.txt'):
                    try:
                        ftxt = open('data/' + line + '.txt', 'r', encoding='utf-8')
                        ftxt_lines = ftxt.readlines()
                        num = len(ftxt_lines)
                        ftxt.close()
                        print('num: ', num)
                        print('numVerify: ', int(numVerify.replace(',', '')) )
                        
                        if(num < int(numVerify.replace(',', ''))):
                            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                            print("網路錯誤:", line + '.txt')
                            print("重新下載: ", line)
                            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                            ### os.system("python main.py " + line + " --repair")
                            #startCrawler(line, "--repair")
                            time.sleep(crawl_stepWaitTime)
                        
                    except:
                        try:
                            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                            print('打不開 ' + line + '.txt')
                            print("重新下載: ", line)
                            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                            if os.path.isfile('data/' + line + '.txt'):
                                ###os.system("python main.py " + line + " --repair")
                                #startCrawler(line, "--repair")
                                pass
                            else:
                                ###os.system("python main.py " + line + " --recover")
                                #startCrawler(line, "--recover")
                                pass
                            time.sleep(crawl_stepWaitTime)
                        except:
                            print("重新下載錯誤")
                else:
                    if int(numVerify.replace(',', '')) > 0:
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                        print('下載: ', line)
                        ###os.system("python main.py " + line)
                        try:
                            startCrawler(line, "")
                        except:
                            print('下載錯誤')
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
            else:
                print('超過%d筆' % checkLarge)


incompleteCount, refCount, repeatCount, disappearCount = 0, 0, 0, 0
if select_condition is 'C':
    part = input('第幾份:')
    f = open('referenceDetail' + part + '000.txt', 'r', encoding='utf-8')
    for detail in f.readlines():
        detail = detail.strip().split(' ')
        idx = detail[0]
        line = detail[1]
        print('='*10, '檢查: ', idx, line, '='*10)
        
        if len(detail) == 3:
            numVerify = detail[2]
            numVerify = int(numVerify.replace(',', ''))
            if os.path.isfile('data/' + line + '.txt'):
                ftxt = open('data/' + line + '.txt', 'r', encoding='utf-8')
                ftxtLines = ftxt.readlines()
                ftxt.close()
                if numVerify != len(ftxtLines):
                    print('-'*5 + '文件未爬完' + '-'*5)
                    incompleteCount += 1

                entryCount = 0
                entryCountArr = []
                foundRepeat = False
                ftxt_idx = 0
                ftxt_idxArr = []
                for ftxt_line in ftxtLines:
            
                    ftxt_line = ftxt_line.strip().split(' ')
                    ftxt_idx += 1
                    entryCount += 1
                    
                    if ftxt_idx != int(ftxt_line[1]):
                        ftxt_idx = int(ftxt_line[1])

                        ftxt_idxArr.append(ftxt_idx-1)
                        entryCountArr.append(entryCount)
                        entryCount = 0
                        foundRepeat = True

                if foundRepeat:
                    ftxt_idxArr.append(ftxt_idx)
                    entryCountArr.append(entryCount)
                    print('-'*5 + '文件有重複爬取' + '-'*5)
                    repeatCount += 1
                    print('段落: ', ftxt_idxArr, '\n連續行數: ', entryCountArr, '\n總行數: ', numVerify)
                        
            else:
                print('-'*5 + '文件不存在' + '-'*5)
                disappearCount += 1
        else:
            refCount += 1

    print('refCount: ', refCount)               ### referenceDetail0000.txt上沒有數目
    print('repeatCount: ', repeatCount)         ### 簡單判斷文件的idx不是連續
    print('disappearCount: ', disappearCount)   ### 還沒抓的文件
    print('incompleteCount: ', incompleteCount)   ### 還沒抓完的文件





if select_condition is 'D':
    checkLarge = input('超過多少: ')
    f = open('cnki_data/totalList.txt', 'r', encoding='utf-8')
    countLarge = 0
    for detail in f.readlines():
        if detail.strip() != '':
            detail = detail.strip().split(' ')
            idx = detail[0]
            line = detail[1]
        
        if len(detail) == 3:
            numVerify = detail[2]
            
            if int(numVerify.replace(',', '')) > int(checkLarge):
                countLarge += 1
                print(detail)
    print('countLarge: ', countLarge)