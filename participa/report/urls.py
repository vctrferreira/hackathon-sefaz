from django.conf.urls import url
from .views import ReportView, QRCodeMonitorView
urlpatterns = [
    url('^send/$', ReportView.as_view(), name="report.send_report"),
    url('^qr-code/send/$', QRCodeMonitorView.as_view(), name="report.send_qrcode_monitor"),
]