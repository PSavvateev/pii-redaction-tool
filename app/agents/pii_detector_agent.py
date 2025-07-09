
from google.adk import Agent              
from .prompts import DETECTION_PROMPT
from app.utils.pii_spans_locator import locate_pii_spans


pii_detector_agent = Agent(
    name="pii_detector_agent",
    description="Detects PII in a ticket body and returns spans to redact.",
    model="gemini-1.5-flash",  
    instruction=DETECTION_PROMPT,
    tools=[locate_pii_spans]
)
