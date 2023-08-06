import logging
import sys
from uvicorn.logging import AccessFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

standard = logging.StreamHandler()
standard.setLevel(logging.INFO)

formatter =  AccessFormatter()
standard.setFormatter(formatter)
logger.addHandler(standard)






