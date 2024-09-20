from django.urls import path

from . import views

urlpatterns = [
    path("", views.Template.as_view(), name="home"),
    path("login", views.LoginView.as_view(), name="login"),
    path("signin", views.SigninView.as_view(), name='signin'),
    # path("signin/flag=true", views.SigninView.as_view(), name='signin'),
    path("signin_completion", views.LoginCompletion.as_view(), name='signin_completion'),
    path("logout_set", views.LogoutSetView.as_view(), name='logout_set'),
    path("logout", views.LogoutView.as_view(), name='logout'),
    path("failed_save", views.FailedTemplate.as_view(), name='failed_save'),
    path("success_save", views.SuccessTemplate.as_view(), name='success_save'),
    path("mypage/<int:pk>", views.MyPage.as_view(), name='mypage'),
]