import asyncio

import nest_asyncio
import PyPtt
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from .account import Account
from .account import parse_accounts_from_env


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


async def run() -> None:
    load_dotenv(find_dotenv(), override=True)

    accounts = parse_accounts_from_env()
    logger.info(f"Found {len(accounts)} accounts to process.")

    logger.info("Starting login and logout tasks...")
    await asyncio.gather(
        *[
            asyncio.to_thread(
                login_and_logout,
                account,
            )
            for account in accounts
        ]
    )


def main() -> None:
    nest_asyncio.apply()
    asyncio.run(run())
