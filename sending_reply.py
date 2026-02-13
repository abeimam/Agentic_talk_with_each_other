import asyncio
import websockets
import json
import sys


async def agent(name):
    uri = "ws://localhost:8765"
    name = sys.argv[-1]
    target = None
    async with websockets.connect(uri) as ws:   # to setup a connection with server 

        await ws.send(json.dumps({"type": "register", "name": name}))

        while True:
            
            msg = await ws.recv()
            msg = json.loads(msg)

            print(f"mssg got to {name} = {msg}")

            print(f"{name} got: {msg}")

            # just a simple check if message is present or not 
            if "text" in msg:
                reply = {"from": name, "text": f"{name} replying to: {msg['text']}"}
                await ws.send(json.dumps(reply))

if __name__ == "__main__":
    asyncio.run(agent("A"))  