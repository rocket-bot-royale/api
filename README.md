# Unofficial Client for RocketBotRoyale Game API

**⚠️️ For Educational Use Only!**

This is an unofficial Python client for the Rocket Bot Royale game API. It allows users to interact with the game API, including authenticating, retrieving account details, collecting timed bonuses, sending friend requests, and purchasing crates.

## Installation

Install the package using pip:

```
pip install -U rbrapi
```

## Usage

### Initialization

Initialize a `RocketBotRoyale` instance with an email and password:

```python
from rbrapi import RocketBotRoyale
from rbrapi.errors import AuthenticationError

# Initialize with email and password
client = RocketBotRoyale(email="email@example.com", password="your_password")
```

### Authentication

Authenticate with the RocketBotRoyale API using provided credentials:

> **Note:** It auto-authenticates when `RocketBotRoyale` is initialized. Use this only for regenerating the session token.

```python
try:
    client.authenticate()
    print("Authentication successful!")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

### Account Details

Retrieve account details:

```python
try:
    account_details = client.account()
    print(f"Account ID: {account_details.custom_id}")
    print(f"Username: {account_details.user["username"]}")
    print(f"Gems: {account_details.wallet["gems"]}")
    print(f"Coins: {account_details.wallet["coins"]}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

### Collect Timed Bonus

Collect a timed bonus:

```python
from rbrapi.errors import CollectTimedBonusError

try:
    success = client.collect_timed_bonus()
    if success:
        print("Timed bonus collected successfully!")
    else:
        print("Failed to collect timed bonus.")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except CollectTimedBonusError as e:
    print(f"Failed to collect timed bonus: {e}")
```

### Send Friend Request

Send a friend request to another user:

```python
from rbrapi.errors import FriendRequestError

friend_code = "your_friend_code"

try:
    success = client.send_friend_request(friend_code)
    if success:
        print("Friend request sent successfully!")
    else:
        print("Failed to send friend request.")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except FriendRequestError as e:
    print(f"Failed to send friend request: {e}")
```

### Purchase Crate

Purchase a crate (regular or elite):

```python
from rbrapi.errors import LootBoxError

try:
    crate_details = client.buy_crate(elite=False)  # Set elite=True for elite crate
    print("Crate purchased successfully!")
    print(f"Crate details: {crate_details}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except LootBoxError as e:
    print(f"Failed to purchase crate: {e}")
```

### Sign Up New User

Make a new account with the RocketBotRoyale API:

```python
from rbrapi.errors import SignUpError

email = "new_user@example.com"
password = "new_password"
username = "new_username"

try:
    success = RocketBotRoyale.signup(email, password, username)
    if success:
        print(f"User {username} signed up successfully!")
    else:
        print("Failed to sign up user.")
except SignUpError as e:
    print(f"Failed to sign up user: {e}")
```
