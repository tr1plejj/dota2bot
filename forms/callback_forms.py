from aiogram.filters.callback_data import CallbackData


class PlayerIdCallback(CallbackData, prefix='proplayer'):
    player_name: str
    player_id: str
    action: str


class HeroIdCallback(CallbackData, prefix='hero'):
    hero_name: str
    action: str


class MatchIdCallback(CallbackData, prefix='match'):
    match_id: str
    action: str


class MetaPosCallback(CallbackData, prefix='meta'):
    pos_id: str
    action: str
