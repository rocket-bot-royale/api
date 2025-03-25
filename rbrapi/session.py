from __future__ import annotations

from datetime import UTC, datetime
from threading import local
from typing import Any, Optional

import requests

# Session time-to-live in seconds
SESSION_TIME_TO_LIVE = 600

# Thread-local storage for session and creation time
thread_local = local()


def get_session(*, reset: bool = False) -> requests.sessions.Session:
    """Return or create a requests session, reset if expired."""
    if not hasattr(thread_local, "session") or reset:
        thread_local.session = requests.sessions.Session()
        thread_local.creation_time = datetime.now(tz=UTC)

    if (
        SESSION_TIME_TO_LIVE
        and (datetime.now(tz=UTC) - thread_local.creation_time).total_seconds()
        > SESSION_TIME_TO_LIVE
    ):
        thread_local.session = requests.sessions.Session()
        thread_local.creation_time = datetime.now(tz=UTC)

    return thread_local.session


def make_request(
    url: str,
    headers: Optional[dict[str, str]] = None,
    json: Optional[dict[str, Any]] = None,
    data: Optional[str] = None,
    timeout: Optional[int] = 60,
    method: str = "POST",
    error_if_not_ok: Optional[Exception] = None,
) -> dict[str, Any]:
    session = get_session()

    if method == "POST":
        response = session.post(
            url,
            timeout=timeout,
            headers=headers,
            json=json,
            data=data,
        )
    else:
        response = session.get(
            url,
            timeout=timeout,
            headers=headers,
            json=json,
            data=data,
        )

    if error_if_not_ok and not response.ok:
        raise error_if_not_ok(response.json().get("message", "Unkown"))

    return response.json()
