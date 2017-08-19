# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from participa.settings import SEFAZ_API_URL
from participa.auth_sefaz.views import ParticipaSefazRequest, BaseView
from participa.auth_sefaz.models import User
from participa.report.models import Report, MonitoredNFe

import json


class ReportView(BaseView):

    def get(self):
        pass

    def post(self, *args, **kwargs):
        get_token = self.request.META['HTTP_AUTHORIZATION']
        data = json.loads(str(self.request.body, "utf_8"))
        user = User.objects.filter(cpf=data.get("cpfDestinatario", None)).first()
        if user:
            return_report = self.send_report(json.dumps(data), get_token)
            if return_report:
                report = Report(id_report=return_report.text, user=user)
                report.save()
                return JsonResponse({})
        


class QRCodeMonitorView(BaseView):

    def post(self, *args, **kwargs):
        # {
        #     "api_auth_token": "APP_TOKEN"
        #     "qrcode_data": "qrcode data"
        # }
        data = json.loads(self.request.body)
        user = User.objects.filter(cpf=data.get("cpf", None)).first()
        qrcode_data = data.get("qrcode_data", None)
        if user and qrcode_data:
            monitor = MonitoredNFe(user, qrcode_data)
            monitor.save()
        else:
            pass
