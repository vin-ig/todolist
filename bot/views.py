import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

from bot.models import TgUser


class BotVerifyView(UpdateAPIView):
	model = TgUser
	permission_classes = [permissions.IsAuthenticated]

	def patch(self, request, *args, **kwargs):
		code = request.data.get('verification_code')
		try:
			tg_user = TgUser.objects.get(verification_code=code)
			tg_user.user = request.user
			tg_user.save()
			return HttpResponse(status=200)
		except ObjectDoesNotExist:
			return JsonResponse({'detail': 'Verification code is invalid'}, status=400)
