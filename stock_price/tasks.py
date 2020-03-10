import csv
import os
import sqlite3
from time import sleep

from celery import shared_task

from stock_price.getStockInformation import get_stock_price_date
from stock_price.models import StockPrice


@shared_task
def copy_database():
    conn = sqlite3.connect("./hongkong_stock.db")
    cur = conn.cursor()
    print("open database")
    select_data_sql = """select * from stock_price"""
    cursor = cur.execute(select_data_sql)
    print(str(cursor.arraysize))
    for row in cursor:
        price = StockPrice(number=row[1], open_price=row[2], close_price=row[3],
                           high_price=row[4], low_price=row[5],
                           date=row[6], volume=row[7])
        price.save()
        print(price.date)
    cur.close()
    conn.close()


@shared_task
def sync_price(year, index):
    cwd = str(os.getcwd())
    f = csv.reader(open(cwd + '/stock_price/stock.cvs', 'r'))
    for item in f:
        op, cp, hp, lp, vl, de = get_stock_price_date(str(item[1]).replace("0", "", 1), int(index))
        stock_price = StockPrice(number=str(int(item[1])), date=year + de, open_price=op, close_price=cp, high_price=hp,
                                 low_price=lp, volume=vl)
        sleep(1)
        if StockPrice.objects.filter(number=stock_price.number, date=stock_price.date).count() == 0:
            stock_price.save()
            print("stock " + stock_price.number + " price in " + str(de) + " is " + str(stock_price.close_price))
