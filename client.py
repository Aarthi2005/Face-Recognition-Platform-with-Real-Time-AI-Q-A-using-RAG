import asyncio
import websockets
import json

async def ask_question():
    async with websockets.connect("ws://localhost:8001") as websocket:
        question = input("Type your question: ")

        # Send the question as a JSON object
        data = {"question": question}
        await websocket.send(json.dumps(data))

        # Receive and print the response
        response = await websocket.recv()
        print(f"Answer: {response}")

# Run the function
asyncio.run(ask_question())
