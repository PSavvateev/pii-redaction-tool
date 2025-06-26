from google.adk import Agent              
from schemas import Ticket, RedactionRequest


_DETECTION_PROMPT = """
1. Extract every span of personally-identifiable information (PII) from
the text of the ticket_body. Offsets are 0-based (end is exclusive). Detect at least:
EMAIL, PHONE, IP, CREDIT_CARD, NATIONAL_ID, FULL_NAME,
STREET_ADDRESS, DATE_OF_BIRTH.  No prose, no markdown.
2. Formulate a list of PII entities in this format:
[
  {"start": int, "end": int, "label": str},
  ...
]
3. Formulate the output based on the output_scheme

"""


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
