import logging

# Create a logger with the name of the current module
logger = logging.getLogger(__name__)

# Set the log level to debug
logger.setLevel(logging.DEBUG)

# Create a console handler and set the log level to debug
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(consoleHandler)
