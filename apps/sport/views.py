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
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'actionList': serializer.data})


class NormalProgramViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Program.objects.filter(pgmType=0).exclude(pgmId__in=PLAN_WORK_PGM_ID_LIST)
    serializer_class = NormalProgramSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'workoutList': serializer.data})


class ChallengeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pagination_class = None
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        result = {'planList': serializer.data}
        # 重新设置新的序列化的类
        self.serializer_class = NormalProgramSerializer
        serializer = self.get_serializer(Program.objects.filter(pgmId__in=PLAN_WORK_PGM_ID_LIST), many=True)
        result['workoutList'] = serializer.data
        return Response(result)
