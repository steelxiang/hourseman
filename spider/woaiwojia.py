import csv
import datetime
import time

import requests
from spider import headers
from lxml import etree

from spider.hourceItem import Item

MAIN_URL = "https://sh.5i5j.com/ershoufang/"
DOMAIN="https://sh.5i5j.com"



def getPage(url):
    data=[]
    response = requests.get(url=url, headers=headers.create_headers())
    html = etree.HTML(response.text)
    hrefs=html.xpath('//a[@class="cPage"]/@href')
    nextUrl = DOMAIN + hrefs[0]
    urls=geturl(url)
    print("crawl page --> "+url)
    for path in urls:
        try:
            item=parse(DOMAIN+path)
        except:
            print("-----------error--------  " + url)
            continue
        line = str(item).split(",")
        data.append(line)
    write(data)
    if len(urls) >10 :
        getPage(nextUrl)



def geturl(url):
    response = requests.get(url=url, headers=headers.create_headers())
    html = etree.HTML(response.text)
    list = html.xpath('//ul[@class="pList"]/li/div[@class="listImg"]/a/@href')
    return list

def parse(url):
    response = requests.get(url=url, headers=headers.create_headers())
    html = etree.HTML(response.text)
    item = Item()
    item.hid = html.xpath('//span[@class="del-houseid"]/text()')[0].split("：")[-1]
    item.sumPrice = html.xpath('//div[@class="de-price fl"]/span/text()')[0]
    item.aviPrice = html.xpath('//div[@class="danjia"]/span/text()')[0]
    item.model = html.xpath('//div[@class="infocon fyxx-box"]/div[1]/ul/li[1]/span/text()')[0]
    item.layer = html.xpath('//div[@class="infocon fyxx-box"]/div[1]/ul/li[2]/span/text()')[0]
    item.size = html.xpath('//div[@class="infocon fyxx-box"]/div[1]/ul/li[3]/span/text()')[0]
    item.year = html.xpath('//div[@class="infocon fyxx-box"]/div[2]/ul/li[1]/span/text()')[0]
    item.cell = html.xpath('//div[@class="zushous"]/ul/li[1]/a/text()')[0]
    item.area = html.xpath('//div[@class="zushous"]/ul/li[2]/a/text()')[0]
    item.source = "我爱我家"
    item.link = url
    item.type = "二手"
    item.time = datetime.date.today().strftime("%Y-%m-%d")
    print("页面完成 " + url)
    return item


def write(lines):
    header = ['sumPrice', 'aviPrice', 'cell', 'area', 'size', 'model', 'link', 'year', 'layer', 'source', 'time', 'hid',
              'type']
    # flag=True
    with open('../data/data-5i5j.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        # if flag:
        #     writer.writerow(header)
        #     flag=False
        # write the data
        writer.writerows(lines)


if __name__ == '__main__':
    # spider()
    getPage(MAIN_URL)

    print("************    finish  ******************")
