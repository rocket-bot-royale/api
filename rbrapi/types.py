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


class Goal(TypedDict):
    goal_id: str
    unlocked_time: int
    count: int


class UserStats(
    TypedDict(
        "UserStats",
        {"5_kills": int, "triple-shots_used": int, "kills_using_triple-shot": int},
    ),
):
    top_5: int
    deaths: int
    assists: int
    snipers: int
    bot_kills: int
    games_won: int
    yardsales: int
    dunk_tanks: int
    flaks_used: int
    mines_used: int
    nukes_used: int
    squads_won: int
    two_birdss: int
    coins_found: int
    drills_used: int
    total_kills: int
    double_kills: int
    first_bloods: int
    games_played: int
    homings_used: int
    player_kills: int
    poisons_used: int
    shields_used: int
    triple_kills: int
    grenades_used: int
    meters_driven: float
    squads_played: int
    missiles_fired: int
    beachball_shots: int
    whirlwinds_used: int
    crates_collected: int
    kills_using_flak: int
    kills_using_mine: int
    kills_using_nuke: int
    most_total_kills: int
    blocks_using_proj: int
    most_player_kills: int
    kills_using_homing: int
    kills_using_poison: int
    kills_using_shield: int
    longest_killstreak: int
    blocks_using_shield: int
    kills_using_grenade: int


class UserProgress(TypedDict):
    xp: int
    level: int


class UserMetadata(TypedDict):
    friend_code: str
    is_guest: bool

    skin: str
    badge: str
    trail: str
    parachute: str

    last_coins: int
    last_points: int
    timed_bonus_last_collect: int
    results_rewarded_video_last_collect: int

    progress: UserProgress
    awards_seen: int
    goals: list[Goal]
    stats: UserStats


class UserResponse(TypedDict):
    id: str
    username: str
    display_name: str
    lang_tag: str
    metadata: UserMetadata
    online: bool
    create_time: str
    update_time: str
    progress: ProgressResponse
    goals: list[GoalResponse]


class Wallet(TypedDict):
    coins: int
    gems: int


class AccountResponse(APIResponse):
    user: UserResponse
    wallet: Wallet
    email: str
    devices: list[dict[str, str]]

    def __init__(
        self: Self,
        *,
        user: UserResponse,
        wallet: str,
        email: str,
        devices: list[dict[str, str]],
    ) -> None:
        user["metadata"] = loads(user["metadata"])
        super().__init__(user=user, wallet=loads(wallet), email=email, devices=devices)


class LootBoxResponses(APIResponse):
    award_id: str
    is_new: bool

    def __init__(self, award_id: str, is_new: bool):
        super().__init__(award_id=award_id, is_new=is_new)
