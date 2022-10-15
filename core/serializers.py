from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer, \
	UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# class UserRegistrationSerializer(BaseUserRegistrationSerializer):
class UserRegistrationSerializer(UserCreatePasswordRetypeSerializer):
	class Meta:
		model = User
		fields = '__all__'

	def create(self, validated_data):
		user = User.objects.create(**validated_data)
		user.set_password(user.password)
		user.save()
		return user


class RetrieveUpdateSerializer(UserSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'email',
			'first_name',
			'last_name',
		]
