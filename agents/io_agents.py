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
from schemas import Ticket, RedactedTicket, CrmEvent

from utils.connector_registry import resolve_tool

_INPUT_PROMPT = """
You are a router.

• If the JSON object has keys `source` AND `ticket_id` and does NOT have `ticket_body`,
  • Call the tool `route_fetch` exactly once.

• Otherwise (it already has `ticket_body`),
  • Do NOT call any tool; return the object unchanged.

Return no prose.
"""

_OUTPUT_PROMPT = """
You are a routing agent that never generates content yourself.
When you receive JSON that matches RedactedTicket,
call `route_update` exactly once to push the redacted ticket back.
DO NOT call any tool again.
Return ONLY the tool call output JSON—no additional prose.
"""


# ---------------------------------------------------------------------------
# 🎣 route_fetch
# ---------------------------------------------------------------------------

def route_fetch(source: str, ticket_id: int) -> Ticket:
    """Fetch a ticket via the appropriate CRM connector."""
    fetch_fn = resolve_tool(source, "fetch_ticket")
    ticket = fetch_fn(ticket_id, source)
    if not isinstance(ticket, Ticket):
        raise TypeError(
            f"Connector '{source}' returned {type(ticket)}, expected Ticket"
        )
    return ticket


# ---------------------------------------------------------------------------
# ✏️ route_update
# ---------------------------------------------------------------------------

def route_update(source: str, ticket: RedactedTicket) -> None:
    """Push the redacted ticket back through the same connector."""
    update_fn = resolve_tool(source, "update_ticket")
    update_fn(ticket)


# ---------------------------------------------------------------------------
# 🤖 Agents definition
# ---------------------------------------------------------------------------


input_router_agent = Agent(
    name="input_router_agent",
    description="Fetch Ticket via CRM connector",
    model="gemini-1.5-flash",
    instruction=_INPUT_PROMPT,
    input_schema=CrmEvent,
    tools=[route_fetch],
    
)


output_router_agent = Agent(
    name="output_router_agent",
    description="Update Ticket via CRM connector",
    model="gemini-1.5-flash",
    instruction=_OUTPUT_PROMPT,
    input_schema=RedactedTicket,
    tools=[route_update],
    
)

