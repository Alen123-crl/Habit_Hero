from django.urls import path
from .views.user_signup import UserSignUpView
from .views.user_login import LoginView, RefreshTokenView
from .views.user import UserView
from .views.habit import (
    HabitListView,
    HabitDetailView,
    HabitCheckInView,
    HabitAnalyticsView,
    HabitOverviewView,
)

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="user-signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh-token"),
    path("user/me", UserView.as_view(), name="user-detail"),
    path("habits/", HabitListView.as_view(), name="habit-list"),
    path("habits/<int:habit_id>/", HabitDetailView.as_view(), name="habit-detail"),
    path("habits/<int:habit_id>/checkin/", HabitCheckInView.as_view(), name="habit-checkin"),
    path("habits/<int:habit_id>/analytics/", HabitAnalyticsView.as_view(), name="habit-analytics"),
    path("analytics/overview/", HabitOverviewView.as_view(), name="analytics-overview"),
]
