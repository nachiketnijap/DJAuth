import json
import os
from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from django.views.decorators.csrf import csrf_protect
from googleapiclient.errors import HttpError
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            access_token = data.get("access_token")
            file_content = data.get("file_content")  # File content as a string
            file_name = data.get("file_name", "example.txt")  # Default file name

            if not access_token or not file_content:
                return JsonResponse({"error": "Missing access_token or file_content"}, status=400)

            # Create credentials and Google Drive service
            credentials = Credentials(token=access_token)
            service = build("drive", "v3", credentials=credentials)

            # Prepare file metadata and media
            file_metadata = {"name": file_name}
            media = MediaIoBaseUpload(io.BytesIO(file_content.encode()), mimetype="text/plain")

            # Upload the file
            file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

            return JsonResponse({"file_id": file.get("id")})

        except HttpError as e:
            return JsonResponse({"error": f"Google Drive API error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

@csrf_exempt
def fetch_files(request):
    # Parse JSON data from the request body
    data = json.loads(request.body)
    access_token = data.get("access_token")
    credentials = Credentials(token=access_token)
    service = build("drive", "v3", credentials=credentials)
    
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    return JsonResponse(results)
