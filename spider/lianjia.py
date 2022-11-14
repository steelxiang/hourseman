import csv
import datetime
import json
import time

import requests
from spider import headers
from lxml import etree

from spider.hourceItem import Item

MAIN_URL = "https://sh.lianjia.com/ershoufang/"
DOMAIN = "https://sh.lianjia.com"
detail_url = []
area_urls = []


# 从区域入口页面获取该区域页码
def getpages(area_url):
    pages=[]
    pages.append(area_url)
    response = requests.get(url=area_url, headers=headers.create_headers())
    html = etree.HTML(response.text)
    try:
        ret = html.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0]
        num=json.loads(ret)["totalPage"]
        for i in range(2,num+1):
            page=area_url+"pg"+str(i)
            pages.append(page)
    except:
        print("-----page error---- "+area_url)
    print(area_url+" 区域共有分页数 "+str(len(pages)))
    return pages



def spider():
    # 从入口页面获取不同区的入口页面
    response = requests.get(url=MAIN_URL, headers=headers.create_headers())
    html = etree.HTML(response.text)
    hrefs = html.xpath('//div[@data-role="ershoufang"]/div/a/@href')
    # 根据区域获取分页
    for href in hrefs:
        data = []
        area_url = DOMAIN + href
        pages = getpages(area_url)
        # 根据分页获取单个页面
        try:
            if len(pages) > 0:
                for page in pages:
                    print("-- crawl page ---" + page)
                    response = requests.get(url= page, headers=headers.create_headers())
                    html = etree.HTML(response.text)
                    urls = html.xpath('//a[@class="noresultRecommend img LOGCLICKDATA"]/@href')
                    for url in urls:
                        item = parse(url)
                        line = str(item).split(",")
                        data.append(line)
                write(data)
        except:
            print(" area error --> "+href)
            continue


def parse(url):
    response = requests.get(url=url, headers=headers.create_headers())
    html = etree.HTML(response.text)
    item = Item()
    item.hid = html.xpath('//div[@class="houseRecord"]/span[@class="info"]/text()')[0].strip()
    item.sumPrice = html.xpath('//span[@class="total"]/text()')[0]
    item.aviPrice = html.xpath('//span[@class="unitPriceValue"]/text()')[0]
    item.model = html.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()')[0]
    item.layer = html.xpath('//div[@class="room"]/div[@class="subInfo"]/text()')[0]
    item.size = html.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()')[0]
    item.year = html.xpath('//div[@class="area"]/div[@class="subInfo noHidden"]/text()')[0].split("年")[0].strip()
    item.cell = html.xpath('//div[@class="communityName"]/a[1]/text()')[0]
    item.area = html.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/text()')[0]
    item.source = "链家"
    item.link = url
    item.type = "二手"
    item.time = datetime.date.today().strftime("%Y-%m-%d")
    print("页面完成 " + url)
    return item


def write(lines):
    header = ['sumPrice', 'aviPrice', 'cell', 'area', 'size', 'model', 'link', 'year', 'layer', 'source', 'time', 'hid',
              'type']
    # flag=True
    with open('../data/data-lianjia.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        # if flag:
        #     writer.writerow(header)
        #     flag=False
        # write the data
        writer.writerows(lines)


if __name__ == '__main__':
    # parse('https://sh.lianjia.com/ershoufang/107105871288.html')
    spider()
    print("************    finish  ******************")
