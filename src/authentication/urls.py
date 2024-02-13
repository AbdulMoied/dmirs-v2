from rest_framework import routers
from django.urls import path
from .views import ChangePasswordView, ObtainTokenPairView,get_user_permissions,UserList,ResetPassword,RequestPasswordResetEmail,SetNewPasswordAPIView
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("login/", ObtainTokenPairView.as_view(), name="login"),
    path("refresh-token/", jwt_views.TokenRefreshView.as_view(), name="refresh_token"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("get_user_permissions/",get_user_permissions,name="get_user_permissions"),
    path("get_all_users/",UserList.as_view(),name="get_all_users/"),
    path('reset-user-password/<int:pk>/',ResetPassword.as_view(),name='reset-user-password'),
    path('reset_password/', RequestPasswordResetEmail.as_view(),name="reset_password"),
    path('password_reset_confirm/', SetNewPasswordAPIView.as_view(),name='password-reset-confirm'),
]
