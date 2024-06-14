from uuid import uuid4

from .session import make_request
from .types import AuthenticateResponse, AccountResponse, SignUpResponse
from .errors import AuthenticationError, SignUpError, CollectTimedBonus

from typing import Optional

CLIENT_VERSION = "61"
BASE_URL = "https://dev-nakama.winterpixel.io/v2"
BASE_HEADERS = {
    "accept": "application/json",
    "authorization": "Basic OTAyaXViZGFmOWgyZTlocXBldzBmYjlhZWIzOTo=",
    "origin": "https://rocketbotroyale2.winterpixel.io",
    "referer": "https://rocketbotroyale2.winterpixel.io/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "content-type": "application/json",
}


class RocketBotRoyale:
    def __init__(self, email: str = None, password: str = None) -> None:
        """
        Args:
            email (str): the account email
            password (str): the account password
        """

        self.email = email
        self.password = password
        self.token: Optional[str] = None
        self.authenticate()

    def authenticate(self, timeout: int = None) -> "AuthenticateResponse":
        data = {
            "email": self.email,
            "password": self.password,
            "vars": {"client_version": CLIENT_VERSION},
        }

        def check(response):
            if not response.ok:
                raise AuthenticationError(
                    response.json().get("message", "Unable to login")
                )

        response = make_request(
            f"{BASE_URL}/account/authenticate/email?create=false&",
            headers=BASE_HEADERS,
            json=data,
            fn=check,
            timeout=timeout,
        )

        response_data = AuthenticateResponse.from_dict(response)
        self.token = response_data.token

        return response_data

    def account(self, timeout: int = None) -> "AccountResponse":
        if not self.token:
            raise AuthenticationError("Token not found or user is unauthenticated")

        response = make_request(
            method="GET",
            url=f"{BASE_URL}/account",
            headers={**BASE_HEADERS, "authorization": f"Bearer {self.token}"},
            timeout=timeout,
        )

        return AccountResponse.from_dict(response)

    def collect_timed_bonus(self, timeout: int = None) -> bool:
        if not self.token:
            raise AuthenticationError("Token not found or user is unauthenticated")

        def check(response):
            if not response.ok:
                raise CollectTimedBonus(
                    response.json().get("message", "Unable to collect coins now")
                )

        make_request(
            f"{BASE_URL}/rpc/collect_timed_bonus",
            headers={
                **BASE_HEADERS,
                "authorization": f"Bearer {self.token}",
                "content-type": "application/x-www-form-urlencoded",
            },
            data='"{}"',
            fn=check,
            timeout=timeout,
        )

        return True

    @staticmethod
    def signup(email: str, password: str, username: str, timeout=None) -> bool:
        data = (
            '"{\\"display_name\\":\\"'
            + username
            + '\\",\\"email\\":\\"'
            + email
            + '\\",\\"password\\":\\"'
            + password
            + '\\"}"'
        )

        temp_account = RocketBotRoyale.__custom_account()

        def check(response):
            if not response.ok:
                raise SignUpError(response.json().get("message", "Unable to signup"))

        make_request(
            f"{BASE_URL}/rpc/winterpixel_signup",
            headers={
                **BASE_HEADERS,
                "authorization": f"Bearer {temp_account.token}",
                "content-type": "application/x-www-form-urlencoded",
            },
            data=data,
            fn=check,
            timeout=timeout,
        )

        return True

    @staticmethod
    def __custom_account(timeout=None) -> "SignUpResponse":
        data = {
            "id": f"{uuid4()}",
            "vars": {"client_version": CLIENT_VERSION, "platform": "HTML5"},
        }

        def check(response):
            if not response.ok:
                raise AuthenticationError(
                    response.json().get("message", "Unable to login")
                )

        response = make_request(
            f"{BASE_URL}/account/authenticate/custom?create=true&",
            headers=BASE_HEADERS,
            json=data,
            fn=check,
            timeout=timeout,
        )

        return SignUpResponse.from_dict(response)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self
