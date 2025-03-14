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
from googleapiclient.http import MediaIoBaseDownload
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import FileResponse
@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        try:
            # Get access_token from form data
            access_token = request.POST.get("access_token")
            
            # Check if a file is included in the request
            if "file" not in request.FILES:
                return JsonResponse({"error": "No file uploaded"}, status=400)
            if not access_token:
                return JsonResponse({"error": "Missing access_token"}, status=400)

            # Get the uploaded file
            uploaded_file = request.FILES["file"]
            file_name = uploaded_file.name  # Use the original file name

            # Create credentials and Google Drive service
            credentials = Credentials(token=access_token)
            service = build("drive", "v3", credentials=credentials)

            # Prepare file metadata and media
            file_metadata = {"name": file_name}
            media = MediaIoBaseUpload(uploaded_file, mimetype=uploaded_file.content_type)

            # Upload the file to Google Drive
            file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

            return JsonResponse({"file_id": file.get("id")})

        except HttpError as e:
            return JsonResponse({"error": f"Google Drive API error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)



@csrf_exempt
def download_file(request):
    try:
        file_id = request.GET.get("file_id")
        access_token = request.GET.get("access_token")

        if not access_token or not file_id:
            return JsonResponse({"error": "Missing access_token or file_id"}, status=400)

        credentials = Credentials(token=access_token)
        service = build("drive", "v3", credentials=credentials)

        # Get file metadata to retrieve the original file name
        file_metadata = service.files().get(fileId=file_id, fields="name").execute()
        original_file_name = file_metadata.get("name", f"downloaded_{file_id}")

        # Prepare the file for download
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        # Download the file in chunks
        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Rewind the file stream to the beginning
        file_stream.seek(0)

        # Create the response with the file content
        response = FileResponse(file_stream, as_attachment=True, filename=original_file_name)
        response['Content-Disposition'] = f'attachment; filename="{original_file_name}"'
        response['Content-Type'] = 'application/octet-stream'

        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def read_file(request):
    """Reads file content without downloading"""
    try:
        data = json.loads(request.body)
        access_token = data.get("access_token")
        file_id = data.get("file_id")

        if not access_token or not file_id:
            return JsonResponse({"error": "Missing access_token or file_id"}, status=400)

        credentials = Credentials(token=access_token)
        service = build("drive", "v3", credentials=credentials)

        # Fetch file metadata
        file_metadata = service.files().get(fileId=file_id, fields="name, mimeType").execute()
        file_name = file_metadata.get("name", "unknown_file")
        mime_type = file_metadata.get("mimeType", "")

        # Read file content
        request_media = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        file_stream.write(request_media.execute())
        file_stream.seek(0)

        if "text" in mime_type or file_name.endswith(".txt"):  
            file_content = file_stream.getvalue().decode("utf-8")  
        elif "application/json" in mime_type or file_name.endswith(".json"):  
            file_content = json.loads(file_stream.getvalue().decode("utf-8"))  
        else:
            file_content = "Preview not supported for this file type."

        return JsonResponse({
            "file_name": file_name,
            "mime_type": mime_type,
            "content": file_content
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt 
def google_picker(request):
    return render(request, "picker.html")
    
@api_view(['GET'])
def get_access_token(request):
    """API to fetch Google OAuth access token from session"""
    access_token = request.session.get('google_access_token')
    
    if not access_token:
        return JsonResponse({'error': 'Access token not found'}, status=401)

    return JsonResponse({'access_token': access_token})