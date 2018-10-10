# -*- coding: utf-8 -*-
import scrapy
from . import model
from ..items import KuaidiItem
import json
import datetime
from . import get_proxy
import time
from . import search_url


class Kuaidi100Spider(scrapy.Spider):
    name = 'kuaidi100'
    allowed_domains = ['http://www.kuaidi100.com/']

    # start_urls = []     # 改写了start_requests函数后无需要再指定start_urls
    query_url = "http://www.kuaidi100.com/query?type={}&postid={}"

    def parse(self, response):
        result = json.loads(response.text)
        item = KuaidiItem()

        result_state = {
            '0': '在途',
            '1': '揽件',
            '2': '疑难',
            '3': '签收',
            '4': '退签',
            '5': '派件',
            '6': '退回',
        }

        item['item_tag'] = result['message']
        if item['item_tag'] == 'ok':
            item['state'] = result_state[result['state']]
            item['last_time'] = result.get('data', [''])[0]['time']
            item['took_time'] = result.get('data', [''])[-1]['time']
            item['results'] = result.get('data', [''])[0]['context']
            item['express_order'] = result.get('nu', '')
            item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if item['state'] == '签收':
                item['confirm_time'] = result.get('data', None)[-1]['time']
            else:
                item['confirm_time'] = ''
        elif item['item_tag'] == '非法访问:IP禁止访问':
            print("IP地址ban")
        yield item

    def start_requests(self):
        # 动态生成url

        get_proxy.main()
        global_count = 0
        switch = True

        while switch:

            """更新代理IP池"""

            global_count += 1
            if global_count > 5:
                get_proxy.main()
                global_count = 0

            db = model.Express()

            item = db.get_unfinished_random(100)  # 获取随机n条未查询的快递信息

            print("随机获取未签收记录： ", len(item), " 条")
            urls = []

            if len(item) == 0:
                print("**********************暂无需爬取的记录*****************************")
                switch = False
                break

            for i in item:
                url = self.query_url.format(i[3], i[2])
                urls.append(url)

            for url in urls:
                print("当前爬取URL：", url)
                yield scrapy.Request(url)
                # yield scrapy.Request(url, meta={'proxy': 'http://122.112.252.167:8080'})

            # 少于20条使用本机ip辅助爬
            if len(item) < 20:
                for url in urls:
                    print("当前为本机ip爬取")
                    time.sleep(2)
                    search_url.search_by_kuaidi100(url)
