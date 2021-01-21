# External Import
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# Internal Import
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('verify-email/', views.VerifyEmail.as_view(), name='user-verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='user-refresh-token'),


]
