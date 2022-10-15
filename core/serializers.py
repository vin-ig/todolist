from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer, UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(UserCreatePasswordRetypeSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'email',
			'first_name',
			'last_name',
			'password'
		]

	def __init__(self, *args, **kwargs):
		super(UserCreateSerializer, self).__init__(*args, **kwargs)
		self.fields["password_repeat"] = serializers.CharField(
			style={"input_type": "password"}
		)

	def validate(self, attrs):
		self.fields.pop("password_repeat", None)
		password_repeat = attrs.pop("password_repeat")
		if attrs["password"] == password_repeat:
			return attrs
		else:
			self.fail("password_mismatch")

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


class UpdatePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	@staticmethod
	def validate_new_password(value):
		validate_password(value)
		return value
