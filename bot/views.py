import json

from django.http import JsonResponse
from django.views.generic import UpdateView
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView

from bot.models import TgUser
from bot.serializers import BotVerifySerializer


class BotVerifyView(UpdateAPIView):
	model = TgUser
	serializer_class = BotVerifySerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		code = json.load(self.request.body)#.get('verification_code')
		print(code)
		return TgUser.objects.filter(verification_code=self.request.body.verification_code)
	# def patch(self, request, *args, **kwargs):


# def patch(self, request, *args, **kwargs):
	# 	super().post(request, *args, **kwargs)
	#
	# 	data = json.load(request.body)
	# 	verification_code = data.get('verification_code')
	# 	tg_user = self.object.filter(verification_code=verification_code)
	# 	if not tg_user:
	# 		raise ValidationError('Verification code invalid')
	# 	self.object.user = self.request.user
	# 	return JsonResponse({
	# 		"tg_id": self.object.tg_id,
	# 		"username": self.object.username,
	# 		"verification_code": self.object.verification_code,
	# 		"user": self.object.user,
	# 	})
