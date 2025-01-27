from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel


class Hero(BaseModel):
    hero_id: int
    name: str
    localized_name: str
    attribute_id: int
    attack_type: str
    img_path: str
    icon_path: str

    class Config:
        from_attributes = True


class Attributes(BaseModel):
    attribute_id: int
    name: str

    class Config:
        from_attributes = True


class HeroesToRole(BaseModel):
    hero_id: int
    role_id: int

    class Config:
        from_attributes = True


class Roles(BaseModel):
    role_id: int
    name: str

    class Config:
        from_attributes = True


class Stats(BaseModel):
    hero_id: int
    base_health: int
    base_health_regen: float
    base_mana: int
    base_mana_regen: float
    base_armor: int
    base_mr: int
    base_attack_min: int
    base_attack_max: int
    base_str: int
    base_agi: int
    base_int: int
    str_gain: float
    agi_gain: float
    int_gain: float
    attack_range: int
    projectile_speed: int
    attack_rate: float
    base_attack_time: int
    attack_point: float
    move_speed: int
    turn_rate: Optional[float]
    cm_enabled: bool
    legs: int
    day_vision: int
    night_vision: int

    class Config:
        from_attributes = True


class Abilities(BaseModel):
    ability_id: int
    name: Optional[str]
    d_name: Optional[str]
    desc: Optional[str]
    dispellable: Optional[bool]
    behavior: Optional[str]
    dmg_type: Optional[str]
    mana_cost: Optional[str]
    cooldown: Optional[str]
    target_team: Optional[str]
    target_type: Optional[str]
    ability_img: Optional[str]
    attributes: List[Dict]
    created_at: datetime

    class Config:
        from_attributes = True


class HeroToAbilities(BaseModel):
    id: int
    ability_id: int
    hero_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Item(BaseModel):
    id: int
    name: str
    dname: str
    cost: int
    behavior: str
    qual: str
    img: str
    notes: str
    lore: str
    abilities: Optional[List[Optional[Dict]]]
    attrib: Optional[List[Optional[Dict]]]
    attrib: Optional[List[Dict]]
    cd: str

    class Config:
        from_attributes = True


class ItemsResponse(BaseModel):
    id: int
    name: str
    dname: str
    cost: int
    behavior: str
    qual: str
    img: str
    notes: str
    lore: str
    components: List[str]
    abilities: List[Dict]
    attrib: List[Dict]
    cd: str
    match_count: int
    win_count: int
    wins_average: float

    class Config:
        from_attributes = True


class ItemStratz(BaseModel):
    itemId: int
    matchCount: int
    winCount: int
    winsAverage: float


class FullPurchaseResponse(BaseModel):
    early_game: List[ItemStratz]
    mid_game: List[ItemStratz]
    late_game: List[ItemStratz]


class EnrichedFullPurchaseResponse(BaseModel):
    early_game: List[ItemsResponse]
    mid_game: List[ItemsResponse]
    late_game: List[ItemsResponse]


class TalentStratz(BaseModel):
    matchCount: int
    winCount: int
    abilityId: int


class TalentResponseStratz(BaseModel):
    talent: List[TalentStratz]


class TalentResponse(BaseModel):
    ability_id: int
    match_count: int
    win_count: int
    win_average: float
    slot: int
    dname: str

