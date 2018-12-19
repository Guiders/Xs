# -*- coding: utf-8 -*-
# @Time : 2018/9/19 下午2:04
# @Author : chengang
# @File : adminx.py
# @Function:

# -*- coding: utf-8 -*-
# @Time : 2018/9/19 下午2:04
# @Author : chengang
# @File : adminx.py
# @Function:

import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "XServer"
    site_footer = "xs"
    # menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "create_time"]


# <link rel="icon" type="image/x-icon" href="favicon.ico"/>


# xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)