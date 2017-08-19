# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from participa.settings import SEFAZ_API_URL
from participa.auth_sefaz.views import ParticipaSefazRequest, BaseView
from participa.auth_sefaz.models import User
from participa.report.models import Report, MonitoredNFe
from rest_framework.renderers import JSONRenderer

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
                return self.success_recive()
        else:
            return self.error_recive()
        


class QRCodeMonitorView(BaseView):

    def post(self, *args, **kwargs):

        data = json.loads(str(self.request.body, "utf_8"))
        user = User.objects.filter(cpf=data.get("cpf", None)).first()
        qr_code_data = data.get("qrcode_data", None)
        if user and qr_code_data:
            monitor = MonitoredNFe(user=user, qr_code_data=qr_code_data)
            monitor.save()
            return self.success_recive()
        else:
            return self.error_recive()

class QRCodeMonitorListView(BaseView):

    def post(self, *args, **kwargs):
        data = json.loads(str(self.request.body, "utf_8"))
        user = User.objects.filter(cpf=data.get("cpf", None)).first()
        if user:
            monitoreds = MonitoredNFe.objects.filter(user=user)
            monitoreds_serialized = dict(monitoreds=list(monitoreds.values('pk', 'status', 'qr_code_data', 'created_at', 'updated_at')))

            return JsonResponse(monitoreds_serialized)
    