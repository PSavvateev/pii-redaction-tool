from schemas import DataSourceRequest, RedactedTicket, Ticket, Interaction, RedactedInteraction
from typing import List
from connectors.connector_registry import fetch_ticket, update_ticket
from utils.pii_redactor import redact_text
from agents.pii_detector_runner import detect_pii


from logger_config import setup_logger
logger = setup_logger()


async def redact_ticket(event: DataSourceRequest, redaction_strategy: str) -> RedactedTicket:

    logger.info("▶️ STARTING TICKET REDACTION WORKFLOW")

    #-------------------------------------------------------
    # 1. Fetching ticket from CRM
    #-------------------------------------------------------
    logger.info(f"1.🔌 Fetching ticket {event.ticket_id} from {event.source}")
    
    ticket: Ticket = fetch_ticket(event.source, event.ticket_id)

    logger.debug(f"✅ Ticket found: {ticket}")
    #-------------------------------------------------------
    # 2. Detecting & Reducting PII entities for each Interaction in the ticket (LLM Agent)
    #-------------------------------------------------------

    logger.info("2. 🛠️ Detecting & Reducting PII entities for each Interaction")

    interactions: List[Interaction] = ticket.interactions
    redacted_interactions: List[RedactedInteraction] = []

    for interaction in interactions:     
        try:
            # 2a. PII Detection
            logger.info(f"2a. 🔍 Detecting PII Entities for interaction {interaction.interaction_id}")
            
            pii_entities = await detect_pii(interaction.interaction_body)
            logger.debug(f"✅ PII Entities: {pii_entities} for interaction {interaction.interaction_id}")
            
            

            # 2b. PII redaction
            logger.info(f"2b. ✂️ Redaction PII using {redaction_strategy} strategy")

            redacted_body = redact_text(text=interaction.interaction_body,
                                        pii_entities=pii_entities,
                                        strategy=redaction_strategy
                                        )
            
            logger.debug(f"✅ Redacted interaction body: {redacted_body}")

            # 2c. Formulating Redacted Interaction
            logger.info("2c. 📝 Formulating Redacted Interaction")

            redacted_interaction = RedactedInteraction(interaction_id=interaction.interaction_id,
                                                        interaction_body=redacted_body,
                                                        pii_entities=pii_entities

                                                        )
            logger.debug(f"✅ Redacted interaction: {redacted_interaction}")

            # 2d. Appending list of Redacted Interactions
            logger.info("2d. 💾 Updating list of Redacted Interactions")

            redacted_interactions.append(redacted_interaction)
            
        
        except Exception as e:
                logger.warning(f"⚠️ Skipping interaction {interaction.interaction_id} — LLM output could not be parsed: {e}")
                logger.info(f"2a. 🛑 No PII found or failed parsing for interaction {interaction.interaction_id}, skipping redaction.")

    logger.debug(f"✅ Final list of redacted interactions: {redacted_interactions}")

    #-------------------------------------------------------
    # 3. Formulating Redacted Ticket as a final outcome
    #-------------------------------------------------------
    logger.info("3. 📝 Formulating Redacted Ticket")

    redacted_ticket = RedactedTicket(ticket_id=event.ticket_id,
                                     interactions=redacted_interactions,                                    
                                    )
    logger.debug(f"✅ Redacted ticket: {redacted_ticket}")

    #-------------------------------------------------------
    # 4. Updating CRM with new redacted ticket
    #-------------------------------------------------------
    logger.info("4.🔌 Updating CRM with new redacted ticket")

    update_ticket(event.source, redacted_ticket)


    logger.info("⏹️  END OF REDACTION WORKFLOW")
    
    return redacted_ticket
