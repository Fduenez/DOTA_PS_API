import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import Abilities

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
    data_abilties = get_abilities()

    for hero in hero_abilities:
        for ability in hero_abilities[hero]["abilities"]:
            def update_abiltiy_details(curr_ability, abilities):
                data = abilities.get(curr_ability)
                print(data)

                if data:

                    abil = session.query(Abilities).filter_by(d_name=data.get("dname")).first()

                    mana_cost_value = data.get("mc", "0")
                    cd_value = data.get("cd", "0")
                    behavior_value = data.get("behavior", None)
                    target_team_value = data.get("target_team", None)
                    target_type_value = data.get("target_type", None)

                    print(curr_ability)

                    if isinstance(mana_cost_value, list):
                        mana_cost_value = ",".join(str(x) for x in mana_cost_value)
                    if isinstance(cd_value, list):
                        cd_value = ",".join(str(x) for x in cd_value)
                    if(isinstance(behavior_value, list)):
                        behavior_value = ",".join(str(x) for x in behavior_value)
                    if(isinstance(target_team_value, list)):
                        target_team_value = ",".join(str(x) for x in target_team_value)
                    if (isinstance(target_type_value, list)):
                        target_type_value = ",".join(str(x) for x in target_type_value)

                    abil.name=curr_ability,
                    abil.d_name=data.get("dname"),
                    abil.desc=data.get("desc"),
                    abil.dispellable=True if data.get("dispellable") == "Yes" else False,
                    abil.behavior=behavior_value,
                    abil.dmg_type=data.get("dmg_type"),
                    abil.mana_cost=mana_cost_value,
                    abil.cooldown=cd_value,
                    abil.target_team=target_team_value,
                    abil.target_type=target_type_value,
                    abil.ability_img=data.get("img", None),
                    abil.attributes=data.get("attrib", None)
            update_abiltiy_details(ability, data_abilties)

    print("Preview of new abilities to be added:")
    for new_ability in session.new:
        print(new_ability)

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
