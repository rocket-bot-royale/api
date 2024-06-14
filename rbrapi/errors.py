class AuthenticationError(Exception):
    """
    Exception raised for errors in the authentication process.
    """

    pass


class SignUpError(Exception):
    """
    Exception raised for errors during the sign-up process.
    """

    pass


class CollectTimedBonusError(Exception):
    """
    Exception raised for errors in collecting the timed bonus.
    """

    pass


class FriendRequestError(Exception):
    """
    Exception raised for errors in sending a friend request.
    """

    pass


class LootBoxError(Exception):
    """
    Exception raised for errors in purchasing a loot box.
    """

    pass
