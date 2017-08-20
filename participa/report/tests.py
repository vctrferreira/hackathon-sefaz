from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.urls import reverse
from participa.report.views import *
from participa.report.models import MonitoredNFe
from participa.auth_sefaz.models import User

import unittest
import json

class ReportTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

        if not User.objects.filter(cpf="69997292472"):
            User(cpf="69997292472", name="Fulano de tal").save()

        self.headers = {
            "HTTP_AUTHORIZATION": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI4NzE5OTU5OTQwNCIsImF1dGgiOiJST0xFX05GQyIsIm51bVBlc3NvYSI6MSwiaW5kU3RhdHVzIjoiQSIsImlkQXBsaWNhdGl2byI6NiwiaWRBdXRvcml6YWNhbyI6NDAsImV4cCI6MTUxODgyNTYwMH0.YibCkLBubFCcb_IEshYSmQwGgTaKVNifuvoRyWtzIMMM24wiSwJHUr75TPRZI1AHs1-6pp0UWMAR_LpaV7W50g"
        }

    def test_send_report(self):

        data = """ 
        {
            "cNF": 987,
            "cnpjDestinatario": "09326760000168",
            "cnpjEmitente": "09326760000168",
            "cpfDestinatario": "69997292472",
            "dataEmissao": "16/08/2017",
            "denuncia": "Uma denúncia",
            "numeroECF": "123456789",
            "serie": "A",
            "situacao": "Pendente",
            "subSerie": 1,
            "tipoDenuncia": "1",
            "tipoDocumento": "NFe",
            "valor": 123.45,
            "api_auth_token": "APP_TOKEN"
        }
        """

        response = self.client.post(reverse('report.send_report'), data="{}", **self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 401)

        response = self.client.post(reverse('report.send_report'), data=data, **self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_qrcode_monitor(self):
        MonitoredNFe.objects.all().delete()
        data_insert = """
        {
            "api_auth_token": "APP_TOKEN",
            "cpf": "69997292472",
            "qrcode_data": "qrcode data"
        }
        """

        response = self.client.post(reverse('report.send_qrcode_monitor'), data="{}", **self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 401)

        response = self.client.post(reverse('report.send_qrcode_monitor'), data=data_insert, **self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        data_list = """
        {
            "api_auth_token": "APP_TOKEN",
            "cpf": "69997292472"
        }
        """

        response = self.client.post(reverse('report.list_qrcode_monitor'), data="{}", **self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 401)

        response = self.client.post(reverse('report.list_qrcode_monitor'), data=data_list, **self.headers, content_type="application/json")
        self.assertEqual(response.json()["monitoreds"][0]["qr_code_data"], json.loads(data_insert).get("qrcode_data"))
        self.assertEqual(response.json()["monitoreds"][0]["status"], "1")
        self.assertEqual(response.status_code, 200)
    