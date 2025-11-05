# tools/mcp_client.py
import aiohttp
from typing import Dict, Any

MCP_ENDPOINT = "https://your-mcp-server.domain/mcp"  # URL of your MCP server

async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "jsonrpc": "2.0",
        "method": tool_name,
        "params": arguments,
        "id": 1
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(MCP_ENDPOINT, json=payload) as resp:
            result = await resp.json()
            if "error" in result:
                raise RuntimeError(f"MCP tool error: {result['error']}")
            return result["result"]

# tools/inventory_tool.py
from pydantic import BaseModel
from typing import Optional
from tools.mcp_client import call_mcp_tool

class InventoryItem(BaseModel):
    product: str
    available: bool
    quantity: Optional[int]

async def check_inventory_via_mcp(product_name: str) -> InventoryItem:
    resp = await call_mcp_tool("inventory_check", {"product_name": product_name})
    return InventoryItem(**resp)
