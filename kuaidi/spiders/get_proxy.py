# coding=utf-8
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:36:35 2018

@author: SmallPot
"""
import requests
from bs4 import BeautifulSoup
import telnetlib
import threading
import random
from kuaidi.kuaidi.spiders import model


def get_ip_list(url, headers):
    ip_list = []

    page = requests.get(url=url, headers=headers)

    # print(page.text)
    soup = BeautifulSoup(page.text, 'lxml')
    ul_list = soup.find_all('tr', limit=100)

    for i in range(1, len(ul_list)):
        line = ul_list[i].find_all('td')

        ip = line[1].text
        port = line[2].text
        http_type = line[5].text
        ip_list.append((http_type, ip, port))

    return ip_list


def get_proxy(i):
    proxy = i[0] + r'://' + i[1] + ':' + i[2]

    # print("验证端口:", i)
    try:
        telnetlib.Telnet(i[1], port=i[2], timeout=5.0)
    except:
        if len(i) == 4:
            db = model.Express()
            db.delete_proxy(proxy)
            print("删除不可用代理", i)
        else:
            print("代理不可用", i)
    else:

        db = model.Express()
        if (db.insert_proxy(proxy, i[1], i[2], i[0])):
            print("获取可用代理：", i)
        else:
            print("重复代理过滤")
    finally:
        pass


def main():
    print("进行新一轮爬取，更新代理IP池")

    n = random.randint(1, 2)

    dl_url = ['http://www.xicidaili.com/wt/{}']

    proxy_url_dl = random.choice(dl_url).format(n)

    proxy_url_dl_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }

    print('获取代理IP池:', proxy_url_dl)
    api_list = get_ip_list(proxy_url_dl, proxy_url_dl_headers)  # 未验证的

    db = model.Express()
    db_list = [i for i in db.get_proxy()]
    api_list = api_list + db_list  # 已有的与新抓取的代理合并

    my_thread = []

    for i in api_list:
        t = threading.Thread(target=get_proxy, args=(i,))
        my_thread.append(t)

    for i in range(len(api_list)):
        my_thread[i].start()

    for i in range(len(api_list)):
        my_thread[i].join()

    db = model.Express()
    db_list = [i[3] for i in db.get_proxy()]

    with open('proxy.txt', 'w+') as f:
        for i in db_list:
            f.write(i + '\n')

    print("代理ip验证完成")


if __name__ == '__main__':
    main()
