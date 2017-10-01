from django.conf.urls import url
from .views import *
urlpatterns = [
    url('^home-data/$', SefazApiFacilitate.as_view(), name="auth_sefaz.facilitate_profile"),
    url('^create-user/$', SefazApiSetNewUser.as_view(), name="auth_sefaz.create_user"),
    url('^ranking/$', SefazApiRanking.as_view(), name="report.ranking"),
]