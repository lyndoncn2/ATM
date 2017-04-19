#!/usr/bin/env python
#_*_ coding: utf-8 _*_
__author__ = 'Administrator'

import os
import sys
import pymysql
from config import setting

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

#数据库连接信息
def mysqlConn(mysql_config):
    try:
        conn = pymysql.connect(
        host = mysql_config['DATABASE_HOST'],
        port = mysql_config['DATABASE_PORT'],
        user = mysql_config['DATABASE_USER'],
        passwd = mysql_config['DATABASE_PASSWORD'],
        db = mysql_config['DATABASE_NAME'],
        use_unicode=True,
        charset='utf8'
        )
        cur = conn.cursor()
        return cur
    except:
        return 0

#根据用户ID查看个人帐户信息
def getUserCountInfoBaseUserID(id, *args,**kwargs):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2='select * from account_info where id = "{0}"'.format(id)
    cur.execute(SQL2)
    for row in cur.fetchall():
        return row

#根据用户名查看个人帐户信息
def getUserCountInfoBaseUsername(username, *args,**kwargs):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2='select * from account_info where user_name = "{0}"'.format(username)
    cur.execute(SQL2)
    numline = cur.rowcount
    if numline == 0:
        row = ()
        return row
    else:
        for row in cur.fetchall():
            return row

def modiyUserLoginStatus(status, username):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2 = 'update account_info set login_status = "{0}" where user_name = "{1}"'.format(status,username)
    cur.execute(SQL2)

#根据用户ID与类型，对用户余额进行修改
def modifyBalanceBaseAccountID(id, type, money):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2='select * from account_info where id = "{0}"'.format(id)
    cur.execute(SQL2)
    for row in cur.fetchall():
        if type == 'plus':
            balance = row[4] + money
        if type == 'minus':
            balance = row[4] - money
    SQL3='UPDATE account_info set balance = {0}  where id = "{1}"'.format(balance, id)
    cur.execute(SQL3)
    SQL4='select * from account_info where id = "{0}"'.format(id)
    cur.execute(SQL4)
    for row in cur.fetchall():
        if row[4] == balance:
            return 'success'
        else:
            return 'fail'

#获取所有产品信息
def getAllProductInfo():
    productList = []
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2='select * from product_info'
    cur.execute(SQL2)
    for row in cur.fetchall():
        productList.append(row)
    return productList

#根据产品ID，获取产品信息
def getProductInfoBasedOnProductID(id):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2='select * from product_info where id = {0}'.format(id)
    cur.execute(SQL2)
    for row in cur.fetchall():
        return row

#根据购买产品的数量，修改产品信息表中产品剩余
def modifyProductInfoTableBaseOnQuantity(id,num):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2='select * from product_info where id = {0}'.format(id)
    cur.execute(SQL2)
    for row in cur.fetchall():
        QuantityOfProduct =  row[3] - num
    SQL3 = 'UPDATE product_info SET product_remaining_amount = {0} where id = {1}'.format(QuantityOfProduct, id)
    cur.execute(SQL3)
    SQL4 = 'select * from product_info where id = {0}'.format(id)
    cur.execute(SQL4)
    for row in cur.fetchall():
        if row[3] == QuantityOfProduct:
            return "success"
        else:
            return "fail"

#查看购物车内所购买物品的信息
def viewPurchasedProductInformation(userId):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    check_product_info = []
    SQL2='select * from shopping_cart where user_id = {0}'.format(userId)
    cur.execute(SQL2)
    for row in cur.fetchall():
        check_product_info.append(row)
    return check_product_info

#向购物车中添加所购买产品的信息
def addProductToShoppingCart(user_id, product_name, product_price, product_num):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2 = 'insert into shopping_cart (user_id, product_name, product_price, product_amount) values({0}, "{1}", {2}, {3})'.format(user_id,product_name, product_price, product_num)
    cur.execute(SQL2)


#add用户帐单信息
def addBillInfo(id, bill_type, moneyonbill, balance):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    SQL2 = 'insert into account_bill(id,time, bill_type,moneyofbill,balance) values({0},now(), "{1}",{2},{3})'.format(id,bill_type, moneyonbill, balance )
    cur.execute(SQL2)

def getBillInfoBaseUserID(id):
    mysql_config = setting.DATABASE
    cur = mysqlConn(mysql_config)
    bill_info = []
    SQL2 = 'select * from account_bill WHERE id = {0}'.format(id)
    SQL2 = 'select * from account_bill where id = {0}'.format(id)
    cur.execute(SQL2)
    for row in cur.fetchall():
        bill_info.append(row)
    return bill_info



