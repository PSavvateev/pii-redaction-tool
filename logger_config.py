# logger_config.py

import logging

APP_LOGGER_NAME = "pii_redaction_app"

def setup_logger() -> logging.Logger:
    logger = logging.getLogger(APP_LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times in case of re-import
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Prevent logs from propagating to the root logger
        logger.propagate = False
        
    silence_third_party_loggers()

    return logger

def silence_third_party_loggers():
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)