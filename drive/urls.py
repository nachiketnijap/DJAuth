from django.urls import path
from .views import upload_file, fetch_files

urlpatterns = [
    path("upload/", upload_file),
    path("files/", fetch_files),
]