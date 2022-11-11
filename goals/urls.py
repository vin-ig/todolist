from django.urls import path

from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name="category created"),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name="category list"),
    path("goal_category/<pk>", views.GoalCategoryView.as_view(), name="category retrieve/update/delete"),

    path("goal/create", views.GoalCreateView.as_view(), name="goal created"),
    path("goal/list", views.GoalListView.as_view(), name="goal list"),
    path("goal/<pk>", views.GoalView.as_view(), name="goal retrieve/update/delete"),

    path("goal_comment/create", views.CommentCreateView.as_view(), name="comment created"),
    path("goal_comment/list", views.CommentListView.as_view(), name="comment list"),
    path("goal_comment/<pk>", views.CommentView.as_view(), name="comment retrieve/update/delete"),

    path("board/create", views.BoardCreateView.as_view(), name="board created"),
    path("board/list", views.BoardListView.as_view(), name="board list"),
    path("board/<pk>", views.BoardView.as_view(), name="board retrieve/update/delete"),
]
