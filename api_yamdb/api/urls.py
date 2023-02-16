from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetAuthTokenView, SignUpView, UserViewSet

app_name = "api"

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet)

urlpatterns = [
    path("v1/auth/signup/", SignUpView.as_view(), name="sign_up"),
    path("v1/auth/token/", GetAuthTokenView.as_view(), name="get_token"),
    path("v1/", include(v1_router.urls))
]
