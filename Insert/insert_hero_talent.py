import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import Abilities, Hero, Hero_Talent


def get_data(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()

    DB_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DB_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    dota_hero_abilities_url = "https://raw.githubusercontent.com/odota/dotaconstants/refs/heads/master/build/hero_abilities.json"

    try:
        data = get_data(dota_hero_abilities_url)
        hero_talent_list = []
        if not data:
            return "No hero abilities found"
        for hero in data:
            hero_abilities = data.get(hero)
            curr_hero = session.query(Hero).filter_by(name=hero).first()
            talents = data[hero].get("talents")
            slot = 0
            for talent in talents:
                print(talent['name'])
                curr_ability = session.query(Abilities).filter_by(name=talent['name']).first()
                if curr_ability:
                    new_hero_talent = Hero_Talent(hero_id=curr_hero.hero_id, ability_id=curr_ability.ability_id, slot=slot)
                    hero_talent_list.append(new_hero_talent)
                slot += 1

        session.bulk_save_objects(hero_talent_list)

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


if __name__ == "__main__":
    main()
