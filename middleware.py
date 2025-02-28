# Nouveau programme Python – Assurez-vous d'installer pyserial et websockets (pip install pyserial websockets)
import asyncio
import json
import serial
import websockets
import time

arduino_serial = serial.Serial(port='COM9', baudrate=2000000, timeout=0.1)
time.sleep(2)

async def process_batch(batch):
    # Chaque point a la structure [timestamp, respiration, pa, diurese]
    if not batch:
        return
    # On prend le dernier point du batch
    _, _, pa, diurese = batch[-1]
    # Calcul des booléens :
    # Pour la diurèse : True si diurese != 0, sinon False.
    # Pour la PA : True si pa > 110, sinon False.
    diuresis_bool = diurese != 0
    for b in batch:
        if b[3] != 0:
            diuresis_bool = True
    
    pa_bool = pa > 105
    # Envoi sous le format "bool_diurese/bool_pa\n" où True est représenté par 1 et False par 0.
    msg = 0
    if diuresis_bool:
        msg = msg + 2
    if pa_bool:
        msg = msg + 1
    
    arduino_serial.write(bytes(str(msg)+"\n",'utf-8'))
    print(str(msg))
    

async def listen():
    uri = "ws://localhost:8765/lapinvitals"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            try:
                batch = json.loads(message)  # Batch de points reçu
                await process_batch(batch)
            except json.JSONDecodeError:
                print("Erreur de décodage JSON :", message)

async def main():
    await listen()

if __name__ == "__main__":
    asyncio.run(main())
