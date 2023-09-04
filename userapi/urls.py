from django.urls import path
from .views import home
from .views import AuthUserListView, RegisterView, AuthUserEditView, LoginViewToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", home, name="home"),
    path('home/', home, name="home"),
    path("users", AuthUserListView.as_view(), name='users'),
    path("users/<int:id>/", AuthUserEditView.as_view(), name='edit-users'),
    path("users/register", RegisterView.as_view(), name='user-register'),
    path('user/login/', LoginViewToken.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
