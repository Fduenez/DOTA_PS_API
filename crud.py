from sqlalchemy.orm import Session

import models


def get_heroes(db: Session):
    return db.query(models.Hero).all()


def get_hero_by_id(db: Session, hero_id: int):
    return db.query(models.Hero).filter(models.Hero.hero_id == hero_id).first()


def get_hero_stats_by_id(db: Session, hero_id: int):
    return db.query(models.Stats).filter(models.Stats.hero_id == hero_id).first()


def get_hero_roles_by_id(db: Session, hero_id: int):
    return db.query(models.Roles).join(models.HeroesToRole).filter(models.HeroesToRole.hero_id == hero_id).all()


def get_hero_abilities_by_id(db: Session, hero_id: int):
    return db.query(models.Abilities).join(models.Hero_To_Ability).filter(
        models.Hero_To_Ability.hero_id == hero_id).all()


def get_item_by_id(item_id: int, db: Session):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items_by_ids(item_ids: list[int], db: Session):
    return db.query(models.Item).filter(models.Item.id.in_(item_ids)).all()


def get_talents_by_hero_id(hero_id: int, db: Session):
    return db.query(models.Hero_Talent.hero_id, models.Hero_Talent.ability_id, models.Abilities.d_name, models.Hero_Talent.slot).join(models.Abilities).filter(models.Hero_Talent.hero_id == hero_id).all()
