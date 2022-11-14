import csv
import datetime
import time

import requests
from spider import headers
from lxml import etree

from spider.hourceItem import Item

MAIN_URL = "https://sh.ke.com/ershoufang/"

detail_url = []


def geturl():
    global detail_url
    urls = ['https://sh.ke.com/ershoufang/']
    for i in range(1, 100):
        url = MAIN_URL + "pg" + str(i)
        urls.append(url)
    for url in urls:
        response = requests.get(url=url, headers=headers.create_headers())
        html = etree.HTML(response.text)
        href = html.xpath('//li[@class="clear"]/a/@href')
        detail_url = detail_url + href
    print("url获取完成 一共 {0} 个".format(len(detail_url)))


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
    item.source = "贝壳"
    item.link = url
    item.type = "二手"
    item.time = datetime.date.today().strftime("%Y-%m-%d")
    print("页面完成 " + url)
    return item


def write(lines):
    header = ['sumPrice', 'aviPrice', 'cell', 'area', 'size', 'model', 'link', 'year', 'layer', 'source', 'time', 'hid',
              'type']
    # flag=True
    with open('../data/data.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        # if flag:
        #     writer.writerow(header)
        #     flag=False
        # write the data
        writer.writerows(lines)


def spider():
    geturl()
    count = 0
    data = []
    for url in detail_url:
        count += 1
        # time.sleep(1)
        try:
            item = parse(url)
        except:
            print("-----------error--------  " + url)
            continue
        line = str(item).split(",")
        data.append(line)
        if count % 100 == 0:
            print("---开始写入数据---count == " + str(count))
            write(data)
            data.clear()


if __name__ == '__main__':
    spider()
    print("************    finish  ******************")
