# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import psycopg2
from twisted.enterprise import adbapi

PG_USERNAME = 'smallpot'
PG_PASSWORD = 'yj'
PG_HOST = '58.63.214.44'
PG_PORT = '5432'
PG_DATABASE = 'express_spider'


class KuaidiPipeline(object):
    def __init__(self):
        self.conn = psycopg2.connect(database=PG_DATABASE, user=PG_USERNAME, password=PG_PASSWORD, host=PG_HOST,
                                     port=PG_PORT)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        took_time = "'" + item.get('took_time') + "'" if item.get('took_time') else 'Null'
        confirm_time = "'" + item.get('confirm_time') + "'" if item.get('confirm_time') else 'Null'
        last_time = "'" + item.get('last_time') + "'" if item.get('last_time') else 'Null'
        update_time = "'" + item.get('update_time') + "'" if item.get('update_time') else 'Null'
        state = "'" + item.get('state') + "'"
        results = "'" + item.get('results') + "'"
        item_tag = "'" + item.get('item_tag') + "'"
        express_order = "'" + item.get('express_order') + "'"

        SQL = """UPDATE express SET update_time={}, took_time={},confirm_time={},last_time={},state={},item_tag={},results={}
                WHERE express_order={};""".format(update_time,took_time, confirm_time, last_time, state, item_tag, results,
                                                  express_order)
        # print(SQL)
        self.cursor.execute(SQL)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
