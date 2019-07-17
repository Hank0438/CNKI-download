#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import time, os, shutil, logging, sys
from GetConfig import config
from CrackVerifyCode import crack
from GetPageDetail import page_detail
from urllib.parse import quote
from bs4 import BeautifulSoup

HEADER = config.crawl_headers
# 获取cookie
BASIC_URL = 'http://kns.cnki.net/kns/brief/result.aspx'
# 利用post请求先行注册一次
SEARCH_HANDLE_URL = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
# 发送get请求获得文献资源
GET_PAGE_URL = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename='
# 切换页面基础链接
CHANGE_PAGE_URL = 'http://kns.cnki.net/kns/brief/brief.aspx'


static_post_data = {
    'action': '',
    'NaviCode': '*',
    'ua': '1.21',
    'isinEn': '1',
    'PageName': 'ASP.brief_default_result_aspx',
    'DbPrefix': 'SCOD',
    'DbCatalog': '专利数据总库',
    'ConfigFile': 'SCOD.xml',
    'db_opt': 'SCOD',  # 搜索类别（CNKI右侧的）
    'db_value': '中国专利数据库,国外专利数据库',
    'year_type': 'echar',
    'his': '0',
    '__': time.asctime(time.localtime()) + ' GMT+0800 (中国标准时间)'
}



class SearchTools(object):
    '''
    构建搜索类
    实现搜索方法
    '''

    def __init__(self):
        self.id = -1
        self.session = requests.Session()
        self.repair = 0
        self.recover = 0
        self.userInput = ''
        self.reference_num = ''
        self.repair_num = 0
        self.cur_page_num = 1
        self.left_page_num = 0
        self.total_page_num = 0
        # 保持連線
        self.session.get(BASIC_URL, headers=HEADER)

    def search_reference(self):
        condition_field_list = {
            'txt_1_value1': self.userInput, 
            'txt_1_sel': 'SQR',
            'txt_1_relation': '#CNKI_AND', 
            'txt_1_special1': '='
        }
        source_fields = {}
        userInputParams = {**condition_field_list,**source_fields}
        '''
        第一次发送post请求
        再一次发送get请求,这次请求没有写文献等东西
        两次请求来获得文献列表
        '''
        # 将固定字段与自定义字段组合
        post_data = {**static_post_data, **userInputParams}
        # 必须有第一次请求，否则会提示服务器没有用户
        first_post_res = self.session.post(
            SEARCH_HANDLE_URL, data=post_data, headers=HEADER)
        # get请求中需要传入第一个检索条件的值
        key_value = quote(userInputParams.get('txt_1_value1'))
        self.get_result_url = GET_PAGE_URL + first_post_res.text + '&t=1544249384932&keyValue=' + key_value + '&S=1&sorttype='
        # 检索结果的第一个页面
        second_get_res = self.session.get(self.get_result_url, headers=HEADER)
        '''
        用户选择需要检索的页数
        '''
        reference_num_pattern_compile = re.compile(r'.*?找到&nbsp;(.*?)&nbsp;')
        self.reference_num = re.search(reference_num_pattern_compile,
                                  second_get_res.text).group(1)
        reference_num_int = int(self.reference_num.replace(',', ''))
        # 以每頁20筆計算有多少頁
        self.total_page_num = (reference_num_int // 20) + 1

        totalList = open('totalList.txt', 'a', encoding='utf-8')
        totalList.write(str(self.id) + ' ' + self.userInput + ' ' + self.reference_num + '\n')
        totalList.close()
        print('檢索到' + self.reference_num + '條結果，總共' + str(self.total_page_num) + '頁')



def s2h(seconds):
    '''
    将秒数转为小时数
    '''
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return ("%02d小时%02d分钟%02d秒" % (h, m, s))


f = open('patent', 'r', encoding='utf-8')
for idx, line in enumerate(f.readlines()):
    print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
    time.perf_counter()
    search = SearchTools()
    search.userInput = line.strip()
    search.id = idx+1
    print('下載: ', search.userInput)

    search.search_reference()
    print('－－－－－－－－－－－－－－－－－－－－－－－－－－')

f.close()
print('爬取完毕，共运行：'+s2h(time.perf_counter()))
