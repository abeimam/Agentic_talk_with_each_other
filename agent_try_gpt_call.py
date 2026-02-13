# import asyncio
# import websockets
# import json
# import sys
# import random

# async def agent(name):
#     uri = "ws://localhost:8765"
#     name = sys.argv[-1]
#     target = None
#     async with websockets.connect(uri) as ws:   # to setup a connection with server 
#         await ws.send(json.dumps({"type": "register", "name": name}))

#         while True:
            
#             msg = await ws.recv()
#             msg = json.loads(msg)

#             print(f"mssg got to {name} = {msg}")

#             print(f"{name} got: {msg}")

#             # just a simple check if message is present or not 
#             if "text" in msg:
#                 reply = {"from": name, "text": f"{name} replying to: {msg['text']}"}
#                 await ws.send(json.dumps(reply))

# if __name__ == "__main__":
#     asyncio.run(agent("A"))  
import asyncio
import websockets
import json
import sys
from openai import OpenAI
import os 
from prompt import making_prompt
from dotenv import load_dotenv

load_dotenv()

# common_mssg = ""
common_mssg = ""

api_key = os.getenv('OPENAI_API_KEY')
print(f"api key -- {api_key}")
client = OpenAI(api_key=api_key)

async def generate_gpt_response(prompt):
    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
        


# async def send_messages(ws, name, target):
#     while True:
#         # For demo, sending random messages every few seconds
#         # await asyncio.sleep(3)
#         # text = f"Hello from {name}"
#         # text = input(f"enter text for {name} - ")
#         prompt = making_prompt(previous_message=common_mssg)
#         print("getting the prompt & passing to GPT ")
#         text = await generate_gpt_response(prompt=prompt)
#         print(f"Response from GPT")
#         if target:
#             await ws.send(json.dumps({"from": name, "target": target, "text": text}))
#             print(f"{name} sent: {text}")

async def send_messages(ws, name, target):
    global common_mssg
    while True:
        await asyncio.sleep(2)   # prevent spamming
        prompt = making_prompt(previous_message=common_mssg)
        print("getting the prompt & passing to GPT ")
        text = await generate_gpt_response(prompt=prompt)
        print(f"Response from GPT: {text}")
        if target:
            await ws.send(json.dumps({"from": name, "target": target, "text": text}))
            print(f"{name} sent: {text}")

# async def receive_messages(ws, name):
#     global common_mssg
#     while True:
#         msg = await ws.recv()
#         msg = json.loads(msg)
#         print(f"{name} got: {msg}")
#         common_mssg = msg

async def receive_messages(ws, name):
    global common_mssg
    while True:
        msg = await ws.recv()
        msg = json.loads(msg)
        print(f"{name} got: {msg}")
        # store only the text for prompt
        if "text" in msg:
            common_mssg = msg["text"]


async def agent(name, target=None):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        # register
        await ws.send(json.dumps({"type": "register", "name": name}))

        # run send and receive concurrently
        await asyncio.gather(
            send_messages(ws, name, target),
            receive_messages(ws, name)
        )

if __name__ == "__main__":
    # Example: python agent.py A B
    agent_name = sys.argv[1]
    target_name = sys.argv[2] if len(sys.argv) > 2 else None
    asyncio.run(agent(agent_name, target_name))
