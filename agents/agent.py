# workflow_agent.py – Ticket Redaction Orchestrator
# -----------------------------------------------------------------------------
# Purpose
# -------
# Coordinate the full PII‑reduction workflow:
#   1. Fetch raw `Ticket` from the CRM via `io_agent`.
#   2. Detect PII spans (and build a `RedactionRequest`) via `pii_detector_agent`.
#   3. Redact the text via `pii_redactor_agent`.
#   4. Push the resulting `RedactedTicket` back to the CRM via `io_agent`.
# -----------------------------------------------------------------------------

from google.adk.agents import SequentialAgent
from .io_agents import input_router_agent, output_router_agent
from .pii_detector_agent import pii_detector_agent  
from .pii_redactor_agent import pii_redactor_agent 



# ---------------------------------------------------------------------------
# 🤖 Agent definition
# ---------------------------------------------------------------------------

root_agent = SequentialAgent(
    name="ticket_reduction_orchestrator",
    description="Fetch → Detect PII → Redact → Update ticket back to CRM",
    sub_agents=[
        input_router_agent,         # 1️⃣ Fetch Ticket
        pii_detector_agent,     # 2️⃣ Detect PII, output RedactionRequest
        pii_redactor_agent,     # 3️⃣ Redact text
        output_router_agent,        # 4️⃣ Push RedactedTicket back
    ],
)
