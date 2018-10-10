# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KuaidiItem(scrapy.Item):
    # define the fields for your item here like:
    # message = scrapy.Field()    # 返回结果  ['ok','快递公司参数异常：单号不存在或者已经过期','参数错误']
    # state = scrapy.Field()      # 状态
    # data = scrapy.Field()       # 快件信息

    took_time = scrapy.Field()   # 揽收时间
    confirm_time = scrapy.Field()  #签收时间
    last_time = scrapy.Field()   # 最后更新时间
    state = scrapy.Field()   # 快递状态
    results = scrapy.Field()    # 查询结果
    item_tag = scrapy.Field()    # 查询标识
    express_order = scrapy.Field()  # 快递单号
    update_time = scrapy.Field()    # 信息更新时间