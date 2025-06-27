from google.adk import Agent              
from schemas import Ticket, RedactionRequest


_DETECTION_PROMPT = """
1. Extract every span of personally-identifiable information (PII) from
the text of the ticket_body. Offsets are 0-based (end is exclusive).
Personally Identifiable Information (PII) includes data that can be used to identify, contact, or locate a specific individual. 
Examples include full name, social security number, driver's license number, passport number, financial account numbers, medical records, email addresses, phone numbers, date of birth, place of birth, ZIP Code, IP addresses. 

2. Formulate a list of PII entities in this format:
[
  {"start": int, "end": int, "label": str},
  ...
]
3. Formulate the output based on the output_scheme

"""

# ---------------------------------------------------------------------------
# 🤖 Agent definition
# ---------------------------------------------------------------------------

pii_detector_agent = Agent(
    name="pii_detector_agent",
    description="Detects PIIs in the Ticket body and returns Redaction Request",
    model="gemini-1.5-flash",  
    instruction=_DETECTION_PROMPT,
    input_schema=Ticket,
    output_schema=RedactionRequest,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,       
    
)
