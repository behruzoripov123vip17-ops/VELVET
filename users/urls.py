from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("auth/google/", views.google_login, name="google_login"),
    path("auth/google/callback/", views.google_callback, name="google_callback"),
    path("account/", views.account, name="account"),
    path("account/avatar/", views.upload_avatar, name="upload_avatar"),
    path("account/status/", views.account_status, name="account_status"),
    path("logout/", views.logout_view, name="logout"),
]
