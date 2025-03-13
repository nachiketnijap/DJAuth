# Google OAuth 2.0, Google Drive API, and WebSocket Real-Time Chat Integration

## Demo Video
For a quick overview and testing of endpoints, refer to the demo video:
[Google Drive API and WebSocket Integration](https://drive.google.com/file/d/1FYgO1DzRr0RNEMVZ74VRaDDIN0e8QAAW/view?usp=drive_link)

## Overview
This document provides a guide on integrating Google OAuth 2.0 API for authentication, Google Picker API for file uploads and reading data, and WebSockets for real-time communication. Follow the step-by-step instructions to test these functionalities using Postman and web browser.

---
## 1. Google OAuth 2.0 API for User Authentication

### Endpoint:
- **Login URL:** [https://djauth-qa3y.onrender.com/googleauth/login/](https://djauth-qa3y.onrender.com/googleauth/login/)

### Steps:
1. Open the login URL in a web browser.
2. Authenticate using your Google credentials.
3. Upon successful authentication, an **access token** will be generated.
4. Save this access token, as it is required for subsequent API requests.

---
## 2. Google Picker API for File Uploads and Reading Data

### Endpoints:
- **Google Picker Interface:** [https://djauth-qa3y.onrender.com/drive/picker/](https://djauth-qa3y.onrender.com/drive/picker/)
- **File Upload:** [https://djauth-qa3y.onrender.com/drive/upload/](https://djauth-qa3y.onrender.com/drive/upload/)

### Steps:
#### a. Using Google Picker to Read or Download Files
1. Ensure you are authenticated and have a valid **access token**.
2. Open the Google Picker URL in a web browser.
3. Click on **"Open Google Picker"**.
4. Select a file from Google Drive.
5. You will see options to either:
   - **Read the file** (Supported formats: **.txt**, **.json**)
   - **Download the file**

#### b. Uploading a File to Google Drive
1. Open Postman.
2. Use the **POST** method to send a request to the **upload URL**.
3. In the request body, provide:
   - **Access Token** (obtained from OAuth login)
   - **File** to be uploaded
4. In response, you will receive a **file_id** for further operations.

---
## 3. WebSocket for Real-Time Communication

### WebSocket Endpoint:
- **WebSocket URL:** `wss://djauth-qa3y.onrender.com/ws/chat/user1-user2/`

### Steps:
1. Authenticate both users separately to obtain their respective **access tokens**.
2. Open Postman and create a WebSocket connection using the above URL.
3. In **Headers**, add:
   - **Authorization:** `Bearer <access_token>` (Replace `<access_token>` with the actual token obtained from OAuth authentication)
4. Repeat steps 1-3 for the second user using a different **access token**.
5. Once both users are connected, they can send and receive messages in real-time.

---
## Resources
- **Postman Collection for Google Drive Upload:** [Upload-Drive Postman Collection](https://upload-drive.postman.co/workspace/Upload-Drive-Workspace~a25d9b87-c762-44dd-a99b-3b7a2ac6dfb3/collection/42227661-128b5b8d-7b32-41f9-bbe5-88fb55e9bef1?action=share&creator=42227661)
- **Postman Collection for WebSocket Chat:** [WebSocket Chat Postman Collection](https://upload-drive.postman.co/workspace/New-Team-Workspace~02a8a198-dee8-4a5c-acf1-0b968a5e61b5/collection/67cc0ffd06fcf15211eccab8?action=share&creator=42227661)

---
This guide provides a structured way to authenticate, manage Google Drive files, and enable real-time messaging using WebSockets. Follow the steps carefully to test and integrate these functionalities successfully.

