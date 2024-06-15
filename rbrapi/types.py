from json import loads, dumps

from typing import TypedDict, Dict, List


class APIResponse:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return dumps(
            {
                "_": self.__class__.__name__,
                **{
                    attr: (getattr(self, attr))
                    for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                    if getattr(self, attr) is not None
                },
            },
            ensure_ascii=False,
            indent=2,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "APIResponse":
        return cls(**data)


class AuthenticateResponse(APIResponse):
    token: str
    refresh_token: str

    def __init__(self, token: str, refresh_token: str):
        super().__init__(token=token, refresh_token=refresh_token)


class SignUpResponse(APIResponse):
    token: str
    refresh_token: str
    created: bool

    def __init__(self, token: str, refresh_token: str, created: bool):
        super().__init__(token=token, refresh_token=refresh_token, created=created)


class ProgressResponse(TypedDict):
    xp: int
    level: int


class GoalResponse(TypedDict):
    count: int
    goal_id: str
    unlocked_time: int


class UserResponse(TypedDict):
    id: str
    username: str
    display_name: str
    lang_tag: str
    metadata: str
    online: bool
    create_time: str
    update_time: str
    progress: ProgressResponse
    goals: List[GoalResponse]


class Wallet(TypedDict):
    coins: str
    gems: str


class AccountResponse(APIResponse):
    user: UserResponse
    wallet: Wallet
    email: str
    custom_id: str

    def __init__(self, user: UserResponse, wallet: str, email: str, custom_id: str):
        super().__init__(
            user=user, wallet=loads(wallet), email=email, custom_id=custom_id
        )


class LootBoxResponses(APIResponse):
    award_id: str
    is_new: bool

    def __init__(self, award_id: str, is_new: bool):
        super().__init__(award_id=award_id, is_new=is_new)
