from django.urls import path
from .views import Home, EditUserForm
from .views import AuthUserListView, RegisterView, AuthUserEditView, LoginViewToken, LoginFormView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path('home/', Home.as_view(), name="home"),
    path("login-user/", LoginFormView.as_view(), name="login-user"),
    path('edit-user/', EditUserForm.as_view(), name="edit-user"),
    path("users/", AuthUserListView.as_view(), name='users'),
    path("users/<int:id>/", AuthUserEditView.as_view(), name='edit-users'),
    path("users/register", RegisterView.as_view(), name='user-register'),
    path('user/login/', LoginViewToken.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
