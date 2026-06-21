import os
import json
import asyncio
import redis.asyncio as redis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)

    async def broadcast_local(self, room: str, message: str):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                try:
                    await connection.send_text(message)
                except:
                    pass

manager = ConnectionManager()

async def redis_listener():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("review-comments")
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"].decode("utf-8"))
            room = data.get("room")
            payload = data.get("payload")
            await manager.broadcast_local(room, json.dumps(payload))

# Start the listener in the background when the app starts
# This should ideally be called in an @app.on_event("startup")
asyncio.create_task(redis_listener())

@router.websocket("/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            # Publish to redis so all workers receive it
            payload = {"room": room, "payload": json.loads(data)}
            await redis_client.publish("review-comments", json.dumps(payload))
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
