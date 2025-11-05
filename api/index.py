from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class InventoryRequest(BaseModel):
    product_name: str

class InventoryResponse(BaseModel):
    product: str
    available: bool
    quantity: Optional[int] = None

@app.post("/mcp")
async def handle_mcp(req: InventoryRequest):
    # your logic to check inventory
    # For demo:
    return InventoryResponse(product=req.product_name, available=True, quantity=10)
