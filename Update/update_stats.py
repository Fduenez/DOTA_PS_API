import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import Abilities, Hero, Hero_Talent, Stats


def get_data(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_attribute_id(attribute: str):
    if attribute == "agi":
        return 1
    elif attribute == "str":
        return 0
    elif attribute == "int":
        return 2
    else:
        return 3


def main():
    load_dotenv()

    DB_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DB_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    dota_hero_url = "https://raw.githubusercontent.com/odota/dotaconstants/refs/heads/master/build/heroes.json"

    try:
        data = get_data(dota_hero_url)
        for id in data:
            hero_id = data[id]['id']
            hero_base_health = data[id]['base_health']
            hero_base_health_regen = data[id]['base_health_regen']
            hero_base_mana = data[id]['base_mana']
            hero_base_mana_regen = data[id]['base_mana_regen']
            hero_base_armor = data[id]['base_armor']
            hero_base_mr = data[id]['base_mr']
            hero_base_attack_min = data[id]['base_attack_min']
            hero_base_attack_max = data[id]['base_attack_max']
            hero_base_str = data[id]['base_str']
            hero_base_agi = data[id]['base_agi']
            hero_base_int = data[id]['base_int']
            hero_str_gain = data[id]['str_gain']
            hero_agi_gain = data[id]['agi_gain']
            hero_int_gain = data[id]['int_gain']
            hero_attack_range = data[id]['attack_range']
            hero_projectile_speed = data[id]['projectile_speed']
            hero_attack_rate = data[id]['attack_rate']
            hero_base_attack_time = data[id]['base_attack_time']
            hero_attack_point = data[id]['attack_point']
            hero_move_speed = data[id]['move_speed']
            hero_turn_rate = data[id]['turn_rate']
            hero_cm_enabled = data[id]['cm_enabled']
            hero_legs = data[id]['legs']
            hero_day_vision = data[id]['day_vision']
            hero_night_vision = data[id]['night_vision']

            hero = session.query(Stats).filter_by(hero_id=hero_id).first()
            if not hero:
                print("not found stats with hero_id: ", hero_id)
                print("preparing stats", {"hero_id": hero_id, "base_health": hero_base_health, "base_health_regen": hero_base_health_regen, "base_mana": hero_base_mana, "base_mana_regen": hero_base_mana_regen })

                new_hero = Stats(
                    hero_id=hero_id,
                base_health=hero_base_health,
                base_health_regen=hero_base_health_regen,
                base_mana=hero_base_mana,
                base_mana_regen=hero_base_mana_regen,
                base_armor=hero_base_armor,
                base_mr=hero_base_mr,
                base_attack_min=hero_base_attack_min,
                base_attack_max=hero_base_attack_max,
                base_str=hero_base_str,
                base_agi=hero_base_agi,
                base_int=hero_base_int,
                str_gain=hero_str_gain,
                agi_gain=hero_agi_gain,
                int_gain=hero_int_gain,
                attack_range=hero_attack_range,
                projectile_speed=hero_projectile_speed,
                attack_rate=hero_attack_rate,
                base_attack_time=hero_base_attack_time,
                attack_point=hero_attack_point,
                move_speed=hero_move_speed,
                turn_rate=hero_turn_rate,
                cm_enabled=hero_cm_enabled,
                legs=hero_legs,
                day_vision=hero_day_vision,
                night_vision=hero_night_vision
                )
                session.add(new_hero)

                print("successfully added stats", hero_id)
            else:
                print("already seen stats", hero_id)
        confirmation = input("Do you want to commit these changes? (yes/no): ").strip().lower()
        if confirmation == "yes":
            try:
                session.commit()
                print("All abilities inserted successfully!")
            except Exception as e:
                session.rollback()  # Rollback in case of any error
                print("Error inserting abilities:", e)
            finally:
                session.close()
        else:
            session.rollback()  # Rollback if the user cancels
            print("Changes have been rolled back.")
    except Exception as e:
        print("Exception", e)


if __name__ == '__main__':
    main()
