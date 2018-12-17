# -*- coding: utf-8 -*-
# @Time : 2018/12/14 下午2:52
# @Author : chengang
# @File : import_program_data.py
# @Function:
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "XServer.settings")

import django

django.setup()
from sport.models import Program


# {
#         "programName": "2 - Minute Trial Progress",
#         "pgmId": 60,
#         "chargeType": 0,
#         "totalTime": 120,
#         "kcal": 160,
#         "level": 1,
#         "programDesc": "Welcom to FatGo！You are provided with rich exercise programs which help you achieve different goals. First, let's try the 2-minute Trial Progress, so you can have a idea how amazingly FatGo serves you.  ",
#         "pgmType": 0,
#         "imgCover": "imgs/img_2min.jpg",
#         "imgCoverBig": "http://cdn.download.mpcfiles.info/uploadonly/201811/103/e542a4aea54525169bc811ee5cfce406.jpg",
#         "restIndexArray": "",
#         "actionIds": "80;103;81;100"
#     }

def save_workout(workoutList):
    for row in workoutList:
        program = Program()
        program.pgmId = row['pgmId']
        program.programName = row.get('programName', '')
        program.chargeType = row.get('chargeType', 0)
        program.totalTime = row.get('totalTime', 0)
        program.kcal = row.get('kcal', 0)
        program.level = row.get('level', 1)
        program.programDesc = row.get('programDesc', '')
        program.pgmType = row.get('pgmType', 0)
        program.imgCover = row.get('imgCover', '')
        program.imgCoverBig = row.get('imgCoverBig', '')
        program.restIndexArray = row.get('restIndexArray', '')
        program.actionIds = row.get('actionIds', '')
        program.save()


def set_challenge_id(pgmId, challenge_id):
    pgm = Program.objects.get(pgmId=pgmId)
    pgm.challenge_id = challenge_id
    pgm.save()


if __name__ == '__main__':
    from db_tools.data.workout_data import workoutList
    # 保存workout.json
    save_workout(workoutList)
    from db_tools.data.plan_data import workoutList, planList

    # 保存plan.json 保存workout
    save_workout(workoutList)
    for challenge in planList:
        save_workout(challenge.get("programList", []))

    from db_tools.data.plan_data import workoutList, planList

    #
    # # 保存plan.json 保存workout
    # save_workout(workoutList)
    for challenge in planList:
        for program in challenge.get("programList"):
            set_challenge_id(program.get('pgmId'), challenge.get("challengeId"))
