import os
from fastapi import FastAPI
from dotenv import load_dotenv
from schemas import CrmEvent, RedactedTicket, Ticket
from connectors.connector_registry import fetch_ticket, update_ticket
from utils.pii_redactor import redact_text
from agents.pii_detector_runner import detect_pii

load_dotenv()

REDACTION_STRATEGY = os.getenv("REDACTION_STRATEGY", "mask")

app = FastAPI()

@app.post("/ticket-created", response_model=RedactedTicket)
async def ticket_created(evt: CrmEvent):

    #-------------------------------------------------------
    # 1. Fetching ticket from CRM
    #-------------------------------------------------------
    ticket: Ticket = fetch_ticket(evt.source, evt.ticket_id)

    #-------------------------------------------------------
    # 2. Detecting PII entities in the ticket body (LLM Agent)
    #-------------------------------------------------------

    pii_entities = await detect_pii(ticket.ticket_body)

    #-------------------------------------------------------
    # 3. Redaction PII from the text
    #-------------------------------------------------------

    redacted_body = redact_text(ticket_body=ticket.ticket_body,
                                pii_entities=pii_entities,
                                strategy=REDACTION_STRATEGY
                                )
    #-------------------------------------------------------
    # 4. Formulating Redacted Ticket as a final outcome
    #-------------------------------------------------------
    
    redacted_ticket = RedactedTicket(source=evt.source,
                                     ticket_id=evt.ticket_id,
                                     ticket_body=redacted_body,
                                     pii_entities=pii_entities,
                                    )
    #-------------------------------------------------------
    # 5. Uopdating CRM with new redacted ticket
    #-------------------------------------------------------
    
    update_ticket(evt.source, redacted_ticket)
    
    
    return redacted_ticket
