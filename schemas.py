from typing import List
from pydantic import BaseModel, Field, ConfigDict

# ---------------------------------------------------------
# Sending API request to Data Source
# ---------------------------------------------------------

class DataSourceRequest(BaseModel):
    source: str
    ticket_id: str

    model_config = ConfigDict(
        title="Data Source Request",
        description="request sent to an external system, containing the data source name and a ticket ID.",
        json_schema_extra={
        "example": {
            "source": "zendesk",
            "ticket_id": "123456"
        }
    })


# ---------------------------------------------------------
# A single customer interaction (e.g. comment, message, email)
# ---------------------------------------------------------

class Interaction(BaseModel):
    interaction_id: str
    interaction_body: str
    model_config = ConfigDict(
        title="Interaction",
        description="A single customer interaction related to the support ticket, such as a message, email, or comment.",
        json_schema_extra={
        "example": {
            "interaction_id": "abc789",
            "interaction_body": "Hi, my name is John Doe. My email is john@example.com."
        }
    })



# ---------------------------------------------------------
# Ticket received from data source with interactions
# ---------------------------------------------------------

class Ticket(BaseModel):
    ticket_id: str
    interactions: List[Interaction]
    model_config = ConfigDict(
        title="Ticket",
        description="A support ticket that includes a unique ID and a list of associated customer interactions.",
        json_schema_extra={
        "example": {
            "ticket_id": "123456",
            "interactions": [
                {
                    "interaction_id": "abc789",
                    "interaction_body": "Hi, my name is John Doe. My email is john@example.com."
                },
                {
                    "interaction_id": "def456",
                    "interaction_body": "Please reach out at +1-202-555-0100 if you need more info."
                }
            ]
        }
    })


# ---------------------------------------------------------
# A single detected PII span
# ---------------------------------------------------------

class PIIEntity(BaseModel):
    start: int = Field(..., ge=0)
    end: int = Field(..., ge=1)
    label: str
    model_config = ConfigDict(
        title="PII Entity",
        description="A span of text identified as personally identifiable information (PII), with start and end character positions and a label.",
        json_schema_extra={
        "example": {
            "start": 18,
            "end": 27,
            "label": "email"
        }
    })


# ---------------------------------------------------------
# Final output: redacted Interaction and Redacted Ticket
# ---------------------------------------------------------

class RedactedInteraction(BaseModel):
    interaction_id: str
    interaction_body: str
    pii_entities: List[PIIEntity]
    model_config = ConfigDict(
        title="Redacted Interaction",
        description="A customer interaction with redacted text and metadata about identified PII spans.",
        json_schema_extra={
        "example": {
            "interaction_id": "abc789",
            "interaction_body": "Hi, my name is **********. My email is *********************.",
            "pii_entities": [
                {"start": 11, "end": 21, "label": "name"},
                {"start": 33, "end": 53, "label": "email"}
            ]
        }
    })


class RedactedTicket(BaseModel):
    ticket_id: str
    interactions: List[RedactedInteraction]
    model_config = ConfigDict(
        title="Redacted Ticket",
        description="Final redaction result for a support ticket, containing all redacted interactions and their detected PII entities.",
        json_schema_extra={
        "example": {
            "ticket_id": "123456",
            "interactions": [
                {
                    "interaction_id": "abc789",
                    "interaction_body": "Hi, my name is **********. My email is *********************.",
                    "pii_entities": [
                                {"start": 11, "end": 21, "label": "name"},
                                {"start": 33, "end": 53, "label": "email"}
                                ]
                },
                {
                    "interaction_id": "def456",
                    "interaction_body": "Please reach out at *************** if you need more info.",
                    "pii_entities": [
                                {"start": 24, "end": 42, "label": "phone_number"}
                                ]
                }
            ]
           
        }
    })
