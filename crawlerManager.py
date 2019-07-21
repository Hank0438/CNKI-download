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
        startCrawler(line, numVerify, '')
        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
        time.sleep(crawl_stepWaitTime)



if select_condition is 'B':

    # 處理網路錯誤的
    part = input('第幾份:')
    checkLarge = 30000
    f = open('referenceDetail' + part + '000.txt', 'r', encoding='utf-8')
    for detail in f.readlines():
        detail = detail.strip().split(' ')
        idx = detail[0]
        line = detail[1]
        print('檢查: ', idx, line)
        if len(detail) == 3:
            numVerify = detail[2]
            numVerify = int(numVerify.replace(',', ''))
            if numVerify < checkLarge:
                if os.path.isfile('data/' + line + '.txt'):
                    
                    ftxt = open('data/' + line + '.txt', 'r',encoding='utf-8')
                    ftxt_lines = ftxt.readlines()
                    ftxt.close()
                    ftxt_sorted = open('data/' + line + '.txt', 'w',encoding='utf-8')

                    
                    lines = [(fi.strip().split(' ')) for fi in ftxt_lines]
                    sortedLines = sorted(lines, key=lambda x: int(x[1].replace(',', '')) )
                    sortedLinesNoRepeat = []
                    for s in sortedLines:
                        if s not in sortedLinesNoRepeat:
                            sortedLinesNoRepeat.append(s)

                    writeLines = []
                    j = 0 
                    for i in range(numVerify):
                        if i+1 == int(sortedLinesNoRepeat[j][1].replace(',', '') ):
                            writeLines.append(' '.join(sortedLinesNoRepeat[j]) + '\n')
                            if j+1 < len(sortedLinesNoRepeat):
                                j += 1
                        else: 
                            writeLines.append(line + ' ' + str(i+1) + '\n')

                    ftxt_sorted.writelines(writeLines)
                    ftxt_sorted.close()
                    

                    missingPage = []
                    ftxt = open('data/' + line + '.txt', 'r', encoding='utf-8')
                    ftxt_lines = ftxt.readlines()
                    ftxt.close()
                    for i in range(numVerify):
                        if len(ftxt_lines[i].split(' ')) == 2:
                            missingPage.append(str(i+1))  
                    print('(num, numVerify, missingPage): ', len(writeLines), numVerify, len(missingPage))

                    try:
                        if len(missingPage) != 0:
                            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                            print("網路錯誤:", line + '.txt')
                            print("重新下載: ", line)
                            print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                            ### os.system("python main.py " + line + " --repair")
                            startCrawler(line, numVerify, "--repair", missingPage)
                            time.sleep(crawl_stepWaitTime)
                    
                    except:
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                        try:
                            print('打不開 ' + line + '.txt')
                            print("重新下載: ", line)
                            ###os.system("python main.py " + line + " --repair")
                            startCrawler(line, numVerify, "--repair", missingPage)
                            time.sleep(crawl_stepWaitTime)
                        except:
                            print("重新下載錯誤")
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                    
                #print(line, ' ', missingPage)
                
                    
                else:
                    if numVerify > 0:
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
                        try:
                            print('下載: ', line)
                            ###os.system("python main.py " + line)
                            startCrawler(line, numVerify, "", [])
                            time.sleep(crawl_stepWaitTime)
                        except:
                            print('下載錯誤')
                        print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
            else:
                print(line, ' 超過%d筆' % checkLarge)



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
                idx_error = 0
                for file_idx in range(numVerify):
                    if file_idx+1 <= len(ftxtLines):
                        ftxt_line = ftxtLines[file_idx]
                        ftxt_line = ftxt_line.strip().split(' ')
                        ftxt_idx += 1
                        entryCount += 1
                        
                        if ftxt_idx != int(ftxt_line[1]):
                            ftxt_idx = int(ftxt_line[1])

                            ftxt_idxArr.append(ftxt_idx-1)
                            entryCountArr.append(entryCount)
                            entryCount = 0
                            foundRepeat = True

                        if file_idx+1 != int(ftxt_line[1]):
                            idx_error += 1
                    else: 
                        idx_error += 1

                if foundRepeat:
                    ftxt_idxArr.append(ftxt_idx)
                    entryCountArr.append(entryCount)
                    print('-'*5 + '文件有重複爬取' + '-'*5)
                    repeatCount += 1
                    print('段落: ', ftxt_idxArr, '\n連續行數: ', entryCountArr, '\n總行數: ', numVerify, '\n排序缺數:', idx_error)
                        
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
            numVerify = int(numVerify.replace(',', ''))
            
            if numVerify > int(checkLarge):
                countLarge += 1
                print(detail)
    print('countLarge: ', countLarge)