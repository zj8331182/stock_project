import csv
import http.cookiejar
import os
import urllib.request
import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

driver_path = r"/Users/mingzhe.zhang/Downloads/chromedriver"


def get_stock_info():
    url = "http://50.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&" \
          "fid=f3&fs=b:MK0144&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18," \
          "f20,f21,f23,f24,f25,f26,f22,f11,f62,f128,f136,f115,f152"
    response = requests.get(url)
    r_json = response.json()
    data = r_json['data']
    total = data['total']
    diff = []
    for i in range(total // 20):
        diff += get_page_list(i + 1)

    no_list = []
    rows = []
    for item in diff:
        rows.append([item['f14'], item['f12']])

    dir = os.getcwd()

    with open(dir + "/stock.cvs", 'w', newline='') as f:
        writer = csv.writer(f)
        # 写入多行数据
        writer.writerows(rows)

    print(no_list)


def get_page_list(page_no):
    url = "http://50.push2.eastmoney.com/api/qt/clist/get?pn=" \
          + str(page_no) + "&pz=20&po=1&np=1&fltt=2&invt=2&" \
                           "fid=f3&fs=b:MK0144&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18," \
                           "f20,f21,f23,f24,f25,f26,f22,f11,f62,f128,f136,f115,f152"
    print(url)
    diff = []
    try:
        response = requests.get(url)
        r_json = response.json()
        data = r_json['data']
        diff = data['diff']
    except:
        print("error")

    return diff


def download_stock_cvs(code):
    print("downloading")
    url = "https://query1.finance.yahoo.com/v7/finance/download/" \
          + str(code) + ".HK" \
                        "?period1=1471478400&period2=1580601600&interval=1d&events=history&crumb=WwHqk6Hme1l"
    print(url)
    cookie_filename = 'cookie.txt'

    cookie = http.cookiejar.LWPCookieJar(cookie_filename)
    cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    opener = urllib.request.build_opener(handler)  # 通过handler来构建opener

    response = opener.open(url)
    data = response.read()
    with open(str(code) + ".cvs", "wb") as code:
        code.write(data)
    print("download finish")


def get_stock_finance(code):
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection': 'Keep-Alive',
               'Host': 'zhannei.baidu.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    url = "http://stockpage.10jqka.com.cn/HK" \
          + str(code) + \
          "/finance/"
    print(url)
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    jk = soup.find(id="keyindex").string
    print(jk)
    jb = soup.find(id="benefit").string
    print(jb)
    jd = soup.find(id="debt").string
    print(jd)
    jc = soup.find(id="cash").string
    print(jc)
    with open("finance/" + str(code) + "_keyindex.json", "w") as codek:
        codek.write(jk)
    with open("finance/" + str(code) + "_benefit.json", "w") as codeb:
        codeb.write(jb)
    with open("finance/" + str(code) + "_debt.json", "w") as coded:
        coded.write(jd)
    with open("finance/" + str(code) + "_cash.json", "w") as codec:
        codec.write(jc)


def get_stock_price(code):
    datas, price_close_list, price_max_list, price_min_list, price_open_list, volumns, j = request_price(code)

    row = []
    for i in range(len(price_min_list)):
        min_price = int(price_min_list[i])
        row.append([datas[i], min_price, min_price + int(price_open_list[i]),
                    min_price + int(price_max_list[i]), min_price + int(price_close_list[i]), volumns[i]])

    dir = os.getcwd()

    with open(dir + "/prices/" + str(code) + "_" + str(j["start"]) + "_" + str(j["priceFactor"]) + ".cvs", 'w',
              newline='') as f:
        writer = csv.writer(f)
        # 写入多行数据
        writer.writerows(row)


def request_price(code):
    fake_ua = UserAgent()
    headers = {'User-Agent': fake_ua.random, 'Referer': "http://stockpage.10jqka.com.cn/HQ_v4.html"}
    url = "http://d.10jqka.com.cn/v6/line/hk_HK" \
          + str(code) + \
          "/01/all.js"
    print(url)
    response = requests.get(url, headers=headers)
    content = str(response.content)
    content = content.replace("b'quotebridge_v6_line_hk_HK" + str(code) + "_01_all(", "")
    content = content.replace(")'", "")
    content = content.replace("\\\'", "")
    j = json.loads(content)
    price_str = str(j["price"])
    volumn_str = str(j["volumn"])
    dates_str = str(j["dates"])
    prices = price_str.split(",")
    volumns = volumn_str.split(",")
    datas = dates_str.split(",")
    # 最低价，开盘价，最高价，收盘价
    price_min_list = prices[::4]
    price_open_list = prices[1::4]
    price_max_list = prices[2::4]
    price_close_list = prices[3::4]
    return datas, price_close_list, price_max_list, price_min_list, price_open_list, volumns, j


def get_stock_price_date(code, index):
    datas, price_close_list, price_max_list, price_min_list, price_open_list, volumns, j = request_price(code)
    min_price = int(price_min_list[index])
    return min_price + int(price_open_list[index]), min_price + int(price_close_list[index]), min_price + int(
        price_max_list[index]), min_price, volumns[
               index], datas[index]


def get_current_stock_detail(code):
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.122 Safari/537.36",
        'Referer': "https://xueqiu.com/S/" + code,
        'Cookie': 'xq_a_token=a664afb60c7036c7947578ac1a5860c4cfb6b3b5;'}
    url = "https://stock.xueqiu.com/v5/stock/quote.json?symbol=" + code + "&extend=detail"
    response = requests.get(url, headers=headers)
    content = str(response.content)
    print(content)


if __name__ == '__main__':
    get_stock_info()
    # get_stock_price_date("0001", '20200304')
    #
    # f = csv.reader(open('stock.cvs', 'r'))
    # for item in f:
    #     get_stock_price(str(item[1]).replace("0", "", 1))
