import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import Abilities, Item

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

dota_items_url = "https://raw.githubusercontent.com/odota/dotaconstants/refs/heads/master/build/items.json"


def get_items():
    response = requests.get(dota_items_url)
    response.raise_for_status()
    return response.json()


try:

    items = get_items()

    for item in items:
        item_details = items.get(item);
        id = item_details.get("id")
        name = item
        dname = item_details.get("dname", "")
        cost = item_details.get("cost", 0)
        behavior = item_details.get("behavior", "")
        qual = item_details.get("qual", "")
        img = item_details.get("img", "")
        notes = item_details.get("notes", "")
        lore = item_details.get("lore", "")
        components = item_details.get("components", [])
        abilities = item_details.get("abilities", [])
        attrib = item_details.get("attrib", [])
        cd = item_details.get("cd", "")

        if isinstance(behavior, list):
            behavior = ",".join(str(x) for x in behavior)
        if isinstance(behavior, bool):
            behavior = ""
        if isinstance(cd, bool):
            cd = "0"
        if abilities is None:
            abilities = []
        if attrib is None:
            attrib = []
        if components is None:
            components = []

        new_item = Item(id=id, name=name, dname=dname, cost=cost, behavior=behavior, qual=qual, img=img, notes=notes,
                        lore=lore, components=components, abilities=abilities, attrib=attrib, cd=cd)
        session.add(new_item)
    print("New objects:")
    for obj in session.new:
        print(obj.id, obj.name, obj.dname, obj.cost, obj.behavior, obj.qual, obj.img, obj.notes, obj.lore, obj.components, obj.abilities, obj.attrib, obj.cd)
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
