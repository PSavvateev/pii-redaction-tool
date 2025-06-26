from typing import List
from pydantic import BaseModel, Field, ConfigDict, RootModel

# -----------------------------------------------------------------------------
# 🗂️  SCHEMAS (pydantic models)
# -----------------------------------------------------------------------------

class PIIEntity(BaseModel):
    start: int = Field(..., ge=0)
    end:   int = Field(..., gt=0)
    end:   int = Field(..., ge=1)   # use inclusive minimum so Pydantic emits `"minimum": 1` instead of `"exclusiveMinimum"`

    label: str

    class ConfigDict:
        schema_extra = {
            "example": {"start": 42, "end": 56, "label": "EMAIL_ADDRESS"}
        }

class PIIEntityList(RootModel[List[PIIEntity]]):
    """Wrapper so ADK’s output_schema is a real Pydantic model."""
    pass

class Ticket(BaseModel):
    ticket_id: int
    ticket_body: str

    class ConfigDict:
        schema_extra = {
            "example": {
                "ticket_id": 12345,
                "body": "Hello, my email is john@example.com and my SSN is 123-45-6789."
            }
        }


class RedactionRequest(BaseModel):
    ticket_id: int
    ticket_body: str
    entities: List[PIIEntity]
    #strategy: str = Field("tokenize", pattern="^(mask|tokenize|hash)$")


class RedactedTicket(BaseModel):
    ticket_id: int
    ticket_body: str
    entities: List[PIIEntity]

    class ConfigDict:
        schema_extra = {
            "example": {
                "ticket_id": 12345,
                "body": "Hello, my email is {{EMAIL:f0e1d2c3}} and my SSN is {{US_SOCIAL_SECURITY_NUMBER:abc12345}}.",
                "entities": [
                    {"start": 18, "end": 36, "label": "EMAIL_ADDRESS"},
                    {"start": 53, "end": 64, "label": "US_SOCIAL_SECURITY_NUMBER"}
                ]
            }
        }