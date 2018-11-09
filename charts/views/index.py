#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import auth

from charts.models import PanelCompose

from utils.db_commands import ExecuteSQL
from utils import db_config

class IndexView(View):
    def get(self, request):

        return render(request, 'charts/index.html')


class ChartJsonView(View):
    def get(self, request):
        panel_id = 1
        chart_obj = ComposeIndex.objects.all()[0]
        dis_obj = chart_obj.dis.all()[0]
        mst_obj = chart_obj.mst.all()[0]
        d_value = dis_obj.field
        m_value = mst_obj.field
        m_type = mst_obj.mst_type.value
        t_src = chart_obj.data_src

        m_expression = '{m} as `{alias}`'.format(m = m_type.format(m_value = m_value ), alias = mst_obj.name)

        print(m_expression)

        _sql = 'select {m_expression}, case {d_value} when 1 then "男" when 2 then "女" end as tmp from {t_src} group by {d_value} ;'.format(m_expression = m_expression, t_src = t_src, d_value = d_value)

        print(_sql)

        mysql_conn = db_config.Master_MySQL_DB['test']
        result = ExecuteSQL(mysql_conn, _sql, _type='select')
        print(result)

        chart_name_list = []
        chart_data_list = []
        for r_obj in result:
            r_set = {'name': str(r_obj[1]), 'value': r_obj[0], 'alias': 'test'}
            chart_name_list.append(str(r_obj[1]))
            chart_data_list.append(r_set)

        data = {'chart_name_list': chart_name_list, 'chart_data_list': chart_data_list}

        print(data)

        return HttpResponse(json.dumps(data))