
# guardrails/input_guardrail.py

from agents import input_guardrail
from agents.guardrail import GuardrailFunctionOutput
from agents.run_context import RunContextWrapper
from agents.agent import Agent
from agents.items import TResponseInputItem

@input_guardrail
async def product_name_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    user_input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # normalize to string
    if isinstance(user_input, list):
        raw = str(user_input[-1])
    else:
        raw = str(user_input)

    cleaned = raw.strip()
    # simple rule: only letters, numbers or spaces
    if not cleaned.replace(" ", "").isalnum():
        return GuardrailFunctionOutput(
            output_info={"reason": "Invalid characters in input", "input": raw},
            tripwire_triggered=True
        )

    # pass through
    return GuardrailFunctionOutput(
        output_info={"cleaned": cleaned},
        tripwire_triggered=False
    )
