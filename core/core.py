#!/usr/bin/env python
#_*_ coding: utf-8 _*_
__author__ = 'Administrator'

import time
import os
import sys
import io
from prettytable import PrettyTable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from db import connect
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

#装饰取款，存款，转帐，shopping等信息时，判断用户的登录态；
def login_required(func):
    def wrapper(*args,**kwargs):
        user_info = connect.getUserCountInfoBaseUsername(args[0])
        if user_info[5] == 'True':
            return func(*args,**kwargs)
        else:
            login()
            user_info = connect.getUserCountInfoBaseUsername(args[0])
            if user_info[5] == 'True':
                return func(*args,**kwargs)
    return wrapper

#用户登录函数
def login(*args, **kwargs):
    flag = 0
    while flag < 3:
        if len(args) == 0:
            username = input('pelase input your name:').strip()
            passwd = input('please input your password:').strip()
        else:
            username = args[0]
            passwd = args[1]

        user_info = connect.getUserCountInfoBaseUsername(username)
        if len(user_info) == 0 :
            print('no user %s' % (username))
            flag += 1
            continue
        else:
            password = user_info[3]
            if password == passwd:
                connect.modiyUserLoginStatus('True', username)
                return username
            else:
                flag += 1
                if flag < 3:
                    continue
                else:
                    return 'fail'

#基于用户名查询用户信息
@login_required
def check_user_info(username):
    user_info = connect.getUserCountInfoBaseUsername(username)
    table = PrettyTable(['用户ID','用户名是否可用','用户名', '用户余额', '用户登录态'])

    table.align['用户ID'] = "l"
    table.align['用户名是否可用'] = "l"
    table.padding_width = 1
    table.add_row([user_info[0],user_info[1],user_info[2],user_info[4],user_info[5]])
    return table

#取款或者还款
@login_required
def withDrawalsOrRepayMent(username, type, numberOfMoney):
    user_info = connect.getUserCountInfoBaseUsername(username)
    if type == 'minus' and user_info[4] >= numberOfMoney and numberOfMoney %100 == 0:
        connect.addBillInfo(user_info[0], 'withDrawals', numberOfMoney, user_info[4] - numberOfMoney )
        result = connect.modifyBalanceBaseAccountID(user_info[0], type, numberOfMoney)
        return result
    elif type == 'plus':
        connect.addBillInfo(user_info[0], 'repayMent', numberOfMoney, user_info[4] + numberOfMoney )
        result = connect.modifyBalanceBaseAccountID(user_info[0],type,numberOfMoney)
        return result

#购物消费
@login_required
def shoppingConsumption(username, type, numberOfMoney):
    user_info = connect.getUserCountInfoBaseUsername(username)
    if user_info[4] >= numberOfMoney:
        result = connect.modifyBalanceBaseAccountID(user_info[0],'minus',numberOfMoney)
        connect.addBillInfo(user_info[0], 'shopping', numberOfMoney, user_info[4] - numberOfMoney )
        return result
    else:
        return 'fail'

#基于用户查看购买的产吕信息
@login_required
def checkPurchasedProductInformation(username):
    user_info = connect.getUserCountInfoBaseUsername(username)
    result = connect.viewPurchasedProductInformation(user_info[0])
    table = PrettyTable(['userID','productName','productPrice', 'shoppingNumber'])
    table.align['userID'] = 'l'
    table.align['productName'] = 'l'
    table.align['productPrice'] = 'l'
    table.align['shoppingNumber'] = 'l'
    table.padding_width = 1
    for product_line in result:
        table.add_row([product_line[0],product_line[2],product_line[3], product_line[4]])
    return table

#购物
@login_required
def buyProducts(username):
    print('Hello {0}, you can buy these products: '.format(username))
    result = connect.getAllProductInfo()
    table = PrettyTable(['productID','productName','productPrice', 'product_remaining_amount'])
    table.align['productID'] = 'l'
    table.align['productName'] = 'l'
    table.align['productPrice'] = 'l'
    table.align['product_remaining_amount'] = 'l'
    table.padding_width = 1
    for product_line in result:
        table.add_row([product_line[0],product_line[1],product_line[2], product_line[3]])
    print(table)
    buyProductsList = {}
    while True:
        ch = input('Please input B/b(购买) or E/e(退出): ').strip()
        if ch == "B" or ch == 'b':
            buyProductId = input('Please input you want to buy productID: ').strip()
            buyProdubtNumber = input('Please input you want to buy productNumber(多少个/台/条等): ').strip()
            buyProductPrice = connect.getProductInfoBasedOnProductID(buyProductId)[2]
            buyProductsList[buyProductId]=[buyProdubtNumber,buyProductPrice]
        elif ch == "E" or ch == 'e':
            break
        else:
            print('no way, you input error.')
    user_info = connect.getUserCountInfoBaseUsername(username)
    result2 = {}
    result2[user_info[0]] = buyProductsList
    return result2

@login_required
def buyProductsCompute(username, result):
    user_info = connect.getUserCountInfoBaseUsername(username)
    money = 0
    for k,v in result[user_info[0]].items():
        money += float(v[0]) * v[1]
    print(money)
    if user_info[4] >= money:
        flag = 0
        for k,v in result[user_info[0]].items():
            flag += 1
            productID = k
            productBuyNum = v[0]
            productInfo = connect.getProductInfoBasedOnProductID(productID)
            numberOfProductShengYu = productInfo[3]
            if int(productBuyNum) > numberOfProductShengYu:
                return "No enough product to sales."
            else:
                connect.modifyProductInfoTableBaseOnQuantity(productID,int(productBuyNum))
                money1 = float(v[0]) * float(v[1])
                connect.modifyBalanceBaseAccountID(user_info[0], "minus", money1)
                user_info = connect.getUserCountInfoBaseUsername(username)
                shengyu = user_info[4]
                connect.addBillInfo(user_info[0], "shopping",money1 , shengyu)
                product_name = connect.getProductInfoBasedOnProductID(productID)[1]
                connect.addProductToShoppingCart(user_info[0], product_name, v[1], v[0])
    else:
        return "fail, you do not have enough money to buy."

#转帐
@login_required
def transfer(Transcriber, accessor, numberOfMoney):
    user_info = connect.getUserCountInfoBaseUsername(Transcriber)
    if user_info[4] >= numberOfMoney:

        accessor_user_info = connect.getUserCountInfoBaseUsername(accessor)
        if len(accessor_user_info) == 0:
            print('Hi {0}, accont_info has no such person: {1}'.format(user_info[0],accessor_user_info[0] ))
        else:
            result = withDrawalsOrRepayMent(Transcriber, 'minus', numberOfMoney)
            #connect.addBillInfo(user_info[0], 'transfer', numberOfMoney, user_info[4] - numberOfMoney )
            result2 = connect.modifyBalanceBaseAccountID(accessor_user_info[0], 'plus', numberOfMoney)
            connect.addBillInfo(accessor_user_info[0], 'Receipt', numberOfMoney, accessor_user_info[4] + numberOfMoney )
            if result == 'success' and result2 == 'success':
                return 'sucess'
            else:
               return 'fail'
    else:
        result = 'Hello {0}, You do not have enough money to transfer, you have {1} yuan.'

@login_required
def checkBillInfoBaseUsername(username):
    user_info = connect.getUserCountInfoBaseUsername(username)
    user_id = user_info[0]
    result = connect.getBillInfoBaseUserID(int(user_id))
    table = PrettyTable(['UserID','Time','BillType', 'moneyofBill', 'Balance'])
    table.align['UserID'] = 'l'
    table.align['Time'] = 'l'
    table.align['BillType'] = 'l'
    table.align['moneyofBill'] = 'l'
    table.align['Balance'] = 'l'
    table.padding_width = 1
    for i in range(0,len(result)):
            table.add_row([result[i][0],result[i][1],result[i][2],result[i][3],result[i][4]])
    return table

@login_required
def userexit(username):
    user_info = connect.getUserCountInfoBaseUsername(username)
    user_id = user_info[0]
    connect.modiyUserLoginStatus('False', username)

def main():
    MENUS = {
        #"1": ["登陆", login],
        "1": ["查看用户信息",  check_user_info],
        "2": ["取款", withDrawalsOrRepayMent],
        "3": ["还款", withDrawalsOrRepayMent],
        "4": ["转账", transfer],
        "5": ["购物", buyProducts],
        "6": ["查看购物车", checkPurchasedProductInformation], #usernmae
        "7": ["查看帐单信息",checkBillInfoBaseUsername], #username
        "8": ["用户退出登录",userexit]
    }
    username = login()
    while True:
        for num, menu in enumerate(sorted(MENUS)):
            print(num + 1, MENUS[menu][0])

        op_evnet = input("输入要操作的内容:").strip()
        if op_evnet in MENUS:
            if op_evnet in ["1", "6", "7"]:
                print(username + ":")
                print(MENUS[op_evnet][1](username))
            if op_evnet == "2":
                numberOfMoney = int(input("Please input you want to withdraw: ").strip())
                result =  withDrawalsOrRepayMent(username,'minus',numberOfMoney)
                if result == "success":
                    print("Hi {0}, withdraw success.".format(username))
                else:
                    print("Hi {0}, withdraw fail.".format(username))
            if op_evnet == "3":
                numberOfMoney = int(input("Please input you want to repayment: ").strip())
                result =  withDrawalsOrRepayMent(username,'plus',numberOfMoney)
                if result == "success":
                    print("Hi {0}, repayment success.".format(username))
                else:
                    print("Hi {0}, repayment fail.".format(username))
            if op_evnet == "4":
                accessor = input("Who do you want to transfer to? ").strip()
                numberOfMoney = int(input("How much money, you want to transfer: ").strip())
                result = transfer(username, accessor, float(numberOfMoney))
                print(result)
            if op_evnet == "5":
                result = buyProducts(username)
                buyProductsCompute(username, result)
            if op_evnet == "8":
                MENUS[op_evnet][1](username)
                exit("Bye Bye")
        else:
            print("功能未找到")

if __name__ == "__main__":
    main()




