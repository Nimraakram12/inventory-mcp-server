# main.py

import os
import asyncio
from dotenv import load_dotenv
from agents import Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from inv_agent.inventory_agent import InventoryAgent

# Disable tracing if you don’t need detailed logs
set_tracing_disabled(True)

# Load environment variables from .env (for local dev)
load_dotenv()

# Get your API key from environment
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set the GEMINI_API_KEY environment variable")

# Initialize your client & model
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash"
)

async def main():
    # Create your agent, passing in the model
    agent = InventoryAgent(model=model)

    print("Ask about a product (or type 'exit'):")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Bye!")
            break

        # Run the agent with the user input
        result = await Runner.run(agent, input=user_input)
        print("Agent:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
