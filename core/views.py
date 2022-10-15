from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import User, RetrieveUpdateSerializer


class UserLoginView(CreateAPIView):
	def post(self, request, *args, **kwargs):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return Response(status=status.HTTP_201_CREATED)

		return Response(data={'password': ['Invalid password']}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = RetrieveUpdateSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

	def delete(self, request, *args, **kwargs):
		logout(request)
		return Response(status=status.HTTP_204_NO_CONTENT)
