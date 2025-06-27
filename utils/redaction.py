# redaction_utils.py
import hashlib
from typing import List
from schemas import PIIEntity, RedactedTicket

def redact_text(
    ticket_id: int,    
    ticket_body: str,
    entities: List[PIIEntity],
    strategy: str = "mask"
) -> RedactedTicket:
    """
    Redacts each span in `entities` within `text` using the given strategy:
    - mask: replace each character with '*'
    - tokenize: {{LABEL:deterministic‐token}}
    - hash:     {{LABEL:sha256‐hex}}
    Returns a RedactedTicket(ticket_id, ticket_body, entities).
    """


    def make_token(span: str):
        # you could use uuid.uuid5 for deterministic tokens, or sha1:
        return hashlib.sha1(span.encode('utf-8')).hexdigest()[:8]
    
    redacted_text = ticket_body

    # Sort descending by start so indexes don’t shift
    for e in sorted(entities, key=lambda e: e.start, reverse=True):
        span = redacted_text[e.start : e.end]
        if strategy == "mask":
            replacement = "*" * len(span)
        elif strategy == "tokenize":
            token = make_token(span)
            replacement = f"{{{{{e.label}:{token}}}}}"
        elif strategy == "hash":
            digest = hashlib.sha256(span.encode('utf-8')).hexdigest()
            replacement = f"{{{{{e.label}:{digest}}}}}"
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        redacted_text = (
            redacted_text[: e.start] + replacement + redacted_text[e.end :]
        )
    
    
    return RedactedTicket(
        ticket_id=ticket_id,
        ticket_body=redacted_text,
        entities=entities,
    )
