from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import User, RetrieveUpdateSerializer, UpdatePasswordSerializer, LoginSerializer, SignUpSerializer


class SignUpView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer


class UserLoginView(CreateAPIView):
	serializer_class = LoginSerializer

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


class UpdatePasswordView(UpdateAPIView):
	serializer_class = UpdatePasswordSerializer
	model = User
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			if not self.object.check_password(serializer.data.get('old_password')):
				return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
			self.object.set_password(serializer.data.get('new_password'))
			self.object.save()
			return Response(status=status.HTTP_204_NO_CONTENT)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
