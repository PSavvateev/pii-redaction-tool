import os

from fastapi import FastAPI, Security, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader

from schemas import RedactedTicket, DataSourceRequest
from services.redaction_service import redact_ticket

from dotenv import load_dotenv

load_dotenv()

REDACTION_STRATEGY = os.getenv("REDACTION_STRATEGY", "mask")
CRM_ORIGIN = os.getenv("CMS_FRONTEND_ORIGIN")
LOCAL_HOST_ORIGIN=os.getenv("LOCAL_HOST_ORIGIN")

API_KEY_NAME = "x-api-key"
API_KEY=os.getenv("API_KEY")


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



@app.post("/ticket-redaction/{source}/{ticket_id}", response_model=RedactedTicket)
async def ticket_redaction(source: str,
                           ticket_id: str, 
                           api_key: str = Security(get_api_key)):
    event = DataSourceRequest(source=source,
                              ticket_id=ticket_id)

    return await redact_ticket(event=event, redaction_strategy=REDACTION_STRATEGY)