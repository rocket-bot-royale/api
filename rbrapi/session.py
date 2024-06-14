import requests
import threading
from datetime import datetime

# Define session time-to-live in seconds
SESSION_TIME_TO_LIVE = 600

# Thread-local storage for session and creation time
thread_local = threading.local()


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
    headers=None,
    json=None,
    timeout: int = 60,
    method="POST",
    fn=None,
    data=None,
) -> dict:
    """Make a request using the session."""
    session = get_session()

    if method == "POST":
        response = session.post(
            url, timeout=timeout, headers=headers, json=json, data=data
        )
    else:
        response = session.get(
            url, timeout=timeout, headers=headers, json=json, data=data
        )

    if fn:
        fn(response)

    return response.json()
