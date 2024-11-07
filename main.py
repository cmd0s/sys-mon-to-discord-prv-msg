import logging
from discord_handler import DiscordHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('application.log', encoding='utf-8')

    # Set levels for handlers (optional)
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logging.info('Logging is set up.')

if __name__ == "__main__":
    setup_logging()
    logging.info('Application is starting.')
    discord_handler = DiscordHandler()
    discord_handler.run_bot()
