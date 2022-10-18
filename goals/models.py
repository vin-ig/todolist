from django.db import models
from django.utils import timezone

from core.models import User


class Status(models.IntegerChoices):
	to_do = 1, "К выполнению"
	in_progress = 2, "В процессе"
	done = 3, "Выполнено"
	archived = 4, "Архив"


class Priority(models.IntegerChoices):
	low = 1, "Низкий"
	medium = 2, "Средний"
	high = 3, "Высокий"
	critical = 4, "Критический"


class GoalCategory(models.Model):
	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"

	title = models.CharField(verbose_name="Название", max_length=255)
	user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
	is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
	created = models.DateTimeField(verbose_name="Дата создания")
	updated = models.DateTimeField(verbose_name="Дата последнего обновления")

	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.updated = timezone.now()
		return super().save(*args, **kwargs)


class Goal(models.Model):
	title = models.CharField(verbose_name="Название", max_length=255)
	description = models.CharField(verbose_name="Описание", max_length=255)
	category = models.ManyToManyField(GoalCategory)
	status = models.PositiveSmallIntegerField(
		verbose_name="Статус", choices=Status.choices, default=Status.to_do
	)
	priority = models.PositiveSmallIntegerField(
		verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
	)
	due_date = models.DateTimeField(verbose_name="Дата дедлайна")
	created = models.DateTimeField(verbose_name="Дата создания")
	updated = models.DateTimeField(verbose_name="Дата последнего обновления")

	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.updated = timezone.now()
		return super().save(*args, **kwargs)
