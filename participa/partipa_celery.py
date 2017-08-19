from __future__ import absolute_import, unicode_literals

from django.conf import settings

import celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'participa.settings')

app = celery.Celery('participa')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)