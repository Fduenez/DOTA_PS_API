import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import Abilities, Hero, Hero_To_Ability

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

dota_hero_abilities_url = "https://raw.githubusercontent.com/odota/dotaconstants/refs/heads/master/build/hero_abilities.json"
dota_abilities_url = "https://raw.githubusercontent.com/odota/dotaconstants/refs/heads/master/build/abilities.json"


def get_hero_abilities():
    response = requests.get(dota_hero_abilities_url)
    response.raise_for_status()
    return response.json()


def get_abilities():
    response = requests.get(dota_abilities_url)
    response.raise_for_status()
    return response.json()


try:
    hero_abilities = get_hero_abilities()
    heroes = session.query(Hero)
    hero_to_ability_list = []
    for hero in heroes:
        h = hero_abilities.get(hero.name)
        abilities = h.get("abilities")

        for ability in abilities:
            if ability == "generic_hidden":
                continue
            abil = session.query(Abilities).filter_by(name=ability).first()
            hero_to_ability_list.append(Hero_To_Ability(
                hero_id=hero.hero_id, ability_id=abil.ability_id
            ))

    session.bulk_save_objects(hero_to_ability_list)

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

except requests.exceptions.RequestException as e:
    print("Error fetching data as ", e)
