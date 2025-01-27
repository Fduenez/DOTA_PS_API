import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import Abilities, Hero, Hero_Talent, Stats, HeroesToRole, Roles


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
        new_hero_to_roles = []
        for id in data:
            hero_id = data[id]['id']
            roles = data[id]['roles']

            hero_to_role = session.query(HeroesToRole).filter_by(hero_id=hero_id).first()
            if not hero_to_role:
                print("not found roles with hero_id: ", hero_id)
                for role in roles:
                    role_db = session.query(Roles).filter_by(name=role).first()
                    if role_db:
                        new_hero_to_roles.append(HeroesToRole(hero_id=hero_id, role_id=role_db.role_id))
            else:
                print("already found roles with hero_id: ", hero_id)
        session.bulk_save_objects(new_hero_to_roles)
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
