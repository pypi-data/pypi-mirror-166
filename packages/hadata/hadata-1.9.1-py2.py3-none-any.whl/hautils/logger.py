import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
logger.addHandler(sh)
logFormatter = logging.Formatter(logging.BASIC_FORMAT)
sh.setFormatter(logFormatter)







