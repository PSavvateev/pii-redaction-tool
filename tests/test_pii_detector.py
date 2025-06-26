# run_detector.py
import json
from google.adk.runners import Runner, InMemorySessionService
from schemas import Ticket, PIIEntityList
from agents.pii_detector_agent import pii_detector_agent

def main():
    # 1) Build a sample ticket
    ticket = Ticket(ticket_id=1, body="Contact a@b.com.")

    # 2) Wire up the runner correctly (keyword args only)
    runner = Runner(
        agent=pii_detector_agent,
        app_name="pii_app",
        session_service=InMemorySessionService(),
    )

    # 3) Call synchronously—note it's `input=…`, not `content=…`
    out_json = runner.run_sync(
        user_id="tester",
        input=ticket.model_dump(),    
    )

    # 4) Parse & validate against your PIIEntityList schema
    entities = PIIEntityList.model_validate_json(out_json).root

    # 5) Print the result so you can eyeball it
    print(json.dumps([e.model_dump() for e in entities], indent=2))

if __name__ == "__main__":
    main()
