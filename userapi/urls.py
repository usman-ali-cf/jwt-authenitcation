from django.urls import path
from .views import Home, EditUserForm, RegisterFormView, LoginFormView, AdminHome, UsersList
from .views import AuthUserListView, RegisterView, AuthUserEditView, LoginViewToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path('home/', Home.as_view(), name="home"),
    path('admin-home/', AdminHome.as_view(), name="admin-home"),
    path('users-list/', UsersList.as_view(), name="users-list"),
    path("login-user/", LoginFormView.as_view(), name="login-user"),
    path("register-user/", RegisterFormView.as_view(), name="register-user"),
    path('edit-user/', EditUserForm.as_view(), name="edit-user"),
    path("users/", AuthUserListView.as_view(), name='users'),
    path("users/<int:id>/", AuthUserEditView.as_view(), name='edit-users'),
    path("user/register", RegisterView.as_view(), name='user-register'),
    path('user/login/', LoginViewToken.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
