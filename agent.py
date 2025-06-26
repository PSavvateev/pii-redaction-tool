# =============================================================================
# io_agent.py – **CRM‑agnostic I/O Router**
# -----------------------------------------------------------------------------
# Purpose:
#   * Decouple the core PII‑reduction pipeline from any particular CRM / help
#     desk by delegating all network calls to **connector agents** (one per CRM).
#   * Validate that incoming / outgoing payloads conform to the canonical
#     pydantic schemas defined in `schemas.py`.
#   * Provide two ADK tools:
#       1. `route_fetch`   – given a `{source, ticket_id}` tuple, locate the
#                            appropriate connector and pull a `Ticket` object.
#       2. `route_update`  – push a `RedactedTicket` back through the same
#                            connector.
# -----------------------------------------------------------------------------


from google.adk import Agent
from .schemas import Ticket, RedactionRequest
from .utils.redaction import redact_text

_DETECTION_PROMPT = """
1. Extract every span of personally-identifiable information (PII) from
the text of the ticket_body. Offsets are 0-based (end is exclusive). Detect at least:
EMAIL, PHONE, IP, CREDIT_CARD, NATIONAL_ID, FULL_NAME,
STREET_ADDRESS, DATE_OF_BIRTH.  No prose, no markdown.
2. Formulate a list of PII entities in this format:
[
  {"start": int, "end": int, "label": str},
  ...
]
3. Formulate the output based on the output_scheme

"""


pii_detector_agent = Agent(
    name="pii_detector_agent",
    description="Detects PIIs in the Ticket body and returns Redaction Request",
    model="gemini-1.5-flash",  
    instruction=_DETECTION_PROMPT,
    input_schema=Ticket,
    output_schema=RedactionRequest,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,       
    
)


_REDACTOR_PROMPT = """
You are a deterministic redaction agent.
• Always call `redact_text` with the JSON you receive.
• If the `strategy` field is missing or null, use "mask".
• Return ONLY the tool‑call result as JSON (no prose).
"""

root_agent = Agent(
    name="pii_redactor_agent",
    description="Redacts text according to detected PII entities",
    model="gemini-1.5-flash", 
    instruction=_REDACTOR_PROMPT,
    tools=[redact_text],
    input_schema=RedactionRequest
)
