import os

import PyPtt
import typer
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

app = typer.Typer()


def login_and_logout(ptt_id: str, ptt_pw: str) -> None:
    client = PyPtt.API()
    try:
        client.login(
            ptt_id=ptt_id,
            ptt_pw=ptt_pw,
            kick_other_session=False,
        )
    except PyPtt.exceptions.LoginError as e:
        logger.error(f"Login error: {e}")
    except PyPtt.exceptions.LoginTooOften as e:
        logger.error(f"Login too often: {e}")
    except PyPtt.exceptions.WrongIDorPassword as e:
        logger.error(f"Wrong ID or password: {e}")

    finally:
        client.logout()


@app.command()
def main() -> None:
    load_dotenv(
        find_dotenv(raise_error_if_not_found=True),
        override=True,
    )

    ptt_id = os.getenv("PTT_ACCOUNT")
    if ptt_id is None:
        logger.error("PTT_ACCOUNT is not set.")
        return
    ptt_pw = os.getenv("PTT_PASSWORD")
    if ptt_pw is None:
        logger.error("PTT_PASSWORD is not set.")
        return

    login_and_logout(ptt_id, ptt_pw)
