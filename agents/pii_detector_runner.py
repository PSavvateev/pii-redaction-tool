import uuid
import asyncio

import json
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner, types
from agents.pii_detector_agent import pii_detector_agent
from schemas import PIIEntity

from utils.markdown_stripper import strip_markdown


APP_NAME  = "pii_redaction_app"
USER_ID   = "fast_api_service"

session_service = InMemorySessionService()


runner = Runner(
                agent=pii_detector_agent,
                app_name=APP_NAME,
                session_service=session_service,
                
                )

# print(f"Runner created for agent '{runner.agent.name}'.")


async def detect_pii(ticket_body: str) -> list[PIIEntity]:
    """
    Synchronously detect PII spans

    """

    session_id = str(uuid.uuid4())
   
    # 1. Create the specific session where the conversation will happen
    await session_service.create_session(
                        app_name=APP_NAME,
                        user_id=USER_ID,
                        session_id=session_id
                        )
    print(f"✅ Session created: {session_id}")   
  
    # 2. ADK Agent needs the payload wrapped in a Content object:
    message = types.Content(role="user", parts=[types.Part(text=ticket_body)])
    # print(f"📩 Message: {message}")

    # 3. Main Agent Runner loop
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message
    ):
        # print("🔄 Received event")

        if event.is_final_response():
            # print("✅ Final response found")

            if event.content and event.content.parts:
                raw_payload = event.content.parts[0].text
                # print(f"📦 Payload: {raw_payload}")

                clean_payload = strip_markdown(raw_payload)               
                # print(f"📦 Payload: {clean_payload}")

                json_payload = json.loads(clean_payload)
                # print(f"📦 JSON Payload: {json_payload}")

                entities = [PIIEntity(**e) for e in json_payload]
                # print(f"📦 Entities: {entities}")

                return entities

    raise RuntimeError("❌ Received no final response with JSON")

    
    

