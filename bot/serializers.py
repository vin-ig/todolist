from rest_framework import serializers

from bot.models import TgUser
from core.serializers import RetrieveUpdateSerializer


class BotVerifySerializer(serializers.ModelSerializer):
	# user = RetrieveUpdateSerializer(read_only=True)

	class Meta:
		model = TgUser
		fields = '__all__'
		read_only_fields = ('id', 'tg_id', 'username')

	def update(self, instance, validated_data):
		print(validated_data)
		return instance
