from django.urls import path
from .views import register_view, verify_email_view, login_view, main_page_view

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("verify/<uidb64>/<token>/", verify_email_view, name="verify_email"),
    path("login/", login_view, name="login"),
    path("main/", main_page_view, name="main_page"),
]
