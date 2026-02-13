import asyncio
import websockets
import json
import sys
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os 
from prompt import making_prompt

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def send_messages(ws, name, target, first_to_speak, bypassing=False, initial_mssg = ""):
    # global common_mssg
    if first_to_speak != name and bypassing is False:
        pass

    else:
        print(f"waiting from inside send_messages function ..")
        await asyncio.sleep(3)

        print(f"with message to pass to LLM = {initial_mssg}")
        prompt = making_prompt(previous_message=initial_mssg)
        chat_completions = await client.chat.completions.create(
            messages=[
                {
                    "role": "user", 
                    "content": prompt,
                }
            ],
            model="gpt-4.1-nano"
        )
        
        text = chat_completions.choices[0].message.content
        if target:
            await ws.send(json.dumps({"from": name, "target": target, "text": text}))
            print(f"{name} sent: {text}")

async def receive_messages(ws, name, target, first_to_speak):
    while True:
        msg = await ws.recv()
        print("ttyu - ")
        msg = json.loads(msg)
        print(f"{name} got: {msg}")

        await send_messages(ws, name, target, first_to_speak, bypassing=True, initial_mssg=msg['text'])


# sending heartbeact so that connection never closes 
async def keep_connection_alive(ws):
    while True:
        try: 
            print(f"sednig ping ")
            await ws.ping()
            await asyncio.sleep(10)
        except Exception as e:
            break 


async def agent(name, first_to_speak, target=None):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        # register
        await ws.send(json.dumps({"type": "register", "name": name}))

        # run send and receive concurrently
        await asyncio.gather(
            send_messages(ws, name, target, first_to_speak, ),
            receive_messages(ws, name, target, first_to_speak),
            keep_connection_alive(ws)
        )

if __name__ == "__main__":
    # Example: python agent.py A B
    agent_name = sys.argv[1]
    target_name = sys.argv[2] if len(sys.argv) > 2 else None
    first_to_speak = sys.argv[3] if len(sys.argv) > 3 else None


    asyncio.run(agent(name=agent_name, first_to_speak=first_to_speak, target=target_name))
