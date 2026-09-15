import logging

LOGGER = logging.getLogger("incident_intelligence")

def configure_logging(level=logging.INFO):
    if not LOGGER.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s incident_intelligence %(message)s"))
        LOGGER.addHandler(handler)
    LOGGER.setLevel(level)
