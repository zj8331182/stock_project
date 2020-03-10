import json
import os
import sqlite3
import csv


def create_price_db():
    create_table_sql = """create table if not exists stock_price(
id integer primary key autoincrement,
number text,
open_price text,
close_price text,
high_price text,
low_price text,
data text,
volume text)"""
    conn = sqlite3.connect("hongkong_stock.db")
    conn.execute(create_table_sql)
    conn.close()


def create_finance_db():
    create_table_sql = """create table if not exists stock_finance(
id integer primary key autoincrement,
number text,
base_profit_pre_shares text,
net_assets_pre_shares text,
income_pre_shares text,
asset_liability_ratio text,
data text)"""
    conn = sqlite3.connect("hongkong_stock.db")
    conn.execute(create_table_sql)
    conn.close()


def save_list_to_db(price_list):
    conn = sqlite3.connect("hongkong_stock.db")
    cur = conn.cursor()
    insert_data_sql = """INSERT INTO stock_price (number, open_price, close_price, 
    high_price, low_price, data, volume) VALUES("""
    for item in price_list:
        cur.execute(insert_data_sql + item[0] + ", " +
                    item[1] + ", " + item[2] + ", " +
                    item[3] + ", " + item[4] + ", " +
                    item[5] + ", " + item[6] + ")")

    conn.commit()
    cur.close()
    conn.close()


def save_price_data_into_database(file_name):
    price_list = []
    with open("prices/" + file_name, "r") as f:
        year = int(file_name.split("_")[1][0:4])
        print("Year of " + file_name + " is " + str(year))
        code = file_name.split("_")[0]
        # 蛋疼同花顺数据竟然有错的
        # 1717的起始年份早了两年
        if code == '1717':
            year += 2
        current_data = 0
        reader = csv.reader(f)
        result = list(reader)

        for item in result:
            item_data = int(item[0])
            if item_data < current_data:
                year += 1

            current_data = item_data
            if item_data < 1000:
                data_str = str(year) + "0" + str(item_data)
            else:
                data_str = str(year) + str(item_data)
            price_list.append([code, item[2], item[4], item[3], item[1], data_str, item[5]])

        save_list_to_db(price_list)


def save_finance_list_to_db(finance_list):
    print(finance_list)
    conn = sqlite3.connect("hongkong_stock.db")
    cur = conn.cursor()
    insert_data_sql = """INSERT INTO stock_finance (number, base_profit_pre_shares, net_assets_pre_shares, 
       income_pre_shares, asset_liability_ratio, data) VALUES("""
    for item in finance_list:
        sql_str = insert_data_sql + item[0] + ", " + item[1] + ", " + item[2] + ", " + item[3] + ", " + item[4] + ", " + \
                  item[5] + ")"
        cur.execute(sql_str)

    conn.commit()
    cur.close()
    conn.close()


def save_finance_data_into_database(file_name):
    num = file_name.split("_")[0]
    finance_list = []
    with open("finance/" + file_name, "r") as f:
        file_json = json.load(f)
    report_list = file_json["report"]
    date_list = report_list[0]
    profit_lit = report_list[1]
    income_list = report_list[7]
    asset_list = report_list[8]
    liability_list = report_list[10]
    for i in range(0, len(date_list)):
        date = str(date_list[i]).replace("-", "")
        profit = deal_data(profit_lit[i])
        asset = deal_data(asset_list[i])
        income = deal_data(income_list[i])
        liability = deal_data(liability_list[i])
        finance_list.append([num, profit, asset, income, liability, date])

    save_finance_list_to_db(finance_list)


def deal_data(data):
    if data == "":
        profit = "null"
    else:
        profit = data
    return profit


def copy_data():
    conn = sqlite3.connect("hongkong_stock.db")
    cur = conn.cursor()
    print("open database")
    select_data_sql = """select * from stock_price"""
    cursor = cur.execute(select_data_sql)
    for row in cursor:
        price = [row[1], row[2], row[3], row[4], row[5],
                 row[6], row[7]]
        print(price)
    cur.close()
    conn.close()


if __name__ == '__main__':
    # create_price_db()
    file_list = os.listdir('prices')
    for file in file_list:
        save_price_data_into_database(file.title())
