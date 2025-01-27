from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Text, ForeignKey, Integer, Column, Float, Boolean, PrimaryKeyConstraint, TIMESTAMP, DateTime


class Base(DeclarativeBase):
    pass


class Hero(Base):
    __tablename__ = "Dota_PS_Heroes"
    hero_id = Column(Integer, primary_key=True)
    name = Column(Text)
    localized_name = Column(Text)
    attribute_id = Column(Integer)
    attack_type = Column(Text)
    img_path = Column(Text)
    icon_path = Column(Text)


class Attributes(Base):
    __tablename__ = "Dota_PS_Attributes"
    attribute_id = Column(Integer, primary_key=True)
    name = Column(Text)


class HeroesToRole(Base):
    __tablename__ = "Dota_PS_Heroes_To_Roles"
    hero_id = Column(Integer, ForeignKey("Dota_PS_Heroes"), primary_key=True)
    role_id = Column(Integer, ForeignKey("Dota_PS_Roles"), primary_key=True)
    __table_args__ = (
        PrimaryKeyConstraint("hero_id", "role_id"),
    )


class Roles(Base):
    __tablename__ = "Dota_PS_Roles"
    role_id = Column(Integer, primary_key=True)
    name = Column(Text)


class Stats(Base):
    __tablename__ = "Dota_PS_Stats"
    hero_id = Column(Integer, ForeignKey("Dota_PS_Heroes.hero_id"), primary_key=True)
    base_health = Column(Integer)
    base_health_regen = Column(Float)
    base_mana = Column(Integer)
    base_mana_regen = Column(Float)
    base_armor = Column(Integer)
    base_mr = Column(Integer)
    base_attack_min = Column(Integer)
    base_attack_max = Column(Integer)
    base_str = Column(Integer)
    base_agi = Column(Integer)
    base_int = Column(Integer)
    str_gain = Column(Float)
    agi_gain = Column(Float)
    int_gain = Column(Float)
    attack_range = Column(Integer)
    projectile_speed = Column(Integer)
    attack_rate = Column(Float)
    base_attack_time = Column(Integer)
    attack_point = Column(Float)
    move_speed = Column(Integer)
    turn_rate = Column(Float)
    cm_enabled = Column(Boolean)
    legs = Column(Integer)
    day_vision = Column(Integer)
    night_vision = Column(Integer)


class Abilities(Base):
    __tablename__ = 'Dota_PS_Abilities'
    ability_id = Column(Integer, primary_key=True)
    name = Column(Text, default="")
    d_name = Column(Text, default="")
    desc = Column(Text, default="")
    dispellable = Column(Boolean, default=False)
    behavior = Column(Text, default="")
    dmg_type = Column(Text, default="")
    mana_cost = Column(Text, default="")
    cooldown = Column(Text, default="")
    target_team = Column(Text, default="")
    target_type = Column(Text, default="")
    ability_img = Column(Text, default="")
    attributes = Column(JSONB, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class Hero_To_Ability(Base):
    __tablename__ = 'Dota_PS_Hero_To_Ability'
    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('Dota_PS_Heroes'))
    ability_id = Column(Integer, ForeignKey('Dota_PS_Abilities'))
    created_at = Column(DateTime, default=datetime.utcnow)

class Item(Base):
    __tablename__ = 'Dota_PS_Items'
    id = Column(Integer, primary_key=True)
    name = Column(Text, default="")
    dname = Column(Text, default="")
    cost = Column(Integer, default=0)
    behavior = Column(Text, default="")
    qual = Column(Text, default="")
    img = Column(Text, default="")
    notes = Column(Text, default="")
    lore = Column(Text, default="")
    components = Column(JSONB, default=[])
    abilities = Column(JSONB, default=[])
    attrib = Column(JSONB, default=[])
    cd = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Hero_Talent(Base):
    __tablename__ = 'Dota_PS_Hero_Talent'
    hero_id = Column(Integer, ForeignKey('Dota_PS_Heroes'), primary_key=True)
    ability_id = Column(Integer, ForeignKey('Dota_PS_Abilities'), primary_key=True)
    slot = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

