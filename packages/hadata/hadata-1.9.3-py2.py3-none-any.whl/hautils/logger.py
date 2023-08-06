import logging
import sys
from uvicorn.logging import DefaultFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

standard = logging.StreamHandler()
standard.setLevel(logging.INFO)

formatter =  DefaultFormatter()
standard.setFormatter(formatter)
logger.addHandler(standard)






