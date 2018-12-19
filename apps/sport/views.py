from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from sport.models import *
from sport.serializers import *

PLAN_WORK_PGM_ID_LIST = [60]


class ActionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def list(self, request, *args, **kwargs):
        response = super(ActionViewSet, self).list(request, args, kwargs)
        for index in LanguageAction.objects.filter(language_id=request.GET.get('language', 1)):
            for d in response.data:
                if d.get('aid') == index.action.aid:
                    if index.actionName:
                        d['actionName'] = index.actionName
                    if index.doItRight:
                        d['doItRight'] = index.doItRight
                    if index.breathing:
                        d['breathing'] = index.breathing
                    break

        return Response({'actionList': response.data})


def changeProgramLanguage(request, data):
    for index in LanguageProgram.objects.filter(language_id=request.GET.get('language', 1)):
        for d in data:
            if d.get('pgmId') == index.program.pgmId:
                d['programName'] = index.programName
                d['programDesc'] = index.programDesc
                break


class NormalProgramViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Program.objects.filter(pgmType=0).exclude(pgmId__in=PLAN_WORK_PGM_ID_LIST)
    serializer_class = NormalProgramSerializer

    def list(self, request, *args, **kwargs):
        response = super(NormalProgramViewSet, self).list(request, args, kwargs)

        changeProgramLanguage(request, response.data)
        return Response({'workoutList': response.data})


class ChallengeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    def list(self, request, *args, **kwargs):
        response = super(ChallengeViewSet, self).list(request, args, kwargs)
        for index in LanguageChallenge.objects.filter(language_id=request.GET.get('language', 1)):
            for d in response.data:
                if d.get('challengeId') == index.challenge.challengeId:
                    if index.challengeName:
                        d['challengeName'] = index.challengeName
                    break

        result = {'planList': response.data}
        # 重新设置新的序列化的类
        self.serializer_class = NormalProgramSerializer
        serializer = self.get_serializer(Program.objects.filter(pgmId__in=PLAN_WORK_PGM_ID_LIST), many=True)
        changeProgramLanguage(request, serializer.data)
        result['workoutList'] = serializer.data

        return Response(result)
