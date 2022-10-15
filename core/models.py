from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
	pass
# 	def create_user(self, username, email, first_name, last_name, password, password_repeat):
# 		if not email:
# 			raise ValueError('Users must have an email address')
# 		user = self.model(
# 			username=username,
# 			email=self.normalize_email(email),
# 			first_name=first_name,
# 			last_name=last_name,
# 			password=password,
# 			password_repeat=password_repeat,
# 		)
# 		user.is_active = True
# 		user.set_password(password)
# 		user.save(using=self._db)
#
# 		return user


class User(AbstractUser):
	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	REQUIRED_FIELDS = ['password', 'last_name']
	objects = UserManager()
