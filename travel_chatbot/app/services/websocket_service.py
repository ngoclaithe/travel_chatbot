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
                # Nhận message với timeout 60s
                data_text = await asyncio.wait_for(
                    websocket.receive_text(), 
                    timeout=60
                )
                
                # Parse JSON
                try:
                    data = json.loads(data_text)
                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON received")
                    continue

                msg_type = data.get("type")
                
                # Xử lý init message
                if msg_type == "init":
                    await websocket.send_json({
                        "type": "init_ack",
                        "content": "Connected to chat service"
                    })
                    continue
                
                # Xử lý pong từ client
                if msg_type == "pong":
                    continue
                
                # Xử lý chat message
                if msg_type == "message":
                    user_msg = data.get("content")  # ✅ Đổi từ "message" → "content"
                    sender_id = data.get("sender", "default_user")
                    
                    if not user_msg:
                        continue

                    # Gọi Rasa
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            RASA_URL,
                            json={"sender": sender_id, "message": user_msg},
                            timeout=30.0
                        )

                    rasa_replies = response.json()
                    
                    # Gửi responses về frontend
                    for msg in rasa_replies:
                        await websocket.send_json({
                            "type": "message",  # ✅ Thêm type
                            "content": msg.get("text"),
                            "data": {
                                "buttons": msg.get("buttons", []),
                                "image": msg.get("image"),
                            }
                        })

            except asyncio.TimeoutError:
                # Gửi ping để giữ connection
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