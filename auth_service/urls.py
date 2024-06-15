from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('auth', views.AuthAPIView.as_view(), name='auth_api'),
    path('user', views.UserAPI.as_view(), name='user_api'),

]
