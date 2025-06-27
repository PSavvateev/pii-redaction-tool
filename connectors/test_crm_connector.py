# Dummy CRM connector ("CRM")
# -----------------------------------------------------------------------------
# Purpose
# -------
# Provide stand‑in `fetch_ticket` and `update_ticket` functions so the pipeline
# can be demo‑ed without hitting a real CRM API.
# -----------------------------------------------------------------------------

from schemas import Ticket, RedactedTicket

# In‑memory “database” keyed by ticket_id
_FAKE_DB: dict[int, str] = {
    101: (
        "Hello, my name is Alice Smith. You can reach me at "
        "alice.smith@example.com or +1‑202‑555‑0183. "
        "My SSN is 123‑45‑6789."
    ),
    102: (
        "Customer John Doe called from +1 (415) 555‑2671 on 2025‑06‑15. "
        "He gave card 4111 1111 1111 1111 for the order."
    ),
}

# ---------------------------------------------------------------------------
# 🎣 fetch_ticket
# ---------------------------------------------------------------------------

def fetch_ticket(ticket_id: int, source: str) -> Ticket:
    """Return a hard‑coded Ticket object for demo purposes."""
    body = _FAKE_DB.get(ticket_id, f"<placeholder body for ticket {ticket_id}>")
    return Ticket(source=source, ticket_id=ticket_id, ticket_body=body)

# ---------------------------------------------------------------------------
# ✏️ update_ticket
# ---------------------------------------------------------------------------

def update_ticket(ticket: RedactedTicket) -> None:
    """Pretend to push the redacted ticket back – just print to console."""
    print("[FAKE_SRM] Updated ticket", ticket.ticket_id)
    print("[FAKE_SRM] Body:", ticket.ticket_body)
    # In a real connector, you’d POST/PUT back to the CRM here.