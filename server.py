# Python code modifié (serveur) – Assurez-vous d'installer pyserial (pip install pyserial)
import asyncio
import json
import time
import websockets
import serial
from GestionCyclesLapin import GestionCyclesLapin

# Ouverture du port série vers l'Arduino (modifiez le port en fonction de votre configuration)


sessions = set()
gestionCycles = GestionCyclesLapin()
simulation_time = time.time() * 1000

async def broadcast(message: str) -> None:
    for ws in sessions.copy():
        if ws:
            await ws.send(message)

async def producer() -> None:
    global simulation_time
    period = 0.1  # 100ms
    next_call = time.monotonic()
    while True:
        next_call += period
        samples = 25  # 25 points par batch
        time_serie = [simulation_time + i * 4 for i in range(samples)]
        vitals = gestionCycles.get_vitals(time_serie)
        simulation_time += 100
        message = json.dumps(vitals)
        await broadcast(message)
        await asyncio.sleep(max(0, next_call - time.monotonic()))

async def handler(websocket) -> None:
    sessions.add(websocket)
    try:
        async for message in websocket:
            if message.strip().lower() == "acétylcholine":
                gestionCycles.inject_acetylcholine()
    except Exception as e:
        print("Error:", e)
    finally:
        sessions.remove(websocket)

async def main() -> None:
    asyncio.create_task(producer())
    async with websockets.serve(handler, "localhost", 8765, process_request=lambda path, request_headers: None):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
