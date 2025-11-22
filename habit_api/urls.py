from django.urls import path
from .views.user_signup import UserSignUpView
from .views.user_login import LoginView
from .views.user import UserView
urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="user-signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('user/me',UserView.as_view(),name='user-detail'),
]
