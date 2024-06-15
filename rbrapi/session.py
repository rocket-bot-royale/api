import requests
from threading import local
from datetime import datetime

from typing import Optional, Dict, Any


# Session time-to-live in seconds
SESSION_TIME_TO_LIVE = 600

# Thread-local storage for session and creation time
thread_local = local()


def get_session(reset=False):
    """Return or create a requests session, reset if expired."""
    if not hasattr(thread_local, "session") or reset:
        thread_local.session = requests.sessions.Session()
        thread_local.creation_time = datetime.now()

    if (
        SESSION_TIME_TO_LIVE
        and (datetime.now() - thread_local.creation_time).total_seconds()
        > SESSION_TIME_TO_LIVE
    ):
        thread_local.session = requests.sessions.Session()
        thread_local.creation_time = datetime.now()

    return thread_local.session


def make_request(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, Any]] = None,
    data: Optional[str] = None,
    timeout: int = 60,
    method: str = "POST",
    error_if_not_ok: Optional[Exception] = None,
) -> Dict[str, Any]:
    session = get_session()

    if method == "POST":
        response = session.post(
            url, timeout=timeout, headers=headers, json=json, data=data
        )
    else:
        response = session.get(
            url, timeout=timeout, headers=headers, json=json, data=data
        )

    if error_if_not_ok:
        if not response.ok:
            raise error_if_not_ok(response.json().get("message", "Unkown"))

    return response.json()
