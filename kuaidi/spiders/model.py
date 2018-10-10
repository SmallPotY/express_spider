# coding=utf-8
import psycopg2

PG_USERNAME = 'smallpot'
PG_PASSWORD = 'yj'
PG_HOST = '58.63.214.44'
PG_PORT = '5432'
PG_DATABASE = 'express_spider'


class Express:

    def __init__(self):
        self.conn = psycopg2.connect(database=PG_DATABASE, user=PG_USERNAME, password=PG_PASSWORD, host=PG_HOST,
                                     port=PG_PORT)

    def get_unfinished_random(self, nub):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM express WHERE state<>'签收' AND item_tag<>'ok' ORDER BY RANDOM() LIMIT {}".format(nub)
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [i for i in rows]
        self.conn.close()
        return result

    def insert_proxy(self, proxy, p_ip, p_port,p_http):
        cursor = self.conn.cursor()
        sql = "select proxy FROM proxy WHERE proxy='{}'".format(proxy)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            self.conn.close()
            return False
        else:
            sql = "INSERT INTO proxy (proxy, p_ip,p_port,p_http) VALUES ('{}','{}','{}','{}')".format(proxy, p_ip, p_port,p_http)
            cursor.execute(sql)
            self.conn.commit()
            self.conn.close()
            return True


    def delete_proxy(self,proxy):
        cursor = self.conn.cursor()
        sql = "DELETE FROM proxy WHERE proxy= '{}'".format(proxy)
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def get_proxy(self):
        cursor = self.conn.cursor()
        sql =  "SELECT p_http,p_ip,p_port,proxy FROM proxy"
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [i for i in rows]
        self.conn.close()
        return result

    def updata_proxy(self, proxy):
        cursor = self.conn.cursor()
        sql = "UPDATA  proxy set state='不可用' where proxy='{}'".format(proxy)
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    db = Express()
    item = db.insert_proxy('HTTP://36.7.78.121:59589','36.7.78.121','59589','http')

    # n = db.get_proxy()
    # print(n)