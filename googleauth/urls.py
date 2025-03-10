from django.urls import path
from .views import google_login, google_callback, display_home_page, display_privacy_policy

urlpatterns = [
    path("login/", google_login),
    path("callback/", google_callback),
    path("home-page/", display_home_page, name="home-page"),
    path("privacy-policy/", display_privacy_policy, name="privacy-policy"),
]