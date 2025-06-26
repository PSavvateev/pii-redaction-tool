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
from schemas import Ticket, RedactedTicket

from utils.connector_registry import resolve_tool


# ---------------------------------------------------------------------------
# 🎣 route_fetch
# ---------------------------------------------------------------------------

def route_fetch(source: str, ticket_id: int) -> Ticket:
    """Fetch a ticket via the appropriate CRM connector."""
    fetch_fn = resolve_tool(source, "fetch_ticket")
    ticket = fetch_fn(ticket_id)
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
# 🤖 Agent definition
# ---------------------------------------------------------------------------
io_agent = Agent(
    name="io_router_agent",
    description=(
        "Schema-validated router that delegates ticket I/O to CRM-specific connector agents."
    ),
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    tools=[route_fetch, route_update],
)

