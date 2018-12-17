# -*- coding: utf-8 -*-
# @Time : 2018/12/14 下午2:52
# @Author : chengang
# @File : import_action_data.py
# @Function:


# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XServer.settings")

import django

django.setup()

from sport.models import Action
from db_tools.data.action_data import action_list

for row in action_list:

    action = Action()
    action.aid = row['aid']
    action.videoRes = row.get('videoRes')
    action.actionName = row.get('actionName')
    action.doItRight = row.get('doItRight')
    action.breathing = row.get('breathing')
    action.videoSize = row.get('videoSize')
    action.imgCover = row.get('imgCover','')
    action.duration = row.get('duration',)
    action.repeatCount = row.get('repeatCount')
    action.imgLocal = row.get('imgLocal')
    action.save()
