import re

# 
def strip_markdown(text: str) -> str:
    """
    Remove markdown code block wrapper (e.g., ```json ... ```)
    It is common that LLM output is in the markdown format.
    It should be striped before converting into json
    """
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())


