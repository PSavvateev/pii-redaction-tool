from google.adk import Agent
from schemas import RedactionRequest
from utils.redaction import redact_text

_REDACTOR_PROMPT = """
You are a deterministic redaction agent.
• Always call `redact_text` with the JSON you receive.
• If the `strategy` field is missing or null, use "mask".
• Return ONLY the tool‑call result as JSON (no prose).
"""

# ---------------------------------------------------------------------------
# 🤖 Agent definition
# ---------------------------------------------------------------------------

pii_redactor_agent = Agent(
    name="pii_redactor_agent",
    description="Redacts text according to detected PII entities",
    model="gemini-1.5-flash", 
    instruction=_REDACTOR_PROMPT,
    tools=[redact_text],
    input_schema=RedactionRequest
)



