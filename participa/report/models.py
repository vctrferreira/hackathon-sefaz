from django.db import models
# Create your models here.


class Report(models.Model):

    id_report     = models.IntegerField("Id denuncia")
    user          = models.ForeignKey('auth_sefaz.User')

    type_choices  = (('2', 'Deferido'),('3', 'Indeferido'), ('1','Em processamento'), )
    status        = models.CharField('Status denuncia', max_length=1, choices=type_choices, default='1')

    created_at 	  = models.DateTimeField('Criado em', auto_now_add='true')
    updated_at 	  = models.DateTimeField('Atualizado em', auto_now='true')

    class Meta:
        unique_together = (('id_report', 'user'),)


class MonitoredNFe(models.Model):

    user          = models.ForeignKey('auth_sefaz.User')
    qr_code_data  = models.TextField('QR Code Data')

    type_choices  = (('2', 'Recebido'),('3', 'Reportado'), ('1','Em processamento'), )
    status        = models.CharField('Status denuncia', max_length=1, choices=type_choices, default='1')

    created_at 	  = models.DateTimeField('Criado em', auto_now_add='true')
    updated_at 	  = models.DateTimeField('Atualizado em', auto_now='true')
