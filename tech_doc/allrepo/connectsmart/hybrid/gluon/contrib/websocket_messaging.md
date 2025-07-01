# Gluon Contrib WebSocket Messaging Module

## Overview
WebSocket messaging implementation for web2py applications. Provides real-time bidirectional communication between web browsers and the server using WebSocket protocol.

## Module Information
- **Module**: `gluon.contrib.websocket_messaging`
- **Purpose**: Real-time WebSocket communication
- **Use Case**: Live chat, notifications, real-time updates

## Key Features
- **Real-time Communication**: Bidirectional WebSocket messaging
- **Broadcasting**: Send messages to multiple clients
- **Room Management**: Group clients into chat rooms or channels
- **Authentication**: Secure WebSocket connections
- **Event Handling**: Custom event handling system

## Basic Usage

### WebSocket Server Setup
```python
from gluon.contrib.websocket_messaging import WebSocketServer

# Create WebSocket server
ws_server = WebSocketServer()

@ws_server.on('connect')
def on_connect(client):
    """Handle client connection"""
    print(f"Client {client.id} connected")
    client.send({'type': 'welcome', 'message': 'Welcome to the chat!'})

@ws_server.on('message')
def on_message(client, data):
    """Handle incoming messages"""
    if data['type'] == 'chat_message':
        # Broadcast message to all clients
        ws_server.broadcast({
            'type': 'chat_message',
            'user': data['user'],
            'message': data['message'],
            'timestamp': datetime.datetime.now().isoformat()
        })

@ws_server.on('disconnect')
def on_disconnect(client):
    """Handle client disconnection"""
    print(f"Client {client.id} disconnected")

# Start WebSocket server
def websocket():
    """WebSocket endpoint"""
    return ws_server.handle_request(request)
```

### Client-Side JavaScript
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/myapp/default/websocket');

ws.onopen = function(event) {
    console.log('Connected to WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'chat_message') {
        displayChatMessage(data);
    } else if (data.type === 'notification') {
        showNotification(data.message);
    }
};

ws.onclose = function(event) {
    console.log('WebSocket connection closed');
};

// Send message
function sendMessage(message) {
    ws.send(JSON.stringify({
        type: 'chat_message',
        user: currentUser,
        message: message
    }));
}
```

### Real-time Notifications
```python
class NotificationService:
    def __init__(self, ws_server):
        self.ws_server = ws_server
        self.user_connections = {}  # Map user_id to client connections
    
    def register_user(self, client, user_id):
        """Register user connection"""
        self.user_connections[user_id] = client
        client.user_id = user_id
    
    def send_notification(self, user_id, notification):
        """Send notification to specific user"""
        if user_id in self.user_connections:
            client = self.user_connections[user_id]
            client.send({
                'type': 'notification',
                'title': notification['title'],
                'message': notification['message'],
                'timestamp': datetime.datetime.now().isoformat()
            })
    
    def broadcast_announcement(self, announcement):
        """Broadcast announcement to all connected users"""
        self.ws_server.broadcast({
            'type': 'announcement',
            'message': announcement,
            'timestamp': datetime.datetime.now().isoformat()
        })

# Usage
notification_service = NotificationService(ws_server)

def send_user_notification(user_id, title, message):
    """Send notification to user"""
    notification_service.send_notification(user_id, {
        'title': title,
        'message': message
    })
    
    # Also store in database
    db.notifications.insert(
        user_id=user_id,
        title=title,
        message=message,
        created_at=datetime.datetime.now(),
        read=False
    )
    db.commit()
```

This module provides comprehensive WebSocket messaging capabilities for web2py applications, enabling real-time communication and live updates.