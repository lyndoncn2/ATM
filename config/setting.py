__author__ = 'Administrator'
import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

DATABASE = {
    'DATABASE_ENGINE': 'mysql',
    'DATABASE_NAME':  'learing',
    'DATABASE_USER': 'learn',
    'DATABASE_PASSWORD':  'oldboylearing',
    'DATABASE_HOST': '118.193.161.38',
    'DATABASE_PORT':  3306
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'consume':{'action':'minus', 'interest':0},
}