from importlib import import_module
from schemas import RedactedTicket

_CONNECTORS = {
    "test": "connectors.test_crm_connector",
    "zendesk":  "connectors.zendesk_crm_connector",
    "salesforce": "connectors.zendesk_crm_connector",
}

def fetch_ticket(source: str, ticket_id: int):
    return import_module(_CONNECTORS[source]).fetch_ticket(
        ticket_id=ticket_id
    )

def update_ticket(source: str, redacted_ticket: RedactedTicket):
    return import_module(_CONNECTORS[source]).update_ticket(redacted_ticket)
