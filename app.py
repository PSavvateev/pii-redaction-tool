import os

from fastapi import FastAPI, Security, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader

from dotenv import load_dotenv

from schemas import CrmEvent, RedactedTicket, Ticket
from connectors.connector_registry import fetch_ticket, update_ticket
from utils.pii_redactor import redact_text
from agents.pii_detector_runner import detect_pii

load_dotenv()

REDACTION_STRATEGY = os.getenv("REDACTION_STRATEGY", "mask")
CRM_ORIGIN = os.getenv("CMS_FRONTEND_ORIGIN")
LOCAL_HOST_ORIGIN=os.getenv("LOCAL_HOST_ORIGIN")

API_KEY_NAME = "x-api-key"
API_KEY=os.getenv("API_KEY")

# -------------------------
# Logging Setup
# -------------------------

from logger_config import setup_logger

logger = setup_logger()

# -------------------------
# App 
# -------------------------

app = FastAPI()

origins = [
    CRM_ORIGIN,
    LOCAL_HOST_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# API key validation
# -------------------------

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )

# -------------------------
# Routes
# -------------------------

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>PII REDACTION TOOL IS RUNNING</h1>"


@app.post("/ticket", response_model=RedactedTicket)
async def ticket_redaction(evt: CrmEvent, api_key: str = Security(get_api_key) ):

    logger.info("STARTING TICKET REDACTION WORKFLOW")

    #-------------------------------------------------------
    # 1. Fetching ticket from CRM
    #-------------------------------------------------------
    logger.info(f"1. Fetching ticket {evt.ticket_id} from {evt.source}")
    
    ticket: Ticket = fetch_ticket(evt.source, evt.ticket_id)

    logger.info(f"Ticket found: {ticket}")
    #-------------------------------------------------------
    # 2. Detecting PII entities in the ticket body (LLM Agent)
    #-------------------------------------------------------

    logger.info("2. Detecting PII Entities by LLM Agent")

    try:
        pii_entities = await detect_pii(ticket.ticket_body)
    except Exception as e:
        logger.error(f"❌ PII detection failed for ticket {evt.ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"PII detection failed: {e}")
    
    logger.info(f"PII Entities: {pii_entities}")

    #-------------------------------------------------------
    # 3. Redaction PII from the text
    #-------------------------------------------------------

    logger.info("3. Redaction PII using {REDUCTION_STRATEGY} strategy")

    redacted_body = redact_text(ticket_body=ticket.ticket_body,
                                pii_entities=pii_entities,
                                strategy=REDACTION_STRATEGY
                                )
    logger.info(f"Redacted ticket body: {redacted_body}")

    #-------------------------------------------------------
    # 4. Formulating Redacted Ticket as a final outcome
    #-------------------------------------------------------
    logger.info("4. Formulating Redacted Ticket")

    redacted_ticket = RedactedTicket(source=evt.source,
                                     ticket_id=evt.ticket_id,
                                     ticket_body=redacted_body,
                                     pii_entities=pii_entities,
                                    )
    logger.info(f"Redacted ticket: {redacted_ticket}")

    #-------------------------------------------------------
    # 5. Updating CRM with new redacted ticket
    #-------------------------------------------------------
    logger.info("5. Updating CRM with new redacted ticket")

    update_ticket(evt.source, redacted_ticket)


    logger.info("END OF REDACTION WORKFLOW")
    
    return redacted_ticket
