from django.db import models

from core.models import User


class TgUser(models.Model):
	class Meta:
		verbose_name = 'Пользователь Telegram'
		verbose_name_plural = 'Пользователи Telegram'

	tg_chat_id = models.IntegerField(verbose_name='ID чата')
	tg_uid = models.IntegerField(verbose_name='ID пользователя в tg')
	user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
