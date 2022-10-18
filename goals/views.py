from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalSerializer, GoalCategoryCreateSerializer


# Категории
class GoalCategoryCreateView(CreateAPIView):
	model = GoalCategory
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
	model = GoalCategory
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = GoalCategorySerializer
	pagination_class = LimitOffsetPagination
	filter_backends = [
		filters.OrderingFilter,
		filters.SearchFilter,
	]
	ordering_fields = ["title", "created"]
	ordering = ["title"]
	search_fields = ["title"]

	def get_queryset(self):
		return GoalCategory.objects.filter(
			user=self.request.user, is_deleted=False
		)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
	model = GoalCategory
	serializer_class = GoalCategorySerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return GoalCategory.objects.filter(
			user=self.request.user, is_deleted=False
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
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
	model = Goal
	serializer_class = GoalSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Goal.objects.filter(
			user=self.request.user, is_deleted=False
		)

	# filter_backends = [
	#     DjangoFilterBackend,
	# ]
	# filterset_class = GoalDateFilter


class GoalView(RetrieveUpdateDestroyAPIView):
	model = Goal
	serializer_class = GoalSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Goal.objects.filter(
			user=self.request.user, is_deleted=False
		)

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.status = 4
		instance.save()
		return instance
