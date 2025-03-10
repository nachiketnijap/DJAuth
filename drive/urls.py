from django.urls import path
from .views import upload_file, download_file, google_picker, get_access_token, read_file

urlpatterns = [
    path("upload/", upload_file, name="upload"),
    path("download/",download_file, name="download"),
    path("picker/read-file/",read_file, name="read-file"),
    path("picker/", google_picker, name="google_picker"),
    path('picker/get-access-token/', get_access_token, name='get-access-token'),
    
]