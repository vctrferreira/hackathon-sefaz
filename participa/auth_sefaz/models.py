from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

import locale

from datetime import datetime


class User(AbstractBaseUser, PermissionsMixin):
	
	name = models.CharField('Nome completo', max_length=255)
	is_active = models.BooleanField('Está ativo?', default=True, blank=True)
	is_staff = models.BooleanField('É administador?', default=False, blank=True)
	date_joined = models.DateTimeField('Data da Entrada', auto_now_add=True)
	cpf = models.CharField('CPF', max_length=15, unique=True)
	img_perfil = models.ImageField(upload_to='contas/perfil', verbose_name='Imagem Perfil', default='contas/perfil/user.png')
	type_choices = (('SU', 'Super User'),('C', 'Common User'), )
	user_type = models.CharField('Tipo do usuário', max_length=2, choices=type_choices, default='C')
	objects = UserManager()
	USERNAME_FIELD = 'cpf'

	def __str__(self):
		return self.name or self.cpf

	def get_full_name(self):
		return str(self)

	def get_short_name(self):
		return str(self)

	class Meta():
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'
