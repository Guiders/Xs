# -*- coding: utf-8 -*-
# @Time : 2018/12/13 下午5:53
# @Author : chengang
# @File : adminx.py
# @Function:
from django.http import HttpRequest

import xadmin
from XServer.settings import MEDIA_URL
from .models import *

#
# aid = models.IntegerField(verbose_name='动作id', help_text="动作id")
# videoRes = models.CharField(default='', max_length=200, verbose_name="视频链接", help_text="视频链接")
# actionName = models.CharField(default='', max_length=100, verbose_name="动作名称", help_text="动作名称")
# doItRight = models.CharField(default='', max_length=100, verbose_name="doItRight", help_text="doItRight")
# breathing = models.CharField(default='', max_length=100, verbose_name="breathing", help_text="breathing")
# videoSize = models.IntegerField(default=0, verbose_name="视频大小", help_text="视频大小")
# imgCover = models.CharField(default='', max_length=100, verbose_name="封面图", help_text="封面图")
# duration = models.IntegerField(default=30, verbose_name="单次时长", help_text="单次时长")
# repeatCount = models.IntegerField(default=1, verbose_name="重复次数", help_text="重复次数")
# imgLocal = models.CharField(default='', max_length=100, verbose_name="本地地址", help_text="本地地址"
from xadmin.plugins.actions import BaseActionView

LOCAL_URL = None


class ActionAdmin(object):
    list_display = ['aid', 'actionName', 'duration', 'repeatCount', 'doItRight', 'breathing',
                    'videoSize', 'open_video', 'videoRes', 'show_img_cover', 'imgCover']
    list_editable = ['aid', 'actionName', 'videoRes', 'imgCover', 'duration', 'repeatCount', 'doItRight', 'breathing',
                     'videoSize', 'imgLocal']
    search_fields = ['aid', 'actionName', 'videoRes', 'imgCover', 'duration', 'repeatCount', 'doItRight', 'breathing',
                     'imgLocal']
    list_filter = ['aid', 'actionName', 'videoRes', 'imgCover', 'duration', 'repeatCount', 'doItRight', 'breathing',
                   'imgLocal']

    def open_video(self, instance):
        return """<a href="%s" target="_blank">跳转</a>""" % instance.videoRes

    open_video.short_description = "视频"
    open_video.allow_tags = True
    open_video.is_column = True

    def show_img_cover(self, instance):
        return """ <img width="80" height="80" src="{src}">""".format(src=instance.imgCover)

    show_img_cover.short_description = "远程封面"
    show_img_cover.allow_tags = True
    show_img_cover.is_column = True


class ProgramAdmin(object):
    list_display = ['pgmId', 'programName', 'chargeType', 'totalTime', 'level',
                    'kcal',
                    'pgmType', 'programDesc', 'show_img_cover', 'show_img_big',
                    'restIndexArray', 'restIndexCheck', 'actionIds', 'action_ids_check']
    list_editable = ['pgmId', 'programName', 'chargeType', 'totalTime', 'level', 'kcal',
                     'pgmType', 'programDesc', 'imgCover', 'imgCoverBig', 'restIndexArray', 'actionIds']
    search_fields = ['pgmId', 'programName', 'chargeType', 'totalTime', 'level', 'kcal',
                     'pgmType', 'programDesc', 'imgCover', 'imgCoverBig', 'restIndexArray']
    list_filter = ['pgmId', 'programName', 'chargeType', 'totalTime', 'level', 'kcal',
                   'pgmType', 'programDesc', 'imgCover', 'imgCoverBig', 'restIndexArray']

    def restIndexCheck(self, instance):

        if instance.pgmId < 0:
            return ""

        if len(str(instance.restIndexArray).strip()) <= 0:
            return ""

        actionId_list = str(instance.actionIds).split(";")
        restIndex_list = str(instance.restIndexArray).split(";")
        if len(restIndex_list) <= 0:
            return ""
        actionId_length = len(actionId_list)

        for index in restIndex_list:
            try:
                if int(index) < 0 or int(index) >= actionId_length:
                    return "{index} 越界".format(index=index)
            except:
                return "index error index is:{index}".format(index=index)
        return "符合"

    restIndexCheck.short_description = "休息ids检测"
    restIndexCheck.allow_tags = True
    restIndexCheck.is_column = True

    def action_ids_check(self, instance):

        if instance.pgmId < 0:
            return ""

        actionId_list = str(instance.actionIds).split(";")
        actionId_list = list(set(actionId_list))
        try:
            actionId_int_list = [int(actionId) for actionId in actionId_list]
        except:
            return "actionIds异常，检查一下是否存在有问题id"
        query_actions = Action.objects.filter(aid__in=actionId_int_list).all()

        query_action_num = len(query_actions)
        actionId_list_num = len(actionId_list)
        if query_action_num != actionId_list_num:
            return """匹配失败 动作id数{actionId_list_num}  查询出来的课程:{query_action_num}""".format(
                actionId_list_num=actionId_list_num,
                query_action_num=query_action_num)
        else:
            return """符合"""

    action_ids_check.short_description = "actionIds检测"
    action_ids_check.allow_tags = True
    action_ids_check.is_column = True

    def show_img_cover(self, instance):
        current_uri = '{scheme}://{host}{media}{img}'.format(scheme=self.request.scheme,
                                                             host=self.request.get_host(), media=MEDIA_URL,
                                                             img=instance.imgCover)

        return """ <img width="80" height="80" src="{src}">""".format(src=current_uri)

    show_img_cover.short_description = "封面图"
    show_img_cover.allow_tags = True
    show_img_cover.is_column = True

    # def show_challenge_id(self, instance):
    #     return instance.challenge.challengeId
    #
    # show_challenge_id.short_description = "挑战课程"
    # show_challenge_id.allow_tags = True
    # show_challenge_id.is_column = True

    def show_img_big(self, instance):
        return """ <img width="142" height="216" src="{src}">""".format(src=instance.imgCoverBig)

    show_img_big.short_description = "大图"
    show_img_big.allow_tags = True
    show_img_big.is_column = True


class ChallengeAdmin(object):
    list_display = ['challengeId', 'challengeName', 'level', 'imgCover', 'show_img_cover', 'pgmIds', 'pgmIds_check']
    list_editable = ['challengeId', 'challengeName', 'level', 'imgCover', 'pgmIds']

    def show_img_cover(self, instance):
        current_uri = '{scheme}://{host}{media}{img}'.format(scheme=self.request.scheme,
                                                             host=self.request.get_host(), media=MEDIA_URL,
                                                             img=instance.imgCover)
        return """ <img width="80" height="80" src="{src}">""".format(base=current_uri)

    show_img_cover.short_description = "封面图"
    show_img_cover.allow_tags = True
    show_img_cover.is_column = True

    def pgmIds_check(self, instance):
        pgmId_list = str(instance.pgmIds).split(";")
        query_pgms = Program.objects.filter(challenge__challengeId=instance.challengeId)

        query_pgms_num = len(query_pgms)
        pgmId_list_num = len(pgmId_list)
        real_ids = [item.pgmId for item in query_pgms]
        if query_pgms_num != pgmId_list_num:
            result = ''
            for id in pgmId_list:
                try:
                    if int(id) not in real_ids:
                        result += str(id)
                        return """不符合的id:{id}""".format(id=result)
                except:
                    return "id:{id}不是一个整数".format(id=id)
        else:
            for pgm in query_pgms:
                if pgm.pgmId in pgmId_list is False:
                    return "课程{pgmId} 不在id集合里面".format(pgmId=pgm.pgmId)
            return """符合"""

    pgmIds_check.short_description = "pgmIds检测"
    pgmIds_check.allow_tags = True
    pgmIds_check.is_column = True

    class ProgramInline(object):
        model = Program
        extra = 1
        style = 'tab'

    inlines = [ProgramInline]


class LanguageBaseAdmin(object):
    list_display = ['language']
    list_editable = ['language']
    search_fields = ['language']
    list_filter = ['language']


class LanguageActionAdmin(object):
    list_display = ['action', 'language', 'actionName', 'doItRight', 'breathing']
    list_editable = ['action', 'language', 'actionName', 'doItRight', 'breathing']
    search_fields = ['action', 'language', 'actionName', 'doItRight', 'breathing']
    list_filter = ['action', 'language', 'actionName', 'doItRight', 'breathing']


class LanguageProgramAdmin(object):
    list_display = ['program', 'language', 'programName', 'programDesc']
    list_editable = ['program', 'language', 'programName', 'programDesc']
    search_fields = ['program', 'language', 'programName', 'programDesc']
    list_filter = ['program', 'language', 'programName', 'programDesc']


class LanguageChallengeAdmin(object):
    list_display = ['challenge', 'language', 'challengeName']
    list_editable = ['challenge', 'language', 'challengeName']
    search_fields = ['challenge', 'language', 'challengeName']
    list_filter = ['challenge', 'language', 'challengeName']


xadmin.site.register(Action, ActionAdmin)
xadmin.site.register(Program, ProgramAdmin)
xadmin.site.register(Challenge, ChallengeAdmin)
xadmin.site.register(LanguageBase, LanguageBaseAdmin)
xadmin.site.register(LanguageAction, LanguageActionAdmin)
xadmin.site.register(LanguageProgram, LanguageProgramAdmin)
xadmin.site.register(LanguageChallenge, LanguageChallengeAdmin)
