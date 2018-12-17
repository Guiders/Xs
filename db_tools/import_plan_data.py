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

from sport.models import Challenge
from db_tools.data.plan_data import planList

for plan in planList:
    challenge = Challenge()
    challenge.level = plan.get('level', 1)
    challenge.challengeId = plan.get('challengeId')
    challenge.challengeName = plan.get('challengeName', '')
    challenge.imgCover = plan.get('imgCover', '')
    challenge.pgmIds = plan.get('pgmIds', '')
    challenge.save()
