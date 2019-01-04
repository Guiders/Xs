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
from sport.models import LanguageProgram


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


def save():
    from db_tools.data.workout_data import workoutList

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


def insert_translate(workoutList, language_id=1):
    for data in workoutList:
        try:
            language = LanguageProgram.objects.get(program__pgmId=data['pgmId'], language_id=language_id)
            language.programName = data['programName']
            language.programDesc = data['programDesc']
            language.save()
            print('save', data['pgmId'])
        except Exception as e:
            print(e)


def translate_pt():
    from db_tools.data.py_workout_data import workoutList

    insert_translate(workoutList, 1)
    from db_tools.data.pt_plan_data import workoutList, planList

    # 保存plan.json 保存workout
    insert_translate(workoutList, 1)
    for challenge in planList:
        insert_translate(challenge.get("programList", []), 1)


def translate():
    from db_tools.data.workout_data import workoutList

    insert_translate(workoutList, 2)
    from db_tools.data.plan_data import workoutList, planList

    # 保存plan.json 保存workout
    insert_translate(workoutList, 2)
    for challenge in planList:
        insert_translate(challenge.get("programList", []),2)


if __name__ == '__main__':
    translate()
