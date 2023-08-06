""""""
import logging
import logging.config
import sys
from pathlib import Path

import toml


def handler(signal_code, _) -> None:
    """Signal handler."""
    logging.debug(f"Shutting down because signal {signal_code} was received.")
    sys.exit(1)


def read_toml(file_path: Path) -> dict:
    """Return the contents of a toml file as a dictionary."""
    if not file_path.exists():
        logging.critical(f"{file_path} does not exist!")
        sys.exit(1)
    try:
        return dict(toml.loads(file_path.read_text()))
    except (toml.TomlDecodeError, TypeError) as error:
        logging.critical(f"Toml format error: {error}.")
        sys.exit(1)
