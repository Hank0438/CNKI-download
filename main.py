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
        if (self.repair is 0) and (self.recover is 0):
            f = open('data/referenceDetail.txt', 'a', encoding='utf-8')
            f.write(self.userInput + ' ' + self.reference_num + '\n')
            f.close()
        
        if (self.repair is 1):
            ftxt = open('data/' + self.userInput + '.txt', 'r', encoding='utf-8')
            self.repair_num = len(ftxt.readlines())
            ftxt.close()
            self.cur_page_num = (self.repair_num // 20) + 1 
            self.left_page_num = self.total_page_num - self.cur_page_num
            self.get_another_page()
        else:
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
        # 遍历每一行
        #f = open('data/'+ self.userInput +'.txt', 'a', encoding='utf-8')
        #f.write(self.reference_num + '\n')
        for index, tr_info in enumerate(tr_table.find_all(name='tr')):
            #if self.repair is 1:

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
                    #print("filename: ", filename)
                
                # 寫檔
                #f.write(td_text + ' ')
            
            # 在每一行结束后输入一个空行
            #f.write(filename + '\n')

            # 将每一篇文献的信息分组
            single_refence_list = tr_text.split(' ')
            #print('正在下载: ' + single_refence_list[1])
            
            # 是否开启详情页数据抓取
            time.sleep(config.crawl_stepWaitTime)
            page_detail.get_detail_page(self.session, self.get_result_url,
                                            detail_url, single_refence_list, self.userInput)
                

        # self.left_page_num为剩余等待遍历页面
        #print('download_page_left: ', self.left_page_num)
        
        if self.left_page_num > 1:
            self.cur_page_num += 1
            self.get_another_page()

    def get_another_page(self):
        '''
        请求其他页面和请求第一个页面形式不同
        重新构造请求
        '''
        time.sleep(config.crawl_stepWaitTime)
        '''
        curpage_pattern_compile = re.compile(r'.*?curpage=(\d+).*?')
        self.get_result_url = CHANGE_PAGE_URL + re.sub(
            curpage_pattern_compile, '?curpage=' + str(self.cur_page_num),
            self.change_page_url)
        '''
        self.get_result_url = CHANGE_PAGE_URL + '?curpage='  + str(self.cur_page_num) + '&RecordsPerPage=20&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCOD&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx&isinEn=1&'
        #print('self.get_result_url: ', self.get_result_url)
        get_res = self.session.get(self.get_result_url, headers=HEADER)
        self.left_page_num -= 1
        self.parse_page(get_res.text)
        
def s2h(seconds):
    '''
    将秒数转为小时数
    '''
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return ("%02d小时%02d分钟%02d秒" % (h, m, s))

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
    #print('正在检索中.....')
    #print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
    #print('fields', fields)
    return fields

def main():
    time.perf_counter()
    search = SearchTools()
    userInput_counter = 0
    search.userInput = sys.argv[1] 
    userInputParams = get_uesr_inpt(search.userInput)
    if (len(sys.argv) == 3):
        if (sys.argv[2] is '--repair'):
            self.repair = 1
        if (sys.argv[2] is '--recover'):
            self.recover = 1
    search.search_reference(userInputParams)
    #print('－－－－－－－－－－－－－－－－－－－－－－－－－－')
    print('爬取完毕，共运行：'+s2h(time.perf_counter()))


if __name__ == '__main__':
    main()