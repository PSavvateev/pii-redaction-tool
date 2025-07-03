# redaction_utils.py
import hashlib
from typing import List
from schemas import PIIEntity

def redact_text(
    ticket_body: str,
    pii_entities: List[PIIEntity],
    strategy: str = "mask" # default
) -> str:
    """
    Redacts each exact match of `text` from the list of PII entities using the given strategy:
    - mask:     replace each character with '*'
    - tokenize: replace with {{LABEL:deterministic-token}}
    - hash:     replace with {{LABEL:sha256-hex}}
    """


    def make_token(span: str):
        return hashlib.sha1(span.encode('utf-8')).hexdigest()[:8]
    
    redacted_text = ticket_body

    # Sort descending by start so indexes don’t shift
    for e in sorted(pii_entities, key=lambda e: e.start, reverse=True):
        span = redacted_text[e.start : e.end]
        # print(f"Redacting span: '{span}' at [{e.start}:{e.end}] with strategy='{strategy}'")
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
    
    
    return redacted_text
