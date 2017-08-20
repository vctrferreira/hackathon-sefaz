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

    