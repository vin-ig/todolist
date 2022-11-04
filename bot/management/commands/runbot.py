import random
import string
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from goals.models import Goal, GoalCategory
from todolist.settings import env


class Command(BaseCommand):
	class BotCommands:
		goals = '/goals'
		create = '/create'
		cancel = '/cancel'

	def handle(self, *args, **options):
		offset = 0
		tg_client = TgClient(env('TG_BOT_TOKEN'))
		while True:
			res = tg_client.get_updates(offset=offset, timeout=5)
			for item in res.result:
				offset = item.update_id + 1
				chat_id = item.message.chat.id
				try:
					tg_user = TgUser.objects.get(tg_id=chat_id)
				except ObjectDoesNotExist:
					tg_user = TgUser.objects.create(
						tg_id=chat_id,
						username=item.message.chat.username,
					)
				if not tg_user.user:
					verification_code = self._generate_code(5)
					tg_user.verification_code = verification_code
					tg_user.save()
					text = f'Привет! Кажется, мы еще не знакомы? Для подтверждения аккаунта ' \
					       f'введите этот код на сайте: *{verification_code}*'
				elif item.message.text == self.BotCommands.goals:
					text = self._get_goals(tg_user.user)
				elif item.message.text == self.BotCommands.create:
					offset, text = self._create_goal(client=tg_client, item=item, user=tg_user.user)
				else:
					text = 'Неизвестная команда, попробуйте еще!'

				tg_client.send_message(chat_id=chat_id, text=text)
				print(item.message)

	@staticmethod
	def _generate_code(length):
		letters = string.ascii_uppercase
		return ''.join(random.choice(letters) for i in range(length))

	@staticmethod
	def _get_goals(user):
		goals = Goal.objects.filter(user=user, is_deleted=False)
		return '\n'.join([f'#{i.id}. {i.title}' for i in goals])

	def _create_goal(self, client, item, user):
		categories = GoalCategory.objects.filter(user=user, is_deleted=False)
		cat_list = '\n'.join([f'  - _{i.title}_' for i in categories])
		category_choice = 'Выберите категорию из списка:\n' + cat_list
		client.send_message(chat_id=item.message.chat.id, text=category_choice)

		offset = item.update_id + 1
		while True:
			res = client.get_updates(offset=offset, timeout=5)
			for cat_item in res.result:
				offset = cat_item.update_id + 1
				if cat_item.message.text in [i.title for i in categories]:
					goal_category = GoalCategory.objects.get(title=cat_item.message.text, user=user)
					client.send_message(chat_id=item.message.chat.id, text='Введите название цели:')
					while True:
						get_goal = client.get_updates(offset=offset, timeout=5).result
						if get_goal:
							offset += 1
							break
					goal_title = get_goal[0].message.text
					Goal.objects.create(
						title=goal_title,
						category=goal_category,
						user=user,
						due_date=datetime.date.today() + datetime.timedelta(days=7)
					)
					return offset, 'Цель создана!'
				elif cat_item.message.text == self.BotCommands.cancel:
					return offset, 'Введите команду:'
				else:
					client.send_message(chat_id=item.message.chat.id, text='Неправильная категория. Попробуйте еще!')
