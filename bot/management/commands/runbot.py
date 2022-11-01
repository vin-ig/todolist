from django.core.management.base import BaseCommand
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
				tg_client.send_message(chat_id=chat_id, text='Пиши еще!')
				print(item.message)
