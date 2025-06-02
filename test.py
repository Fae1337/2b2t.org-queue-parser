import asyncio
import websockets
import json
from colorama import Fore

actual_queue = 0
async def get_queue_from_websocket():
    global actual_queue
    url = "wss://2b2t.io/ws"
    try:
        async with websockets.connect(url) as websocket:
            message = await websocket.recv()
            #if message == '1':
                #await websocket.send('2')

            data = json.loads(message)
            queue_length = int(data[1])

            if queue_length != actual_queue:
                actual_queue = queue_length
                print(Fore.GREEN + f"   2b2t queue is {queue_length} players long")

            elif queue_length == actual_queue:
                pass

            return queue_length

    except websockets.exceptions.ConnectionClosedError as cc:
        print(Fore.Red + f"WebSocket locked: {cc}")
        return None
    except Exception as e:
        print(Fore.Red + f"Error to connect WebSocket: {e}")
        return None

async def main():
    await get_queue_from_websocket()

if __name__ == "__main__":
    print("2b2t queue parser by:\n"
          "https://github.com/Fae1337/2b2t.org-queue-parser\n")

    while True:
        asyncio.run(main())