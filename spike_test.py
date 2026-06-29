import os
import asyncio
from dotenv import load_dotenv

load_dotenv()  # reads our .env file into environment variables

import cognee

async def main():
    print("Storing a memory...")
    await cognee.remember("The user's name is Alex and they prefer concise answers.")

    print("Recalling it...")
    results = await cognee.recall("What does the user prefer?")

    print("\n--- RECALL RESULTS ---")
    for result in results:
        print(result)

asyncio.run(main())