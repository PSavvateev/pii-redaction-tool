import re
   
from app.schemas import PIIEntity
from typing import List, Dict


def locate_pii_spans(text: str, spans: List[Dict[str, str]]) -> List[PIIEntity]:
    """
    Finds and returns the start and end character positions of each PII span in the original text.

    --- FUNCTION DESCRIPTION ---
    Given a block of text and a list of PII spans (each span includes a `label` and the `text` to be found),
    this function searches the input text for the exact location of each PII span and returns a list of
    PII entities, where each entity includes:

    - `start`: The index where the PII span begins in the text.
    - `end`: The index where the PII span ends (exclusive).
    - `label`: The category of the PII (e.g., "email", "phone_number", etc.).

    --- PARAMETERS ---
    text (str): The full original text where PII needs to be located.
    
    spans (List[Dict]): A list of dictionaries where each item has:
        - "text" (str): The exact span of PII (must exist in `text`).
        - "label" (str): The category/type of the PII span.

    Example input:
    text = "Contact John Smith at john.smith@example.com."
    spans = [
        {"label": "name", "text": "John Smith"},
        {"label": "email", "text": "john.smith@example.com"}
    ]

    --- RETURNS ---
    List[Dict]: A list of dictionaries where each item has:
        - "start" (int): Start index of the PII span.
        - "end" (int): End index (exclusive).
        - "label" (str): The PII label.

    Example output:
    [
        {"start": 8, "end": 18, "label": "name"},
        {"start": 22, "end": 46, "label": "email"}
    ]

    --- NOTES ---
    - Assumes each span appears **exactly once** in the text.
    - Spans must match exactly — casing and spacing are important.
    - If a span is not found, the function may raise an error or skip it.

    """
    entities: List[PIIEntity] = []

    for span in spans:
        label = span["label"]
        snippet = span["text"]

        if not snippet:
            continue

        # Escape special regex characters in snippet
        pattern = re.escape(snippet)
        for match in re.finditer(pattern, text):
            entities.append(PIIEntity(
                start=match.start(),
                end=match.end(),
                label=label
            ))
    # print("Check of the function outcome - just for testing:")
    # print(entities)        

    return entities
