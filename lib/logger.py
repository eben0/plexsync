import logging
from os import environ


def setup_logger():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-4s] %(message)s",
        level=environ.get("LOG_LEVEL", "INFO"),
        datefmt="%d-%m-%Y %H:%M:%S",
    )
