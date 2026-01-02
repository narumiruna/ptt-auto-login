import os
from dataclasses import dataclass
from dataclasses import field

import PyPtt
import typer
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

app = typer.Typer()


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
    except PyPtt.exceptions.LoginError as e:
        logger.error(f"Login error: {e}")
    except PyPtt.exceptions.LoginTooOften as e:
        logger.error(f"Login too often: {e}")
    except PyPtt.exceptions.WrongIDorPassword as e:
        logger.error(f"Wrong ID or password: {e}")
    finally:
        if logged_in:
            client.logout()


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


@app.command()
def main() -> None:
    load_dotenv(find_dotenv(), override=True)

    accounts = parse_accounts_from_env()
    for account in accounts:
        login_and_logout(account)
