# Dummy CRM connector
# -----------------------------------------------------------------------------
# Purpose
# -------
# Provide stand‑in `fetch_ticket` and `update_ticket` functions so the pipeline
# can be demo‑ed without hitting a real CRM API.
# -----------------------------------------------------------------------------
import json
import os

from app.models.pydentic_model import Ticket, RedactedTicket, Interaction
 
# Load JSON from file
with open(os.path.join(os.path.dirname(__file__), "mock_db.json"), "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Convert list of tickets into a dict for easy lookup by ticket ID
RAW_DB = {t["id"]: t for t in raw_data["mock_database"]}



def fetch_ticket(ticket_id: str) -> Ticket:
    """Fetch a ticket from the test JSON file and adapt field names to match schemas."""
    raw_ticket = RAW_DB.get(ticket_id)
    if not raw_ticket:
        raise ValueError(f"Ticket ID {ticket_id} not found in test database.")

    # Rename interaction "id" → "interaction_id"
    interactions = [
        Interaction(
            interaction_id=interaction["id"],
            interaction_body=interaction["interaction_body"]
        )
        for interaction in raw_ticket["interactions"]
    ]

    # Return Ticket with ticket_id and transformed interactions
    return Ticket(
        ticket_id=raw_ticket["id"],
        interactions=interactions
    )


def update_ticket(ticket: RedactedTicket) -> None:
    """Pretend to push the redacted ticket back – just print to console."""
    print("[TEST_CRM] Updated ticket", ticket.ticket_id)
    print("[TEST_CRM] INteractions:", ticket.interactions)
