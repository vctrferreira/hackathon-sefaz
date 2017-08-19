from django.conf.urls import url
from .views import ReportView, QRCodeMonitorView, QRCodeMonitorListView
urlpatterns = [
    url('^send/$', ReportView.as_view(), name="report.send_report"),
    url('^qr-code/send/$', QRCodeMonitorView.as_view(), name="report.send_qrcode_monitor"),
    url('^qr-code/list/$', QRCodeMonitorListView.as_view(), name="report.list_qrcode_monitor"),
]