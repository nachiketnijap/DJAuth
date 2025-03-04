import os
import json
from django.shortcuts import redirect
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow

# Allow HTTP during local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Google OAuth 2.0 Configuration
CLIENT_SECRETS_FILE = "client_secret.json"  # Download from Google Console
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",  # For email access
    "openid",  # For basic profile information
    "https://www.googleapis.com/auth/drive.file",  # For Google Drive file access
]
REDIRECT_URI = "http://127.0.0.1:8000/googleauth/callback/"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
)

def google_login(request):
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)

def google_callback(request):
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    return JsonResponse({"access_token": credentials.token})
