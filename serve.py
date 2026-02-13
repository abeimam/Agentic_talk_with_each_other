import asyncio
import websockets
import json

connection_dictionary = {}

# ws is the live websocket connection object like: <WebSocketServerProtocol ws://localhost:8765/ state=OPEN>
#       it's structure is as: Protocol - URL - State
async def heandler(ws):
    try:
        intro = await ws.recv()   # wesbocket method to recieve mssg from client.
        data = json.loads(intro)
        print(f"data is :: {data}")
        name = data["name"]

        if data.get("type") == "register":
            connection_dictionary[name] = ws   # storing the agents in the connected 
        
        print(f"connection_dictionary is : {connection_dictionary}")
        print(f"Agent name {name} connected")

        while True:
            async for msg in ws:
                data= json.loads(msg)
                print(f"data is from inside :: {data}")
                target = data["target"]
                text = data["text"]

                print(f"from {name} -> {target}: {text}")

                if target in connection_dictionary:
                    print(f"inside the if target in connection_dictionary BLOCK..")
                    await connection_dictionary[target].send(json.dumps({
                        "from": name, 
                        "text": text
                    }))
                else:
                    print(f"Target not connected ..")

    except websockets.ConnectionClosed:
        print(f"❌ Agent {name} disconnected")

    finally:
        if name in connection_dictionary:
            del connection_dictionary[name]

async def main():
    # async with websockets.serve(heandler, "localhost", 8765, ping_timeout=None):   # this is not the normal running of the funciton but the coroutine, ????
    async with websockets.serve(heandler, "localhost", 8765, ping_timeout=None):
        print("🚀 Server running at ws://localhost:8765")
        await asyncio.Future()  # keep running forever

if __name__ == "__main__":
    asyncio.run(main())


print("DONE..")