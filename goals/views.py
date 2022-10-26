from django.db import transaction
from django_filters import filterset
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals import models
from goals.filters import GoalDateFilter, CategoryBoardFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, CommentPermissions
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalSerializer, \
	GoalCategoryCreateSerializer, CommentSerializer, CommentCreateSerializer, BoardSerializer, BoardCreateSerializer


# Категории
class GoalCategoryCreateView(CreateAPIView):
	model = GoalCategory
	permission_classes = [permissions.IsAuthenticated, GoalCategoryPermissions]  # Check the permissions
	serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
	model = GoalCategory
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = GoalCategorySerializer
	pagination_class = LimitOffsetPagination
	filter_backends = [
		DjangoFilterBackend,
		filters.OrderingFilter,
		filters.SearchFilter,
	]
	ordering_fields = ["title", "created"]
	ordering = ["title"]
	search_fields = ["title"]
	filterset_class = CategoryBoardFilter

	def get_queryset(self):
		return GoalCategory.objects.filter(
			board__participants__user=self.request.user, is_deleted=False
		)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
	model = GoalCategory
	serializer_class = GoalCategorySerializer
	permission_classes = [permissions.IsAuthenticated, GoalCategoryPermissions]

	def get_queryset(self):
		return GoalCategory.objects.filter(
			board__participants__user=self.request.user, is_deleted=False
		)

	def perform_destroy(self, instance):
		instance.is_deleted = True
		for goal in Goal.objects.filter(category=instance.id):
			GoalView().perform_destroy(goal)
		instance.save()
		return instance


# Цели
class GoalCreateView(CreateAPIView):
	model = Goal
	permission_classes = [permissions.IsAuthenticated, GoalPermissions]  # Check the permissions
	serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
	model = Goal
	serializer_class = GoalSerializer
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = LimitOffsetPagination
	ordering_fields = ["due_date"]
	ordering = ["-priority", "due_date"]
	search_fields = ["title", "description"]
	filter_backends = [
		DjangoFilterBackend,
		filters.OrderingFilter,
		filters.SearchFilter,
	]
	filterset_class = GoalDateFilter

	def get_queryset(self):
		return Goal.objects.filter(
			category__board__participants__user=self.request.user, is_deleted=False
		)


class GoalView(RetrieveUpdateDestroyAPIView):
	model = Goal
	serializer_class = GoalSerializer
	permission_classes = [permissions.IsAuthenticated, GoalPermissions]

	def get_queryset(self):
		return Goal.objects.filter(
			category__board__participants__user=self.request.user, is_deleted=False
		)

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.status = 4
		instance.save()
		return instance


# Комментарии
class CommentCreateView(CreateAPIView):
	model = GoalComment
	permission_classes = [permissions.IsAuthenticated, CommentPermissions]  # Не работают пермишены
	serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
	model = GoalComment
	serializer_class = CommentSerializer
	pagination_class = LimitOffsetPagination
	permission_classes = [permissions.IsAuthenticated]
	ordering = ["-created"]
	filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
	filterset_fields = ["goal"]

	def get_queryset(self):
		return GoalComment.objects.filter(user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
	model = GoalComment
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return GoalComment.objects.filter(user=self.request.user)


# Доски
class BoardCreateView(CreateAPIView):
	model = Board
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
	model = Board
	serializer_class = BoardSerializer
	pagination_class = LimitOffsetPagination
	permission_classes = [permissions.IsAuthenticated]
	ordering = ["title"]
	filter_backends = [filters.OrderingFilter]

	def get_queryset(self):
		return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
	model = Board
	permission_classes = [permissions.IsAuthenticated, BoardPermissions]
	serializer_class = BoardSerializer

	def get_queryset(self):
		# Обратите внимание на фильтрацию – она идет через participants
		return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

	def perform_destroy(self, instance: Board):
		# При удалении доски помечаем ее как is_deleted,
		# «удаляем» категории, обновляем статус целей
		with transaction.atomic():
			instance.is_deleted = True
			instance.save()
			instance.categories.update(is_deleted=True)
			Goal.objects.filter(category__board=instance).update(
				status=models.Status.archived
			)
		return instance
