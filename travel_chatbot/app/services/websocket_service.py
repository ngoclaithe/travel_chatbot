from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import httpx

router = APIRouter()

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected to WebSocket")

    try:
        while True:
            # 1️⃣ Nhận message từ FE
            data = await websocket.receive_json()
            user_msg = data.get("message")
            sender_id = data.get("sender", "default_user")

            # 2️⃣ Gửi message tới Rasa Core REST webhook
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    RASA_URL,
                    json={"sender": sender_id, "message": user_msg},
                    timeout=30.0
                )

            rasa_replies = response.json()

            # 3️⃣ Trả lại cho FE
            for msg in rasa_replies:
                await websocket.send_json({
                    "from": "bot",
                    "text": msg.get("text"),
                    "buttons": msg.get("buttons", []),
                    "image": msg.get("image"),
                })

    except WebSocketDisconnect:
        print("❌ Client disconnected")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        await websocket.close()
