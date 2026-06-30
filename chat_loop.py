import os
import asyncio
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables

import cognee
import google.generativeai as genai

# Configure Gemini for our OWN chat calls (separate from Cognee's internal use of Gemini)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


async def chat_turn(user_message: str) -> str:
    """One full turn of the memory loop: recall -> inject -> call -> remember."""

    # 1. RECALL: pull relevant memory for this message
    print("[recalling relevant memory...]")
    memory_results = await cognee.recall(user_message)

    memory_context = ""
    if memory_results:
        memory_context = "\n".join(str(r.raw.get("value", r.text)) for r in memory_results)

    # 2. INJECT: build a prompt that includes what we remember
    if memory_context:
        prompt = (
            f"Here is what you remember about the user from past conversations:\n"
            f"{memory_context}\n\n"
            f"Now respond to the user's new message:\n{user_message}"
        )
    else:
        prompt = user_message

    # 3. CALL: ask Gemini for a response
    print("[calling Gemini...]")
    response = model.generate_content(prompt)
    reply = response.text

    # 4. REMEMBER: store this new exchange for future turns
    print("[storing this exchange in memory...]")
    await cognee.remember(f"User said: {user_message}. Assistant replied: {reply}")

    return reply


async def main():
    print("Memory-aware chat. Type 'exit' to quit.\n")
    while True:
        user_message = input("You: ")
        if user_message.strip().lower() == "exit":
            break

        if user_message.strip().lower().startswith("/remember"):
            fact = user_message[len("/remember"):].strip()
            if fact:
                print("[manually storing this fact...]")
                await cognee.remember(fact)
                print(f"\nRemembered: {fact}\n")
            else:
                print("\nUsage: /remember <something to store>\n")
            continue

        if user_message.strip().lower() == "/forget":
            print("[wiping all memory...]")
            await cognee.forget(dataset="main_dataset")
            print("\nAll memory has been cleared.\n")
            continue

        reply = await chat_turn(user_message)
        print(f"\nAssistant: {reply}\n")

if __name__ == "__main__":
    asyncio.run(main())