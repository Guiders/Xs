# -*- coding: utf-8 -*-
# @Time : 2018/12/14 下午2:52
# @Author : chengang
# @File : import_action_data.py
# @Function:
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XServer.settings")

import django

django.setup()

from sport.models import Challenge,LanguageChallenge
from db_tools.data.plan_data import planList
from db_tools.data.pt_plan_data import planList as pt_planList
def save():
    for plan in planList:
        challenge = Challenge()
        challenge.level = plan.get('level', 1)
        challenge.challengeId = plan.get('challengeId')
        challenge.challengeName = plan.get('challengeName', '')
        challenge.imgCover = plan.get('imgCover', '')
        challenge.pgmIds = plan.get('pgmIds', '')
        challenge.save()

def insert_to_translate(planList,language_id=1):
    for row in planList:
        try:
            actionLanguage = LanguageChallenge.objects.get(challenge__challengeId=row['challengeId'], language_id=language_id)
            actionLanguage.challengeName = row.get('challengeName')

            print('save',row['challengeId'])
        except Exception as e:
            print(e)

if __name__ == '__main__':
    insert_to_translate(planList,2)

