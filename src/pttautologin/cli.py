import asyncio
import os
from dataclasses import dataclass
from dataclasses import field

import nest_asyncio
import PyPtt
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger


@dataclass
class Account:
    username: str
    password: str = field(repr=False)


def login_and_logout(account: Account) -> None:
    client = PyPtt.API()
    logged_in = False
    try:
        client.login(
            ptt_id=account.username,
            ptt_pw=account.password,
            kick_other_session=False,
        )
        logged_in = True
    except PyPtt.exceptions.LoginError:
        logger.error("Login error")
    except PyPtt.exceptions.LoginTooOften:
        logger.error("Login too often")
    except PyPtt.exceptions.WrongIDorPassword:
        logger.error("Wrong ID or password")
    finally:
        if logged_in:
            client.logout()
        client.close()


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


async def run() -> None:
    load_dotenv(find_dotenv(), override=True)

    accounts = parse_accounts_from_env()

    tasks = []
    for account in accounts:
        tasks.append(
            asyncio.to_thread(
                login_and_logout,
                account,
            )
        )
    await asyncio.gather(*tasks)

    # Allow pending async tasks to complete gracefully
    await asyncio.sleep(0.1)


def main() -> None:
    nest_asyncio.apply()
    asyncio.run(run())
