# -*- coding: utf-8 -*-
# @Time : 2018/12/17 下午4:11
# @Author : chengang
# @File : base.py
# @Function:

import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XServer.settings")

import django

django.setup()
list=[0]*11
list.insert(5,2)
print(list)