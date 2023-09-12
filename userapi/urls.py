from django.urls import path
from .views import Home, EditUserForm, RegisterFormView, LoginFormView, AdminHome, UsersList
from .views import AuthUserListView, RegisterView, AuthUserEditView, LoginViewToken, AdminUsers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import DocumentListView, DocumentDetailView
from django.conf import settings
from django.conf.urls.static import static


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
    path('admin-users/', AdminUsers.as_view(), name='admin-users-list'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:id>', DocumentDetailView.as_view(), name="user-document-detail"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
