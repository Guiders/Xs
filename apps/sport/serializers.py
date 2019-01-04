# -*- coding: utf-8 -*-
# @Time : 2018/12/17 下午4:20
# @Author : chengang
# @File : serializers.py
# @Function:
from rest_framework import serializers
from sport.models import *


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class NormalProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        exclude = ('challenge',)


class ChallengeSerializer(serializers.ModelSerializer):
    programList = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = '__all__'

    def get_programList(self, obj):
        ids = [int(pgmId) for pgmId in str(obj.pgmIds).split(';')]
        print('result0', ids)
        result = [0] * len(ids)

        programs = Program.objects.filter(pgmId__in=ids)
        print('result1', [index.pgmId for index in programs])
        for program in programs:
            challenge_json = NormalProgramSerializer(program, many=False,
                                                     context={'request': self.context['request']}).data
            result[ids.index(program.pgmId)] = challenge_json
        print('result2', [index.get('pgmId') for index in result])
        return result
