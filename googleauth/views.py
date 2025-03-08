import os
import json
from django.shortcuts import redirect
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow

# Allow HTTP during local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Load Google OAuth Credentials from Environment Variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URI = os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")
GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token")
GOOGLE_AUTH_PROVIDER_CERT = os.getenv("GOOGLE_AUTH_PROVIDER_CERT", "https://www.googleapis.com/oauth2/v1/certs")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly"
]

# Manually construct client config instead of using a file
client_config = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": GOOGLE_AUTH_URI,
        "token_uri": GOOGLE_TOKEN_URI,
        "auth_provider_x509_cert_url": GOOGLE_AUTH_PROVIDER_CERT
    }
}

def google_login(request):
    flow = Flow.from_client_config(client_config, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)

def google_callback(request):
    flow = Flow.from_client_config(client_config, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    credentials = flow.credentials
    request.session['google_access_token'] = credentials.token
    request.session['google_refresh_token'] = credentials.refresh_token

    return JsonResponse({"access_token": credentials.token})
