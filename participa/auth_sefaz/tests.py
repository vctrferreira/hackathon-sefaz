from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.urls import reverse
from participa.report.views import *
from participa.report.models import MonitoredNFe
from participa.auth_sefaz.models import User

import unittest
import json

class AuthSefazTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

        if not User.objects.filter(cpf="69997292472"):
            User(cpf="69997292472", name="Fulano de tal").save()

        self.headers = {
            "HTTP_AUTHORIZATION": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI4NzE5OTU5OTQwNCIsImF1dGgiOiJST0xFX05GQyIsIm51bVBlc3NvYSI6MSwiaW5kU3RhdHVzIjoiQSIsImlkQXBsaWNhdGl2byI6NiwiaWRBdXRvcml6YWNhbyI6NDAsImV4cCI6MTUxODgyNTYwMH0.YibCkLBubFCcb_IEshYSmQwGgTaKVNifuvoRyWtzIMMM24wiSwJHUr75TPRZI1AHs1-6pp0UWMAR_LpaV7W50g"
        }

    def test_create_user(self):
        User.objects.all().delete()
        data_insert = """  
        {
            "api_auth_token": "APP_TOKEN",
            "cpf": "69997292472",
            "name": "Nome do usuario"
        }
        """

        response = self.client.post(reverse('auth_sefaz.create_user'), data="{}", content_type="application/json")
        self.assertEquals(response.status_code, 401)

        response = self.client.post(reverse('auth_sefaz.create_user'), data=data_insert, content_type="application/json")
        self.assertEquals(response.status_code, 200)

        user_inserted = User.objects.filter(cpf=json.loads(data_insert).get("cpf")).first()

        self.assertEqual(user_inserted.cpf, json.loads(data_insert).get("cpf"))
        self.assertEqual(user_inserted.name, json.loads(data_insert).get("name"))

    def test_facilitate_profile(self):
        data_insert = """  
        {
            "api_auth_token": "APP_TOKEN",
            "cpf": "69997292472"
        }
        """

        response = self.client.post(reverse('auth_sefaz.facilitate_profile'), data="{}", content_type="application/json")
        self.assertEquals(response.status_code, 401)

        response = self.client.post(reverse('auth_sefaz.facilitate_profile'), data=data_insert, **self.headers, content_type="application/json")
        self.assertEquals(response.status_code, 200)

