import json
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.token = await self.get_token_from_headers()

        # Verify token with Google API
        user_info = await self.verify_google_token(self.token)

        if not user_info:
            await self.send(text_data=json.dumps({
                "error": "Invalid or expired token. Authentication failed."
            }))
            await self.close()
            return  # Close connection if token is invalid

        # Extract room name only after authentication
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join the WebSocket group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.send(text_data=json.dumps({
            "message": f"Connected to room {self.room_name}",
            "user": user_info
        }))

    async def get_token_from_headers(self):
        """Extract token from WebSocket headers"""
        headers = dict(self.scope["headers"])
        auth_header = headers.get(b"authorization", None)
        if auth_header:
            return auth_header.decode().split("Bearer ")[-1]  # Extract token
        return None

    async def verify_google_token(self, token):
        """Verify Google OAuth token and fetch user info"""
        if not token:
            return None

        google_verify_url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(google_verify_url) as response:
                if response.status == 200:
                    user_data = await response.json()
                    return {"email": user_data.get("email"), "user_id": user_data.get("user_id")}

        return None  # Return None if token is invalid

    async def disconnect(self, close_code):
        """Leave the WebSocket group on disconnect"""
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        data = json.loads(text_data)
        message = data["message"]

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({"message": event["message"]}))
