# -*- coding: utf-8 -*-
# @Time : 2018/12/13 下午5:53
# @Author : chengang
# @File : adminx.py
# @Function:
from django.http import HttpRequest

import xadmin
from XServer.settings import MEDIA_URL
from xadmin.views import ModelDashboard
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
                    'videoSize', 'open_video', 'show_img_cover', 'show_local_img_cover', ]
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

    def show_local_img_cover(self, instance):
        current_uri = '{scheme}://{host}{media}{img}'.format(scheme=self.request.scheme,
                                                             host=self.request.get_host(), media=MEDIA_URL,
                                                             img=instance.imgLocal)
        return """ <img width="80" height="80" src="{src}">""".format(src=current_uri)

    show_local_img_cover.short_description = "本地封面图"
    show_local_img_cover.allow_tags = True
    show_local_img_cover.is_column = True

    def show_img_cover(self, instance):
        return """ <img width="80" height="80" src="{src}">""".format(src=instance.imgCover)

    show_img_cover.short_description = "远程封面"
    show_img_cover.allow_tags = True
    show_img_cover.is_column = True


class ProgramAdmin(object):
    list_display = ['pgmId', 'programName', 'chargeType', 'slotid', 'totalTime', 'level',
                    'kcal',
                    'pgmType', 'programDesc', 'show_img_cover', 'show_img_big',
                    'restIndexArray', 'restIndexCheck', 'actionIds', 'action_ids_check']
    list_editable = ['pgmId', 'programName', 'chargeType', 'slotid', 'totalTime', 'level', 'kcal',
                     'pgmType', 'programDesc', 'imgCover', 'imgCoverBig', 'restIndexArray', 'actionIds']
    search_fields = ['pgmId', 'programName', 'chargeType', 'slotid', 'totalTime', 'level', 'kcal',
                     'pgmType', 'programDesc', 'imgCover', 'imgCoverBig', 'restIndexArray']
    list_filter = ['pgmId', 'programName', 'chargeType', 'slotid', 'totalTime', 'level', 'kcal',
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
        query_actions = [index.aid for index in Action.objects.filter(aid__in=actionId_int_list).all()]

        result = list(set(actionId_int_list).difference(set(query_actions)))
        if len(result) > 0:
            return """匹配失败 多余的id{ids}""".format(ids=result)
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
    list_display = ['challengeId', 'challengeName', 'chargeType', 'slotid', 'level', 'imgCover', 'show_img_cover',
                    'pgmIds', 'pgmIds_check']
    list_editable = ['challengeId', 'challengeName', 'chargeType', 'slotid', 'level', 'imgCover', 'pgmIds']

    def show_img_cover(self, instance):
        current_uri = '{scheme}://{host}{media}{img}'.format(scheme=self.request.scheme,
                                                             host=self.request.get_host(), media=MEDIA_URL,
                                                             img=instance.imgCover)
        return """ <img width="80" height="80" src="{src}">""".format(src=current_uri)

    show_img_cover.short_description = "封面图"
    show_img_cover.allow_tags = True
    show_img_cover.is_column = True

    def pgmIds_check(self, instance):
        try:
            pgmId_list = [int(index) for index in str(instance.pgmIds).split(";")]
        except Exception as e:
            return e
        query_pgms_ids = [index.pgmId for index in Program.objects.filter(challenge__challengeId=instance.challengeId)]

        query_pgms_ids.sort()
        pgmId_list.sort()
        import operator
        if operator.eq(query_pgms_ids, pgmId_list) is False:
            result = ''
            for id in pgmId_list:
                try:
                    if int(id) not in query_pgms_ids:
                        result += str(id)
                        return """不符合的id:{id}""".format(id=result)
                except:
                    return "id:{id}不是一个整数".format(id=id)

        else:
            return "符合"

    pgmIds_check.short_description = "pgmIds检测"
    pgmIds_check.allow_tags = True
    pgmIds_check.is_column = True

    class ProgramInline(object):
        model = Program
        extra = 1
        style = 'tab'

    inlines = [ProgramInline]


class LanguageBaseAdmin(object):
    list_display = ['language', 'show_link', "version", 'check']
    list_editable = ['language', "version"]
    search_fields = ['language']
    list_filter = ['language']

    def show_link(self, instance):
        apis = ['challenge', 'action', 'program']
        api_map = {'challenge': "挑战课程", 'action': "动作", 'program': "普通课程"}

        a_fmt = """
            <a href="{scheme}://{host}/{api}/?format=json&language={language}" download="{download_name}.json">下载</a>
            <a href="{scheme}://{host}/{api}/?format=json&language={language}">{key}</a>  
            <br/>

        """
        a_fmt_download = """
        """
        result = ''
        for api in apis:
            result += a_fmt.format(scheme=self.request.scheme, host=self.request.get_host(), api=api,
                                   language=instance.id, key=api_map.get(api) + "json",
                                   download_name=instance.language + "_" + api)
            

        return result

    show_link.short_description = "json文件"
    show_link.allow_tags = True
    show_link.is_column = True

    def check(self, instance):
        challenge_count = Challenge.objects.count()
        language_challenge_count = LanguageChallenge.objects.filter(language__language=instance.language).count()
        if challenge_count != language_challenge_count:
            for challenge in Challenge.objects.all():
                LanguageChallenge.objects.update_or_create(language_id=instance.id, challenge_id=challenge.challengeId)

        program_count = Program.objects.count()
        language_program_count = LanguageProgram.objects.filter(language__language=instance.language).count()
        if program_count != language_program_count:
            for program in Program.objects.all():
                LanguageProgram.objects.update_or_create(language_id=instance.id, program_id=program.pgmId)

        action_count = Action.objects.count()
        language_action_count = LanguageAction.objects.filter(language__language=instance.language).count()
        if action_count != language_action_count:
            for action in Action.objects.all():
                LanguageAction.objects.update_or_create(language_id=instance.id, action_id=action.aid)

        return "Checked"

    check.short_description = "Check"
    check.allow_tags = True
    check.is_column = True


class LanguageActionAdmin(object):
    list_display = ['action', 'language', 'actionName', 'doItRight', 'breathing']
    list_editable = ['actionName', 'doItRight', 'breathing']
    search_fields = ['actionName', 'doItRight', 'breathing']
    list_filter = ['action', 'language', 'actionName', 'doItRight', 'breathing']

    # def get_context(self):
    #     context = super(LanguageActionAdmin, self).get_context()
    #     print('get_context')
    #
    #     if 'form' in context:
    #
    #
    #         context['form'].fields['action'].queryset = LanguageAction.objects.filter()
    #     return context


class LanguageProgramAdmin(object):
    list_display = ['program', 'language', 'programName', 'programDesc']
    list_editable = ['programName', 'programDesc']
    search_fields = ['programName']
    list_filter = ['program', 'language', 'programName', 'programDesc']


class LanguageChallengeAdmin(object):
    list_display = ['challenge', 'language', 'challengeName']
    list_editable = ['challengeName']
    search_fields = ['challengeName']
    list_filter = ['challenge', 'language', 'challengeName']


class ImgAdmin(object):
    list_display = ['show_img_cover', 'img', 'imgType']
    list_editable = ['img', ]
    list_filter = ['img', 'imgType']

    def show_img_cover(self, instance):
        current_uri = '{scheme}://{host}{media}{img}'.format(scheme=self.request.scheme,
                                                             host=self.request.get_host(), media=MEDIA_URL,
                                                             img=instance.img)
        return """ <img width="80" height="80" src="{src}">""".format(src=current_uri)

    show_img_cover.short_description = "图片"
    show_img_cover.allow_tags = True
    show_img_cover.is_column = True


class ChallengeSortAdmin(object):
    list_display = ['challenge', 'position']
    list_editable = ['position']
    search_fields = ['challenge', 'position']
    list_filter = ['challenge', 'position']

    def get_context(self):
        context = super(ChallengeSortAdmin, self).get_context()

        if 'form' in context:
            challengeIds = [index.challenge.challengeId for index in ChallengeSort.objects.all()]
            context['form'].fields['challenge'].queryset = Challenge.objects.exclude(challengeId__in=challengeIds)
        return context


class ProgramSortAdmin(object):
    list_display = ['program', 'position']
    list_editable = ['position']
    list_filter = ['program', 'position']

    def get_context(self):
        context = super(ProgramSortAdmin, self).get_context()

        if 'form' in context:
            pgmIds = [index.program.pgmId for index in ProgramSort.objects.all()]
            context['form'].fields['program'].queryset = Program.objects.filter(pgmType=0).exclude(pgmId__in=pgmIds)
        return context


xadmin.site.register(Action, ActionAdmin)
xadmin.site.register(Program, ProgramAdmin)
xadmin.site.register(Challenge, ChallengeAdmin)
xadmin.site.register(LanguageBase, LanguageBaseAdmin)
xadmin.site.register(LanguageAction, LanguageActionAdmin)
xadmin.site.register(LanguageProgram, LanguageProgramAdmin)
xadmin.site.register(LanguageChallenge, LanguageChallengeAdmin)
xadmin.site.register(Image, ImgAdmin)
xadmin.site.register(ChallengeSort, ChallengeSortAdmin)
xadmin.site.register(ProgramSort, ProgramSortAdmin)
