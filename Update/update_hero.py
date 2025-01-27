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
            hero_name = data[id]['name']
            hero_localized = data[id]['localized_name']
            hero_attribute_id = get_attribute_id(data[id]['primary_attr'])
            hero_attack_type = data[id]['attack_type']
            hero_img_path = data[id]['img']
            hero_icon_path = data[id]['icon']
            hero = session.query(Hero).filter_by(hero_id=hero_id).first()
            if not hero:
                print("not found hero", hero_id)
                print("preparing hero", {"hero_id": hero_id, "name": hero_name, "localized_name": hero_localized, "attribute_id": hero_attribute_id, "attack_type": hero_attack_type, "img_path": hero_img_path, "icon_path": hero_icon_path})

                new_hero = Hero(
                    hero_id=hero_id,
                    name=hero_name,
                    localized_name=hero_localized,
                    attribute_id=hero_attribute_id,
                    attack_type=hero_attack_type,
                    img_path=hero_img_path,
                    icon_path=hero_icon_path
                )
                session.add(new_hero)

                print("successfully added hero", hero_id)
            else:
                print("already seen hero", hero_id)
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
