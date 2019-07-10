"""
-------------------------------------------------
   File Name：     GetPageDetail.py
   Description :   获取文献摘要等信息存储至excel
   Author :        Cyrus_Ren
   date：          2018/12/12
-------------------------------------------------
   Change Activity:
                   
-------------------------------------------------
"""
__author__ = 'Cyrus_Ren'

import xlwt
from bs4 import BeautifulSoup
from GetConfig import config
import re
import math,random
from GetConfig import config

HEADER = config.crawl_headers


class PageDetail(object):
    def __init__(self):
        # count用于计数excel行
        self.excel = xlwt.Workbook(encoding='utf8')
        self.sheet = self.excel.add_sheet('專利列表', True)
        self.set_style()
        self.sheet.write(0, 0, '序號', self.basic_style)
        self.sheet.write(0, 1, '專利名稱', self.basic_style)
        self.sheet.write(0, 2, '發明人', self.basic_style)
        self.sheet.write(0, 3, '申請人', self.basic_style)
        self.sheet.write(0, 4, '发表时间', self.basic_style)
        self.sheet.write(0, 5, '別人抓的申請日',self.basic_style)
        self.sheet.write(0, 6, '申請號', self.basic_style)
        self.sheet.write(0, 7, '申請日', self.basic_style)
        self.sheet.write(0, 8, '公開號', self.basic_style)
        self.sheet.write(0, 9, '公開日', self.basic_style)


        # 生成userKey,服务器不做验证
        self.cnkiUserKey=self.set_new_guid()


    def get_detail_page(self, session, result_url, page_url,
                        single_refence_list, download_url):
        '''
        发送三次请求
        前两次服务器注册 最后一次正式跳转
        '''
        # 这个header必须设置
        HEADER['Referer'] = result_url
        self.single_refence_list=single_refence_list
        self.session = session
        self.session.cookies.set('cnkiUserKey', self.cnkiUserKey)
        self.download_url=download_url        

        filename = page_url[page_url.find('filename=')+9:]
        dbCode = 'SCPD'
        
        print("filename: ", filename)
        print("page_url: ", page_url)
        print("download_url: ", download_url)
        # 前两次请求需要的验证参数
        params = {
            'curUrl':'detail.aspx?dbCode=' + dbCode + '&fileName=' + filename,
            'referUrl': result_url+'#J_ORDER&',
            'cnkiUserKey': self.session.cookies['cnkiUserKey'],
            'action': 'file',
            'userName': '',
            'td': '1544605318654'
        }
        # 首先向服务器发送两次预请求
        self.session.get(
            'http://i.shufang.cnki.net/KRS/KRSWriteHandler.ashx',
            headers=HEADER,
            params=params)
        self.session.get(
            'http://kns.cnki.net/KRS/KRSWriteHandler.ashx',
            headers=HEADER,
            params=params)
        page_url = 'http://dbpub.cnki.net/Grid2008/Dbpub/Detail.aspx?DBName=SCPD2010&FileName='+filename
        get_res=self.session.get(page_url,headers=HEADER)
        self.pars_page(get_res.text)
        self.excel.save('data/Reference_detail.xls')


    def pars_page(self,detail_page):
        '''
        解析页面信息
        '''
        soup=BeautifulSoup(detail_page,'lxml')
        box = soup.find('table', id='box')
        checkItem = box.find_all(name='td', class_='checkItem', limit=2)
        self.checkItem = []
        self.date = []
        for t in checkItem:
            self.checkItem.append(t.text)
            date = t.next_sibling.find_next_siblings("td")[1]
            self.date.append(date.text)
        self.wtire_excel()

    def create_list(self):
        '''
        整理excel每一行的数据
        序号 题名 作者 单位 关键字 摘要  来源 发表时间 数据库
        '''
        self.reference_list = []
        for i in range(0,3):
            self.reference_list.append(self.single_refence_list[i])
        for i in range(3,6):
            self.reference_list.append(self.single_refence_list[i])
        self.reference_list.append(self.checkItem[0])
        self.reference_list.append(self.date[0])
        self.reference_list.append(self.checkItem[1])
        self.reference_list.append(self.date[1])

    def wtire_excel(self):
        '''
        将获得的数据写入到excel
        '''
        self.create_list()
        for i in range(0,10):
            self.sheet.write(int(self.reference_list[0]),i,self.reference_list[i],self.basic_style)

    def set_style(self):
        '''
        设置excel样式
        '''
        self.sheet.col(1).width = 256 * 20
        self.sheet.col(2).width = 256 * 20
        self.sheet.col(3).width = 256 * 20
        self.sheet.col(4).width = 256 * 20
        self.sheet.col(5).width = 256 * 20
        self.sheet.col(6).width = 256 * 20
        self.sheet.col(7).width = 256 * 20
        self.sheet.col(8).width = 256 * 20
        self.sheet.col(9).width = 256 * 20
        self.sheet.row(0).height_mismatch=True
        self.sheet.row(0).height = 20*20
        self.basic_style=xlwt.XFStyle()
        al=xlwt.Alignment()
        # 垂直对齐
        al.horz = al.HORZ_CENTER
        # 水平对齐
        al.vert =al.VERT_CENTER
        # 换行
        al.wrap = al.WRAP_AT_RIGHT
        # 设置边框
        borders = xlwt.Borders()
        borders.left = 6
        borders.right = 6
        borders.top = 6
        borders.bottom = 6

        self.basic_style.alignment=al
        self.basic_style.borders=borders



    def set_new_guid(self):
        '''
        生成用户秘钥
        '''
        guid=''
        for i in range(1,32):
            n = str(format(math.floor(random.random() * 16.0),'x'))
            guid+=n
            if (i == 8) or (i == 12) or (i == 16) or (i == 20):
                guid += "-"
        return guid


# 实例化
page_detail = PageDetail()