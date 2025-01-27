#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import re
import time, os, shutil, logging, sys
from GetConfig import config
from CrackVerifyCode import crack
from GetPageDetail import page_detail
# 引入字节编码
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
#CHANGE_PAGE_URL = 'http://dbpub.cnki.net/Grid2008/Dbpub/brief.aspx'

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
        self.session = requests.Session()
        self.repair = False
        self.recover = False
        self.userInput = ''
        self.numVerify = 0
        self.reference_num = ''
        self.cur_page_num = 0
        self.left_page_num = 0
        self.total_page_num = 0
        self.startPage = True
        self.missingPage = []
        self.missingPage_idx = 0
        self.getDetail = False
        # 保持連線
        self.session.get(BASIC_URL, headers=HEADER)

    def search_reference(self, ueser_input):
        '''
        第一次发送post请求
        再一次发送get请求,这次请求没有写文献等东西
        两次请求来获得文献列表
        '''
        # 将固定字段与自定义字段组合
        post_data = {**static_post_data, **ueser_input}
        # 必须有第一次请求，否则会提示服务器没有用户
        first_post_res = self.session.post(
            SEARCH_HANDLE_URL, data=post_data, headers=HEADER)
        # get请求中需要传入第一个检索条件的值
        key_value = quote(ueser_input.get('txt_1_value1'))
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

        print('檢索到' + self.reference_num + '條結果，總共' + str(self.total_page_num) + '頁')

        if self.repair:
            self.get_another_page()
        else:
            self.left_page_num = self.total_page_num - self.cur_page_num
            self.parse_page(second_get_res.text)


    def parse_page(self, page_source):
        '''
        保存页面信息
        解析每一页的下载地址
        '''
        soup = BeautifulSoup(page_source, 'lxml')
        # 定位到内容表区域
        tr_table = soup.find(name='table', attrs={'class': 'GridTableContent'})
        # 处理验证码
        try:
            # 去除第一个tr标签（表头）
            tr_table.tr.extract()
        except Exception as e:
            logging.error('出现验证码')
            return self.parse_page(
                self.left_page_num,
                crack.get_image(self.get_result_url, self.session,
                                page_source))
        
        for index, tr_info in enumerate(tr_table.find_all(name='tr')):

            searching_idx = str((index+1) + (self.cur_page_num-1)*20)
            #print('searching_idx: ', searching_idx)
            if self.repair & (searching_idx in self.missingPage) is False:
                ##print('QQ')
                self.getDetail = False
            else:
                self.getDetail = True


            tr_text = ''
            detail_url = ''
            filename = ''
            
            # 遍历每一列
            for index, td_info in enumerate(tr_info.find_all(name='td')):
                
                # 因为一列中的信息非常杂乱，此处进行二次拼接
                td_text = ''
                for string in td_info.stripped_strings:
                    td_text += string
                tr_text += td_text + ' '
                
                # 寻找详情链接
                dt_url = td_info.find('a', attrs={'class': 'fz14'})
                if dt_url:
                    detail_url = dt_url.attrs['href']
                    filename = detail_url[detail_url.find('filename=')+9:]

            # 将每一篇文献的信息分组
            single_refence_list = tr_text.split(' ')
            #print('正在下载: ' + single_refence_list[1])
            
            # 是否开启详情页数据抓取
            if self.getDetail:
                ##print('repair:',self.repair)
                time.sleep(config.crawl_stepWaitTime)
                page_detail.get_detail_page(self.session, self.get_result_url,
                                            detail_url, single_refence_list, self.userInput, self.repair)
            self.getDetail = False

        
        #print('download_page_left: ', self.left_page_num)
        
        self.get_another_page()

    def get_another_page(self):
        #print('cur_page_num: ', self.cur_page_num)
        '''
        请求其他页面和请求第一个页面形式不同
        重新构造请求
        '''
        if self.repair:
            if self.missingPage_idx < len(self.missingPage):
                #print('self.missingPage_idx:', self.missingPage_idx)
                self.repair_num = int(self.missingPage[self.missingPage_idx])
                self.cur_page_num = (self.repair_num // 20) + 1
                self.left_page_num = self.total_page_num - self.cur_page_num
                
                while self.missingPage_idx < len(self.missingPage):
                    if (int(self.missingPage[self.missingPage_idx]) // 20) + 1 != self.cur_page_num:
                        break  
                    self.missingPage_idx += 1
            else:
                self.left_page_num = -1
        else:
            self.cur_page_num += 1
            self.left_page_num -= 1

        #print('self.left_page_num: ', self.left_page_num)
        if self.left_page_num >= 0:
            time.sleep(config.crawl_stepWaitTime)
            self.get_result_url = CHANGE_PAGE_URL + '?curpage='  + str(self.cur_page_num) + '&RecordsPerPage=20&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCOD&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx&isinEn=1&'
            #print('self.get_result_url: ', self.get_result_url)
            get_res = self.session.get(self.get_result_url, headers=HEADER)
            self.parse_page(get_res.text)

        

def get_uesr_inpt(userInput):
    '''
    处理用户所需搜索的全部条件
    '''
    condition_field_list = {
        'txt_1_value1': userInput, 
        'txt_1_sel': 'SQR',
        'txt_1_relation': '#CNKI_AND', 
        'txt_1_special1': '='
    }
    source_fields = {}
    fields={**condition_field_list,**source_fields}
    return fields

def startCrawler(userInput, numVerify, param, missingPage):
    time.perf_counter()
    search = SearchTools()
    userInput_counter = 0
    search.userInput = userInput
    search.numVerify = numVerify
    search.missingPage = missingPage
    userInputParams = get_uesr_inpt(search.userInput)
    if (param == '--repair'):
        search.repair = True
    if (param == '--recover'):
        search.recover = True
    #print('search param:(%d,%d)' % (search.repair, search.recover) )
    search.search_reference(userInputParams)
    print('下載完成')


if __name__ == '__main__':
    startCrawler('扬州亿安电动车有限公司', 6, '', [])