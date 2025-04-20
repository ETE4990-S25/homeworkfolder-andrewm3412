import logging
import json
import logging.config

logger_sqldb = logging.getLogger("sqldb")
logger_ui = logging.getLogger("ui")
logger_front_js = logging.getLogger("frontend.js")
logger_back_js = logging.getLogger("backend.js")
logger_front_flask = logging.getLogger("frontend.flask")

def setup_logging():
    with open('config.json') as f:
        data = json.load(f)
        logging.config.dictConfig(data)

def main():
    setup_logging()
    logger_sqldb.info("Connection to database established successfully")
    logger_ui.warning(" User attempted to access deprecated feature")
    logger_front_js.error("Uncaught TypeError: Cannot read properties of undefined")
    logger_back_js.critical("System failure: Kernel panic triggered during file sync")
    logger_front_flask.error(" Template rendering failed due to missing context")
    try:
        1/0
    except ZeroDivisionError:
        logger_sqldb.exception("exception message")

if __name__ == "__main__":
    main()