import asyncio
import websockets
import json
import requests
import time
from colorama import Fore

actual_queue = []
async def get_queue_from_websocket():
    global actual_queue
    uri = "wss://2b2t.io/ws"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                if message == '1':
                    await websocket.send('2')
                    continue

                data = json.loads(message)
                queue_length = int(data[1])

                if queue_length not in actual_queue:
                    actual_queue.append(queue_length)
                    print(Fore.GREEN + f"   2b2t queue is {queue_length} players long")

                elif queue_length == actual_queue:
                    pass

                return queue_length

    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket соединение закрыто.")
        return None
    except Exception as e:
        print(f"Ошибка при подключении WebSocket: {e}")
        return None

async def get_queue_from_api():
    global actual_queue

    url = "https://2b2t.org/api/queue?last=true"
    response = requests.get(url)
    response.raise_for_status()  # Проверка на ошибки HTTP
    data = response.json()

    if data:
        queue_length = int(data[0][1])

        if queue_length not in actual_queue:
            actual_queue.append(queue_length)
            print(Fore.GREEN + f"   2b2t queue is {queue_length} players long")

        elif queue_length == actual_queue:
            pass

        return queue_length
    else:
        print("Не удалось получить данные о очереди из API")
        return None

async def main():
    queue_length = await get_queue_from_websocket()
    if queue_length is None:
       queue_length = await get_queue_from_api()
    if queue_length is None:
        print("Не удалось получить данные о очереди")

if __name__ == "__main__":
    print(
        "                                 ..                \n"
        "                                .@@@.              \n"
        "                                *@@@-              \n"
        "                               =@@@@@=.             \n"
        "                              +@@@@@@@@-            \n"
        "                             #@@@@@@@@@@#.          \n"
        "      :@@@#                .@@@@@@@@@@@@@@@=.       \n"
        "      :@@@@@%..............+@@@@@@@@@@@@@@@@@-      \n"
        "        =@@@@@@@@@@@@@@@@@@*:.-%@@@@@@@@@@@@@=      \n"
        "          :@@@@@@@@@@@@@@@@@@@#:.:%%..:=+=:.       \n"
        "           *@@@@@@@@@@@@@@@@@@@@@@:.               \n"
        "           +@@@@@@@@@@@@@@@@@@@@@@%                \n"
        "           +@@@@@@@@@@@@@@@@@@@@@@*                \n"
        "           +@@@@@@@@@@@@@@@@@@@@@@*                \n"
        "          .@@@@@@@@*+=======++#@@@*                \n"
        "          #@@@+%@@@+          .@@@#                \n"
        "         #@@@+..%@@@*         .@@@#                \n"
        "        %@@@#.  .@@@@#        .@@@%.               \n"
        "       :@@@%     .%@@@:       .@@@@.               \n"
        "        :-:        :-.         .--.                \n"
        "\n"
        ": ================= 2b2t actual queue ================= :\n")

    while True:
        asyncio.run(main())