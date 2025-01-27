import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import Abilities
import asyncio
from stratzapi import get_stratz_abilities


async def main():
    load_dotenv()

    DB_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DB_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    dota_hero_abilities_url = "https://raw.githubusercontent.com/odota/dotaconstants/refs/heads/master/build/hero_abilities.json"
    dota_abilities_url = "https://raw.githubusercontent.com/odota/dotaconstants/refs/heads/master/build/abilities.json"

    try:

        data = await get_stratz_abilities()
        abilities = data['abilities']
        talent = []

        for ability in abilities:
            print(ability)
            if ability['isTalent']:
                id = ability.get('id')
                abilityDB = session.query(Abilities).filter_by(ability_id=id).first()
                if not abilityDB:
                    name = ability.get('name')
                    language = ability.get('language')
                    dname = language.get('displayName')
                    mana_cost_value = ability.get("mc", "0")
                    cd_value = ability.get("cd", "0")
                    behavior_value = ability.get("behavior", "")
                    target_team_value = ability.get("target_team", "")
                    target_type_value = ability.get("target_type", "")
                    attrib = ability.get("attrib", [])
                    dmg_type_value = ability.get("dmg_type", "")

                    if isinstance(mana_cost_value, list):
                        mana_cost_value = ",".join(str(x) for x in mana_cost_value)
                    if isinstance(cd_value, list):
                        cd_value = ",".join(str(x) for x in cd_value)
                    if (isinstance(behavior_value, list)):
                        behavior_value = ",".join(str(x) for x in behavior_value)
                    if (isinstance(target_team_value, list)):
                        target_team_value = ",".join(str(x) for x in target_team_value)
                    if (isinstance(target_type_value, list)):
                        target_type_value = ",".join(str(x) for x in target_type_value)
                    if (isinstance(dmg_type_value, list)):
                        dmg_type_value = ",".join(str(x) for x in dmg_type_value)
                    if not attrib:
                        attrib = []  # Set to NULL if attrib is empty or invalid

                    new_ability = Abilities(
                        ability_id=id,
                        name=name,
                        d_name=dname,
                        desc=ability.get("desc", ""),
                        dispellable=True if ability.get("dispellable", False) == "Yes" else False,
                        behavior=behavior_value,
                        dmg_type=dmg_type_value,
                        mana_cost=mana_cost_value,
                        cooldown=cd_value,
                        target_team=target_team_value,
                        target_type=target_type_value,
                        ability_img=ability.get("img", ""),
                        attributes=attrib
                    )
                    talent.append(new_ability)
        session.bulk_save_objects(talent)

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

asyncio.run(main())