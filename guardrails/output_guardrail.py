

# guardrails/output_guardrail.py

from agents import output_guardrail
from agents.guardrail import GuardrailFunctionOutput
from agents.run_context import RunContextWrapper
from agents.agent import Agent
from pydantic import BaseModel
from typing import Optional, Any, Dict

class ProductInfoSchema(BaseModel):
    product: str
    available: bool
    quantity: Optional[int] = None

@output_guardrail
async def product_info_output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent[Any],
    output: Any
) -> GuardrailFunctionOutput:
    """
    Validates that the agent output includes at least the keys:
      - product (string)
      - available (bool)
      - quantity (int or None) (optional if available = False)
    Ignores any extra fields beyond these.
    """
    # Check the output is a dict (or mapping) so we can parse required keys
    if not isinstance(output, Dict):
        return GuardrailFunctionOutput(
            output_info={
                "reason": "Output is not a dict",
                "raw_output": output
            },
            tripwire_triggered=True
        )

    # Try to extract only the relevant subset
    # We ignore extra keys by allowing extra fields in schema with `extra = "ignore"`.
    try:
        parsed = ProductInfoSchema(**{
            "product": output.get("product"),
            "available": output.get("available"),
            "quantity": output.get("quantity")
        })
    except Exception as e:
        return GuardrailFunctionOutput(
            output_info={
                "reason": "Schema validation failed",
                "error": str(e),
                "raw_output": output
            },
            tripwire_triggered=True
        )

    # Additional logic: if available is True → quantity must be non‐null and >= 0
    if parsed.available:
        if parsed.quantity is None or parsed.quantity < 0:
            return GuardrailFunctionOutput(
                output_info={
                    "reason": "Invalid quantity when available=True",
                    "parsed": parsed.dict()
                },
                tripwire_triggered=True
            )

    # If available is False, quantity may be None or >= 0
    if not parsed.available:
        if parsed.quantity is not None and parsed.quantity < 0:
            return GuardrailFunctionOutput(
                output_info={
                    "reason": "Quantity negative when available=False",
                    "parsed": parsed.dict()
                },
                tripwire_triggered=True
            )

    # Passed checks — ignore extra fields
    return GuardrailFunctionOutput(
        output_info={"parsed": parsed.dict()},
        tripwire_triggered=False
    )
