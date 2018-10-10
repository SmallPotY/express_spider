# coding=utf-8
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:36:35 2018

@author: SmallPot
"""
import requests
from bs4 import BeautifulSoup
import telnetlib
from socket import *
import time
import threading


def get_ip_list(url, headers):
    ip_list = []
    page = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(page.text, 'lxml')
    ul_list = soup.find_all('tr', limit=100)

    for i in range(1, len(ul_list)):
        line = ul_list[i].find_all('td')

        ip = line[1].text
        port = line[2].text
        http_type = line[5].text
        ip_list.append((http_type, ip, port))

    return ip_list


def get_proxy(api_list):
    for i in api_list:

        print("验证端口:", i)
        try:
            telnetlib.Telnet(i[1], port=i[2], timeout=3)
        except:
            print("不可用")
        else:
            proxy = i[0] + r'://' + i[1] + ':' + i[2]
            print(proxy, "可用")

            with open('proxy.txt', 'a+') as f:
                f.write(proxy + '\n')

        finally:
            pass




def main():
    proxy_url_dl = "http://www.xicidaili.com/wt"
    proxy_url_dl_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',

    }

    api_list = get_ip_list(proxy_url_dl,proxy_url_dl_headers)
    get_proxy(api_list)