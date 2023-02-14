from django.urls import path

from .views import GetTokenView, SignUpView

app_name = "api"

urlpatterns = [
    path("v1/auth/signup/", SignUpView.as_view(), name="sign_up"),
    path("v1/auth/token/", GetTokenView.as_view(), name="get_token"),
]
