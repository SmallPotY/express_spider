import requests
import json
import datetime
import psycopg2

PG_USERNAME = 'smallpot'
PG_PASSWORD = 'yj'
PG_HOST = '58.63.214.44'
PG_PORT = '5432'
PG_DATABASE = 'express_spider'


def search_by_kuaidi100(url):
    item = {}

    result_state = {
        '0': '在途',
        '1': '揽件',
        '2': '疑难',
        '3': '签收',
        '4': '退签',
        '5': '派件',
        '6': '退回',
    }

    response = requests.get(url)
    result = json.loads(response.text)

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

        print("IP地址被封了")

    conn = psycopg2.connect(database=PG_DATABASE, user=PG_USERNAME, password=PG_PASSWORD, host=PG_HOST,
                            port=PG_PORT)
    cursor = conn.cursor()

    took_time = "'" + item.get('took_time') + "'" if item.get('took_time') else 'Null'
    confirm_time = "'" + item.get('confirm_time') + "'" if item.get('confirm_time') else 'Null'
    last_time = "'" + item.get('last_time') + "'" if item.get('last_time') else 'Null'
    update_time = "'" + item.get('update_time') + "'" if item.get('update_time') else 'Null'
    state = "'" + item.get('state') + "'"
    results = "'" + item.get('results') + "'"
    item_tag = "'" + item.get('item_tag') + "'"
    express_order = "'" + item.get('express_order') + "'"

    SQL = """UPDATE express SET update_time={}, took_time={},confirm_time={},last_time={},state={},item_tag={},results={}
                WHERE express_order={};""".format(update_time, took_time, confirm_time, last_time, state, item_tag,
                                                  results,
                                                  express_order)
    # print(SQL)
    cursor.execute(SQL)
    conn.commit()


    cursor.close()
    conn.close()


if __name__ == '__main__':
    search_by_kuaidi100('http://www.kuaidi100.com/query?type=yuantong&postid=816196183861')