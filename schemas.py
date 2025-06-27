from typing import List
from pydantic import BaseModel, Field, ConfigDict, RootModel

# -----------------------------------------------------------------------------
# 🗂️  SCHEMAS (pydantic models)
# -----------------------------------------------------------------------------


# receiving from CRM hook
class CrmEvent(BaseModel):
    source: str
    ticket_id: int

    class ConfigDict:
        schema_extra = {
            "example": {
                "source": "zendesk",
                "ticket_id": 12
            }
        }
# Ticket Received from CRM (to be passed to PII Detector)
class Ticket(BaseModel):
    source: str
    ticket_id: int
    ticket_body: str

    class ConfigDict:
        schema_extra = {
            "example": {
                "source": "str",
                "ticket_id": 12345,
                "body": "Hello, my email is john@example.com and my SSN is 123-45-6789."
            }
        }

# Identified entities for further redaction
class PIIEntity(BaseModel):
    start: int = Field(..., ge=0)
    end:   int = Field(..., gt=0)
    end:   int = Field(..., ge=1)   # use inclusive minimum so Pydantic emits `"minimum": 1` instead of `"exclusiveMinimum"`

    label: str

    class ConfigDict:
        schema_extra = {
            "example": {"start": 42, "end": 56, "label": "EMAIL_ADDRESS"}
        }

# Request on redaction from PII Detector to PII Redactor
class RedactionRequest(BaseModel):
    source: str
    ticket_id: int
    ticket_body: str
    entities: List[PIIEntity]
    #strategy: str = Field("tokenize", pattern="^(mask|tokenize|hash)$")

# Redacted ticket
class RedactedTicket(BaseModel):
    source: str
    ticket_id: int
    ticket_body: str
    entities: List[PIIEntity]

    class ConfigDict:
        schema_extra = {
            "example": {
                "source": "crm",
                "ticket_id": 12345,
                "body": "Hello, my email is {{EMAIL:f0e1d2c3}} and my SSN is {{US_SOCIAL_SECURITY_NUMBER:abc12345}}.",
                "entities": [
                    {"start": 18, "end": 36, "label": "EMAIL_ADDRESS"},
                    {"start": 53, "end": 64, "label": "US_SOCIAL_SECURITY_NUMBER"}
                ]
            }
        }


class IoRouterPayload(RootModel[CrmEvent |RedactedTicket]):
    """Either a TicketEvent or an UpdateEvent."""