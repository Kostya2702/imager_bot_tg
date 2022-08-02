import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# create logger
logger = logging.getLogger('debug information')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
d_handler = logging.FileHandler(filename='debug_logs.log')
d_handler.setLevel(logging.DEBUG)

# create console handler with a higher log level
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('[%(asctime)s: %(name)s - %(levelname)s] %(message)s')
d_handler.setFormatter(formatter)
c_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(d_handler)
logger.addHandler(c_handler)