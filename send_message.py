# send_acetylcholine.py
import asyncio
import websockets

async def send_injection():
    uri = "ws://localhost:8765/lapinvitals"
    async with websockets.connect(uri) as websocket:
        await websocket.send("acétylcholine")
        print("Message 'acétylcholine' envoyé.")

asyncio.run(send_injection())