from django.db import models

from core.models import User


class TgUser(models.Model):
	class Meta:
		verbose_name = 'Пользователь Telegram'
		verbose_name_plural = 'Пользователи Telegram'

	tg_id = models.IntegerField(verbose_name='ID чата')
	username = models.IntegerField(verbose_name='Username пользователя в tg')
	user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
	verification_code = models.CharField(max_length=150, verbose_name='Код верификации')
