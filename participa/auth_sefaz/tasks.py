# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from participa.settings import SEFAZ_APP_TOKEN 
from django.http import JsonResponse
from celery.task import task


def auth_token(f):

    def verify(request, *args, **kwargs):
        # try:
        token = json.loads(str(request.request.body, "utf_8")).get('api_auth_token', None)
        print(token)
        if token == SEFAZ_APP_TOKEN:
            return f(request, *args, **kwargs)
        else:
            return JsonResponse({"status": 401}, status=401)

        # except:
        #     return JsonResponse({"status": 401}, status=401)

    verify.__doc__ = f.__doc__
    verify.__name__ = f.__name__

    return verify

@task(track_started=True, name='task_update_daily_monitoreds')
def update_daily_monitoreds():
    print('heree----------------')