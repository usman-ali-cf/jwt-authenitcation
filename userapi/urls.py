from django.urls import path
from .views import Home, EditUserForm, RegisterFormView, LoginFormView, AdminHome
from .views import LoginViewToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import UserViewSet, DocumentViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


route = routers.DefaultRouter()
route.register('user', UserViewSet, basename='user')
route.register('documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path('home/', Home.as_view(), name="home"),
    path('admin-home/', AdminHome.as_view(), name="admin-home"),
    path("login-user/", LoginFormView.as_view(), name="login-user"),
    path("register-user/", RegisterFormView.as_view(), name="register-user"),
    path('edit-user/', EditUserForm.as_view(), name="edit-user"),

    # JWT Authentication urls
    path('user/login/', LoginViewToken.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += route.urls
