import logging

from dotenv import load_dotenv
from os import getenv


logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(name)s.%(funcName)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class environment:
    """
    This class will contain the environment variables for the mock bot:
    - bot_token
    - bot_trigger
    """

    def __init__(self) -> None:
        """
        Creates a environment object. If an exception is raised retrieving environment
        variables, all elements of the environment class will be set to None
        """
        logger.info("Retrieving environment variables")
        try:
            load_dotenv()
            self.bot_token = getenv("BOT_TOKEN", None)
            self.bot_trigger = getenv("BOT_TRIGGER", None)
        except Exception as ex:
            self.bot_token = None
            self.bot_trigger = None
            logger.critical(
                "Failed to retrieve environment variables. Please verify environment variable exists"
            )
            logger.critical(ex)
