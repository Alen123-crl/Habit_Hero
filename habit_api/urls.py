from django.urls import path
from .views.user_signup import UserSignUpView
from .views.user_login import LoginView

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="user-signup"),
    path("login/", LoginView.as_view(), name="login"),
]
