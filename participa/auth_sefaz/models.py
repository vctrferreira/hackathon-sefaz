from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

import hashlib
import json
import locale

from datetime import datetime
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

class User(AbstractBaseUser, PermissionsMixin):

	username = models.CharField('Username', max_length=255, unique=True)
	
	nome = models.CharField('Nome completo', max_length=255)
	email = models.EmailField('E-mail', unique=True)
	is_active = models.BooleanField('Está ativo?', default=True, blank=True)
	is_staff = models.BooleanField('É administador?', default=False, blank=True)
	date_joined = models.DateTimeField('Data da Entrada', auto_now_add=True)
	cpf = models.CharField('CPF', max_length=15)
	img_perfil = models.ImageField(upload_to='contas/perfil', verbose_name='Imagem Perfil', default='contas/perfil/user.png')


	type_choices = (('SU', 'Super User'),('C', 'Common User'),)

	user_type = models.CharField('Tipo do usuário', max_length=2, choices=type_choices, default='A')

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.nome or self.email or self.cpf


	def get_short_name(self):
		return self.email


	def get_full_name(self):
		return str(self)


	class Meta():
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'


