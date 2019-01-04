from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from sport.models import *
from sport.serializers import *

PLAN_WORK_PGM_ID_LIST = [60]


def get_language_version(language_id):
    language = LanguageBase.objects.get(id=language_id)
    return language.version


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

        return Response({'actionList': response.data, "version": get_language_version(request.GET.get('language', 1))})


def changeProgramLanguage(language_id, data):
    for index in LanguageProgram.objects.filter(language_id=language_id):
        for d in data:

            if d.get('pgmId') == index.program.pgmId:
                if index.programName:
                    d['programName'] = index.programName
                if index.programDesc:
                    d['programDesc'] = index.programDesc
                break


class NormalProgramViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = NormalProgramSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = [a.program for a in
                         ProgramSort.objects.all().order_by('position').exclude(
                             program__pgmId__in=PLAN_WORK_PGM_ID_LIST)]
        response = super(NormalProgramViewSet, self).list(request, args, kwargs)

        changeProgramLanguage(request.GET.get('language', 1), response.data)

        # sort_list = [index.get('pgmId') for index in response.data]
        #
        # program_sort_ids = [index.program.pgmId for index in ProgramSort.objects.all().order_by('position')]
        #
        # for index in program_sort_ids:
        #     if index in sort_list:
        #         program_sort_ids.remove()
        #         program_sort_ids.append(index)
        #
        # ressult = []
        # for i in range(0, len(program_sort_ids)):
        #     if i < len(program_sort_ids):
        #         for index in response.data:
        #             if index.get('pgmId') == program_sort_ids[i]:
        #                 ressult[i] = index
        #                 break
        return Response({'workoutList': response.data, "version": get_language_version(request.GET.get('language', 1))})


class ChallengeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = ChallengeSerializer

    def list(self, request, *args, **kwargs):
        print('list')

        self.queryset = [a.challenge for a in ChallengeSort.objects.all().order_by('position')]
        response = super(ChallengeViewSet, self).list(request, args, kwargs)
        language_id = request.GET.get('language', 1)
        for index in LanguageChallenge.objects.filter(language_id=language_id):

            print('x', index.language_id)

            for d in response.data:
                changeProgramLanguage(language_id, d.get('programList'))
                if d.get('challengeId') == index.challenge.challengeId:
                    if index.challengeName:
                        d['challengeName'] = index.challengeName
                    break

        result = {'planList': response.data}
        # 重新设置新的序列化的类
        self.serializer_class = NormalProgramSerializer
        serializer = self.get_serializer(Program.objects.filter(pgmId__in=PLAN_WORK_PGM_ID_LIST), many=True)
        changeProgramLanguage(language_id, serializer.data)
        result['workoutList'] = serializer.data
        result['version'] = get_language_version(language_id)

        return Response(result)
