# -*- coding: utf-8 -*-
# @Time : 2018/12/17 下午4:10
# @Author : chengang
# @File : get_plan_data.py
# @Function:
from django.forms import model_to_dict

import db_tools.base
from sport.models import Action
import json

actions = Action.objects.all()
result = []
for action in actions:
    item = model_to_dict(action)
    item['imgLocal'] = str(action.imgLocal.__str__())
    print(item)
#     result.append(item)
#
# f = open("action.json", 'w')
# f.write(json.dumps(result))
# print(result)
