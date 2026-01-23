import pytest
from pytest import MonkeyPatch

from pttautologin.account import Account
from pttautologin.account import parse_accounts_from_env


@pytest.mark.parametrize(
    "env_value, expected_accounts",
    [
        (
            "user1,pass1",
            [Account(username="user1", password="pass1")],
        ),
        (
            "user1,pass1;user2,pass2",
            [Account(username="user1", password="pass1"), Account(username="user2", password="pass2")],
        ),
    ],
)
def test_parse_accounts_from_env(env_value: str, expected_accounts: list[Account], monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("PTT_ACCOUNTS", env_value)

    accounts = parse_accounts_from_env()
    for account, expected_account in zip(accounts, expected_accounts, strict=True):
        assert account.username == expected_account.username
        assert account.password == expected_account.password
