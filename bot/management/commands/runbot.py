import random
import string

from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import env


class Command(BaseCommand):
	def handle(self, *args, **options):
		offset = 0
		tg_client = TgClient(env('TG_BOT_TOKEN'))
		while True:
			res = tg_client.get_updates(offset=offset, timeout=5)
			for item in res.result:
				offset = item.update_id + 1
				chat_id = item.message.chat.id
				if TgUser.objects.filter(tg_id=chat_id):
					text = 'Уже был'
				else:
					verification_code = self._generate_code(5)
					text = f'Привет! Кажется, мы еще не знакомы? Для подтверждения аккаунта ' \
					       f'введи этот код на сайте: *{verification_code}*'
				tg_client.send_message(chat_id=chat_id, text=text)
				print(item.message)

	@staticmethod
	def _generate_code(length):
		letters = string.ascii_uppercase
		return ''.join(random.choice(letters) for i in range(length))
