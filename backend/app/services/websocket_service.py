from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import httpx
import asyncio
import json

router = APIRouter()
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected to WebSocket")

    try:
        while True:
            try:
                data_text = await asyncio.wait_for(
                    websocket.receive_text(), 
                    timeout=60
                )
                
                try:
                    data = json.loads(data_text)
                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON received")
                    continue

                msg_type = data.get("type")
                
                if msg_type == "init":
                    await websocket.send_json({
                        "type": "init_ack",
                        "content": "Connected to chat service"
                    })
                    continue
                
                if msg_type == "pong":
                    continue
                
                if msg_type == "message":
                    user_msg = data.get("content") 
                    sender_id = data.get("sender", "default_user")
                    
                    if not user_msg:
                        continue

                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            RASA_URL,
                            json={"sender": sender_id, "message": user_msg},
                            timeout=30.0
                        )

                    rasa_replies = response.json()
                    
                    for msg in rasa_replies:
                        await websocket.send_json({
                            "type": "message", 
                            "content": msg.get("text"),
                            "data": {
                                "buttons": msg.get("buttons", []),
                                "image": msg.get("image"),
                            }
                        })

            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
                
            except WebSocketDisconnect:
                print("❌ Client disconnected")
                break
                
            except Exception as e:
                print(f"⚠️ Error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "content": "An error occurred processing your message"
                })

    finally:
        print("🔻 Connection closed")