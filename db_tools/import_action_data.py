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

from sport.models import Action, LanguageAction
from db_tools.data.action_data import action_list
from db_tools.data.pt_action_data import action_list as pt_action_list


def insert():
    for row in action_list:
        action = Action()
        action.aid = row['aid']
        action.videoRes = row.get('videoRes')
        action.actionName = row.get('actionName')
        action.doItRight = row.get('doItRight')
        action.breathing = row.get('breathing')
        action.videoSize = row.get('videoSize')
        action.imgCover = row.get('imgCover', '')
        action.duration = row.get('duration', )
        action.repeatCount = row.get('repeatCount')
        action.imgLocal = row.get('imgLocal')
        action.save()


def insert_to_translate(action_list,language_id=1):
    for row in action_list:
        print(row['aid'])
        try:
            actionLanguage = LanguageAction.objects.get(action__aid=row['aid'], language_id=language_id)
            actionLanguage.actionName = row.get('actionName')
            actionLanguage.doItRight = row.get('doItRight')
            actionLanguage.breathing = row.get('breathing')
            actionLanguage.save()
            print('save',row['aid'])
        except Exception as e:
            print(e)

if __name__ == '__main__':
    # insert_to_translate(pt_action_list)
    insert_to_translate(action_list,2)
