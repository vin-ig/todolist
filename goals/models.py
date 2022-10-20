from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
	class Meta:
		abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

	created = models.DateTimeField(verbose_name="Дата создания")
	updated = models.DateTimeField(verbose_name="Дата последнего обновления")

	def save(self, *args, **kwargs):
		if not self.id:  # Когда модель только создается – у нее нет id
			self.created = timezone.now()
		self.updated = timezone.now()  # Каждый раз, когда вызывается save, проставляем свежую дату обновления
		return super().save(*args, **kwargs)


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


class GoalCategory(DatesModelMixin):
	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"

	title = models.CharField(verbose_name="Название", max_length=255)
	user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
	is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DatesModelMixin):
	class Meta:
		verbose_name = "Цель"
		verbose_name_plural = "Цели"

	title = models.CharField(verbose_name="Название", max_length=255)
	description = models.CharField(verbose_name="Описание", max_length=255)
	user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
	category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT, null=True)
	is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
	status = models.PositiveSmallIntegerField(
		verbose_name="Статус", choices=Status.choices, default=Status.to_do
	)
	priority = models.PositiveSmallIntegerField(
		verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
	)
	due_date = models.DateTimeField(verbose_name="Дата дедлайна")


class GoalComment(DatesModelMixin):
	class Meta:
		verbose_name = "Комментарий"
		verbose_name_plural = "Комментарии"

	text = models.CharField(verbose_name="Текст", max_length=255)
	goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.PROTECT)
	user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
