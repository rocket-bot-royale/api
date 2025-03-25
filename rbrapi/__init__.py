from __future__ import annotations

__version__ = "0.7"

from json import loads
from typing import Optional, Self
from uuid import uuid4

from .errors import (
    AuthenticationError,
    CollectTimedBonusError,
    FriendRequestError,
    LootBoxError,
    SignUpError,
    UnknownUserError,
)
from .session import make_request
from .types import (
    AccountResponse,
    AuthenticateResponse,
    LootBoxResponses,
    SignUpResponse,
)

CLIENT_VERSION = "9999999999"  # will never raise an AuthenticationError for having an older client version
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
    def __init__(self: Self, email: str, password: str) -> None:
        """
        Initialize RocketBotRoyale instance with email and password.

        Args:
            email (str): The account email.
            password (str): The account password.
        """

        self.email = email
        self.password = password
        self.token: Optional[str] = None
        self.authenticate()

    def authenticate(self: Self, timeout: Optional[int] = None) -> AuthenticateResponse:
        """
        Authenticate the user.

        Args:
            timeout (int, optional): Timeout for the request in seconds.

        Returns:
            AuthenticateResponse: Response object containing authentication details.

        Raises:
            AuthenticationError: If authentication fails.
        """

        data = {
            "email": self.email,
            "password": self.password,
            "vars": {"client_version": CLIENT_VERSION},
        }

        response = make_request(
            f"{BASE_URL}/account/authenticate/email?create=false&",
            headers=BASE_HEADERS,
            json=data,
            timeout=timeout,
            error_if_not_ok=AuthenticationError,
        )

        response_data = AuthenticateResponse.from_dict(response)
        self.token = response_data.token

        return response_data

    def account(self: Self, timeout: Optional[int] = None) -> AccountResponse:
        """
        Retrieve account details for the authenticated user.

        Args:
            timeout (int, optional): Timeout for the request in seconds.

        Returns:
            AccountResponse: Response object containing account details.

        Raises:
            AuthenticationError: If authentication token is missing or invalid.
        """

        if not self.token:
            raise AuthenticationError("Token not found or user is unauthenticated")

        response = make_request(
            method="GET",
            url=f"{BASE_URL}/account",
            headers={**BASE_HEADERS, "authorization": f"Bearer {self.token}"},
            timeout=timeout,
        )

        return AccountResponse.from_dict(response)

    def collect_timed_bonus(self: Self, timeout: Optional[int] = None) -> bool:
        """
        Collect timed bonus.

        Args:
            timeout (int, optional): Timeout for the request in seconds.

        Returns:
            bool: True if timed bonus collection was successful.

        Raises:
            AuthenticationError: If authentication token is missing or invalid.
            CollectTimedBonusError: If collecting timed bonus fails.
        """
        if not self.token:
            raise AuthenticationError("Token not found or user is unauthenticated")

        data = '"{}"'
        make_request(
            f"{BASE_URL}/rpc/collect_timed_bonus",
            headers={
                **BASE_HEADERS,
                "authorization": f"Bearer {self.token}",
                "content-type": "application/x-www-form-urlencoded",
            },
            data=data,
            error_if_not_ok=CollectTimedBonusError,
            timeout=timeout,
        )

        return True

    def send_friend_request(
        self: Self, friend_code: str, timeout: Optional[int] = None
    ) -> bool:
        """
        Send a friend request.

        Args:
            friend_code (str): The friend code of the user to send the friend request to.
            timeout (int, optional): Timeout for the request in seconds.

        Returns:
            bool: True if the friend request was sent successfully.

        Raises:
            AuthenticationError: If authentication token is missing or invalid.
            FriendRequestError: If sending the friend request fails.
        """

        if not self.token:
            raise AuthenticationError("Token not found or user is unauthenticated")

        data = '"{\\"friend_code\\":\\"' + friend_code + '\\"}"'
        make_request(
            f"{BASE_URL}/rpc/winterpixel_query_user_id_for_friend_code",
            headers={
                **BASE_HEADERS,
                "authorization": f"Bearer {self.token}",
                "content-type": "application/x-www-form-urlencoded",
            },
            data=data,
            error_if_not_ok=FriendRequestError,
            timeout=timeout,
        )

        return True

    def buy_crate(
        self: Self, *, elite: bool = False, timeout: Optional[int] = None
    ) -> LootBoxResponses:
        """
        Purchase a crate.

        Args:
            elite (bool, optional): Indicates if the crate to be bought is elite. Defaults to False.
            timeout (int, optional): Timeout for the request in seconds.

        Returns:
            LootBoxResponses: Response object containing details of the purchased crate.

        Raises:
            AuthenticationError: If authentication token is missing or invalid.
            LootBoxError: If purchasing the crate fails.
        """

        if not self.token:
            raise AuthenticationError("Token not found or user is unauthenticated")

        data = f'"{{\\"unique\\":{"true" if elite else "false"}}}"'
        response = make_request(
            f"{BASE_URL}/rpc/tankkings_consume_lootbox",
            headers={
                **BASE_HEADERS,
                "authorization": f"Bearer {self.token}",
                "content-type": "application/json",
            },
            data=data,
            error_if_not_ok=LootBoxError,
            timeout=timeout,
        )

        payload = response.get("payload")

        if isinstance(payload, str):
            payload = loads(payload)

        if payload:
            return LootBoxResponses.from_dict(payload)

        raise LootBoxError(response.get("message", "Unable to buy crate"))

    def friend_code_to_id(
        self: Self, friend_code: str, timeout: Optional[int] = None
    ) -> str:
        """
        Convert a friend code to a user ID.

        Args:
            friend_code (str): The friend code to be converted to a user ID.
            timeout (int, optional): Timeout for the request in seconds.

        Returns:
            str: The user ID corresponding to the given friend code.

        Raises:
            AuthenticationError: If authentication token is missing or invalid.
            userNotExistError: If the user with the given friend code does not exist or if the request fails.
        """

        if not self.token:
            raise AuthenticationError("Token not found or user is unauthenticated")

        data = '"{\\"friend_code\\":\\"' + friend_code + '\\"}"'
        response = make_request(
            f"{BASE_URL}/rpc/winterpixel_query_user_id_for_friend_code",
            headers={
                **BASE_HEADERS,
                "authorization": f"Bearer {self.token}",
                "content-type": "application/json",
            },
            data=data,
            error_if_not_ok=UnknownUserError,
            timeout=timeout,
        )

        payload = response.get("payload")

        if isinstance(payload, str):
            payload = loads(payload)

        if payload and payload.get("user_id"):
            return payload.get("user_id")

        raise UnknownUserError(response.get("message", "Unable to get user id"))

    @staticmethod
    def signup(
        email: str, password: str, username: str, timeout: Optional[int] = None
    ) -> bool:
        """
        Sign up a new user.

        Args:
            email (str): New account email.
            password (str): New account password.
            username (str): Display name for the new account.
            timeout (int, optional): Timeout for the request in seconds.

        Returns:
            bool: True if signup was successful.

        Raises:
            SignUpError: If signup fails.
        """

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
        make_request(
            f"{BASE_URL}/rpc/winterpixel_signup",
            headers={
                **BASE_HEADERS,
                "authorization": f"Bearer {temp_account.token}",
                "content-type": "application/x-www-form-urlencoded",
            },
            data=data,
            error_if_not_ok=SignUpError,
            timeout=timeout,
        )

        return True

    @staticmethod
    def __custom_account(timeout: Optional[int] = None) -> SignUpResponse:
        data = {
            "id": f"{uuid4()}",
            "vars": {"client_version": CLIENT_VERSION, "platform": "HTML5"},
        }

        response = make_request(
            f"{BASE_URL}/account/authenticate/custom?create=true&",
            headers=BASE_HEADERS,
            json=data,
            error_if_not_ok=AuthenticationError,
            timeout=timeout,
        )

        return SignUpResponse.from_dict(response)
