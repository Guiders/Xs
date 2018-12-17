# -*- coding: utf-8 -*-
# @Time : 2018/12/16 上午11:17
# @Author : chengang
# @File : move.py
# @Function:

import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XServer.settings")

import django

django.setup()
from sport.models import Program

pgms = Program.objects.filter(challenge__challengeId__isnull=False)
# for pgm in pgms:
#     sportChallengeProgram = ChallengeProgram()
#     sportChallengeProgram.challenge = pgm.challenge
#     sportChallengeProgram.program = pgm.pgmId
#     sportChallengeProgram.save()
#     print('save ', pgm.challenge.challengeId)
