#我们先导入相关的库
import socket

import requests
import re
import urllib.parse
import json
import os
from urllib.parse import  urlencode

from datetime import time

from datashape import null


def page_url(name,pages):
    #首先我们得知道，百度图片是动态加载的，我们不能通过静态方法取获取，也就是说不能通过img特征获取，我们需要找到相关规律
    #我们进去百度图片首页 ，搜索你需要搜索的内容，之后点击F12，，查看network栏目，滑动鼠标,你会发现acjson？的单元，点击进去headers
    #把query string parameters复制下来制作成一个字典即可，可以明显看到关键词与页码的位置，我们就可以修改这些页码进行修改了。
    p = 1
    result_urls = []
    temps = []
    y = 1
    while p<pages:
            p = p + 1
            data= {'tn': 'resultjson_com',
                    'ipn': 'rj',
                    'ct': '201326592',
                    'is': '',
                    'fp': 'result',
                    'queryWord': name,
                    'cl': 2,
                    'lm': -1,
                    'ie': 'utf-8',
                    'oe': 'utf-8',
                    'adpicid': '',
                    'st': -1,
                    'z': '',
                    'ic': 0,
                    'word': name,
                    's': '',
                    'se': '',
                    'tab': '',
                    'width': '',
                    'height': '',
                    'face': 0,
                    'istype': 2,
                    'qc': '',
                    'nc': 1,
                    'fr': '',
                    'expermode':'',
                    'pn': p*30,
                    'rn': 30,
                    '1539509973690':''
            }
            url = 'https://image.baidu.com/search/index?'+urlencode(data)
            #'http://image.baidu.com/search/avatarjson?
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            req = urllib.request.Request(url=url, headers=headers)
            page = urllib.request.urlopen(req)
            rsp = page.read().decode('unicode_escape')
            rsp_data = json.loads(rsp)
            if 'data' in rsp_data.keys():
                for items in rsp_data.get('data'):
                    try:
                        #中等图用middleURL，一般图用thumbURL,高清图片好像已经被加密了，
                        # url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                        #     pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
                        #你可以在这个网址的基础上爬取高清图片
                        #分析相对应json，会有objURL这个就可以下载了
                        url = items['middleURL']
                        print(url)

                        save_image(url, name, y)
                        y = y + 1
                        print("已经下载"+str(y)+"图片")
                    except:
                        page.close()
    print("下载结束")

def save_image( url, word,index):
        path = get_path(word)
        picture_path = path+r"//"+str(index)+".jpg"
        with open(picture_path,"wb") as f:
            picture = urllib.request.urlopen(url)
            f.write(picture.read())

            f.close()

def get_path(name):
    cwd = os.getcwd();
    path = cwd+r"//"+str(name);
    if not os.path.exists(path):
        os.makedirs(path)
    return path

if __name__ == '__main__':
    page_url("狮子",4)



