# main.py

import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled
from inv_agent.inventory_agent import InventoryAgent  

set_tracing_disabled(True)  
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY is None:
    raise RuntimeError("Please set the GEMINI_API_KEY environment variable")


client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash"
)

async def main():
    
    agent = InventoryAgent(model=model)

    print("Ask about a product (or type 'exit'):")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Bye!")
            break

    
        result = await Runner.run(agent, input=user_input)
        print("Agent:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
