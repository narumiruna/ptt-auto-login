import os
from dataclasses import dataclass
from dataclasses import field

from loguru import logger


@dataclass
class Account:
    username: str
    password: str = field(repr=False)


def parse_accounts_from_env() -> list[Account]:
    raw = os.getenv("PTT_ACCOUNTS", "").strip()
    if not raw:
        logger.error("No PTT accounts found in environment variable 'PTT_ACCOUNTS'.")
        return []

    accounts = []

    for entry in raw.split(";"):
        try:
            username, password = entry.split(",")
            accounts.append(Account(username=username.strip(), password=password.strip()))
        except ValueError:
            logger.error(
                "Invalid account format in PTT_ACCOUNTS. Expected format is 'account,password'. "
                "The malformed entry has been skipped."
            )

    return accounts
