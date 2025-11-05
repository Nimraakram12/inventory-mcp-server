# agents/inventory_agent.py
from agents import Agent, function_tool
from tools.inventory_tool import check_inventory_via_mcp
from guardrails.input_guardrail import product_name_input_guardrail
from guardrails.output_guardrail import product_info_output_guardrail
from pydantic import BaseModel
from typing import Optional

class InventoryOutput(BaseModel):
    product: str
    available: bool
    quantity: Optional[int]

@function_tool
async def tool_check_inventory(product_name: str) -> InventoryOutput:
    item = await check_inventory_via_mcp(product_name)
    return InventoryOutput(
        product=item.product,
        available=item.available,
        quantity=item.quantity
    )

class InventoryAgent(Agent[InventoryOutput]):
    def __init__(self, model):
        super().__init__(
            name="InventoryAgent",
            instructions=(
                "You are an inventory-checking assistant. "
                "When asked about a product, you must **call the tool** `tool_check_inventory` via the MCP server. "
                "Then respond only in JSON format with keys: product (string), available (boolean), quantity (integer or null)."
            ),
            tools=[tool_check_inventory],
            input_guardrails=[product_name_input_guardrail],
            #output_guardrails=[product_info_output_guardrail],
            output_type=InventoryOutput,
            model=model
        )
