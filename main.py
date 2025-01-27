from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from stratzapi import get_stratz_full_purchase, get_stratz_talent
import logging

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/heroes/", response_model=list[schemas.Hero])
async def get_heroes(db: Session = Depends(get_db)):
    heroes = crud.get_heroes(db)
    if heroes is None:
        return HTTPException(status_code=404, detail="Not able to get Heroes")
    return heroes


@app.get("/heroes/{hero_id}", response_model=schemas.Hero)
async def get_hero_by_id(hero_id: int, db: Session = Depends(get_db)):
    hero = crud.get_hero_by_id(db, hero_id)
    if hero is None:
        return HTTPException(status_code=404, detail="Not able to get Hero")
    return hero


@app.get("/heroes/{hero_id}/stats", response_model=schemas.Stats)
async def get_hero_stats_by_id(hero_id: int, db: Session = Depends(get_db)):
    hero_stat = crud.get_hero_stats_by_id(db, hero_id)
    if hero_stat is None:
        return HTTPException(status_code=404, detail="Hero ID does not exist")
    return hero_stat


@app.get("/heroes/{hero_id}/roles", response_model=list[schemas.Roles])
async def get_hero_roles_by_id(hero_id: int, db: Session = Depends(get_db)):
    hero_roles = crud.get_hero_roles_by_id(db, hero_id)
    if hero_roles is None:
        return HTTPException(status_code=404, detail="Hero ID does not exist")
    return hero_roles


@app.get("/heroes/{hero_id}/abilities", response_model=list[schemas.Abilities])
async def get_hero_abilities_by_id(hero_id: int, db: Session = Depends(get_db)):
    hero_abilities = crud.get_hero_abilities_by_id(db, hero_id)
    if hero_abilities is None:
        return HTTPException(status_code=404, detail="Hero ID does not exist")
    return hero_abilities


@app.get("/items/{item_id}", response_model=schemas.Item)
async def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id)
    if item is None:
        return HTTPException(status_code=404, detail="Item id does not exist")
    return item


@app.get("/full-item-purchase/{hero_id}", response_model=schemas.EnrichedFullPurchaseResponse)
async def get_items(hero_id: int, db: Session = Depends(get_db)):
    # call stratz api
    full_purchase = await get_stratz_full_purchase(hero_id)
    full_purchase_data = schemas.FullPurchaseResponse(**full_purchase)
    # enriched items list throughout the game
    enriched_early_game = await process_game_items(full_purchase_data.early_game, db)
    enriched_mid_game = await process_game_items(full_purchase_data.mid_game, db)
    enriched_late_game = await process_game_items(full_purchase_data.late_game, db)

    return schemas.EnrichedFullPurchaseResponse(
        early_game=enriched_early_game,
        mid_game=enriched_mid_game,
        late_game=enriched_late_game
    )


@app.get("/talents/{hero_id}", response_model=List[schemas.TalentResponse])
async def get_talents(hero_id: int, db: Session = Depends(get_db)):
    data = await get_stratz_talent(hero_id)

    # Fetch talent data from the database
    talent_db = crud.get_talents_by_hero_id(hero_id, db)

    if not talent_db:
        raise HTTPException(status_code=404, detail="No Talents found in the database")

    # Map the talents from the database using ability_id as the key
    db_dict = {talent.ability_id: talent for talent in talent_db}

    talents = []

    # Loop through the API data and update or add information
    for talent in data.get('talent', []):
        ability_id = talent['abilityId']
        if ability_id in db_dict:
            db_talent = db_dict[ability_id]
            # Safely compute win_average, check if match_count is 0
            match_count = talent['matchCount']
            win_count = talent['winCount']
            win_average = win_count / match_count if match_count > 0 else 0
            slot = db_talent.slot
            dname = db_talent.d_name

            talents.append(schemas.TalentResponse(ability_id=ability_id,  match_count=match_count, win_count=win_count,
                                                   win_average=win_average, slot=slot, dname=dname))

        else:
            # Logging a message if the ability_id is not found in the database (instead of print)
            print(f"Talent not found in DB: {ability_id}")

    # If no matching talents, raise an error
    if not talents:
        raise HTTPException(status_code=404, detail="No Talents found after API merge")
    talents.sort(reverse=True, key=lambda talent: talent.slot)
    return talents


async def process_game_items(items: List[schemas.ItemStratz], db: Session):
    map = {}
    for item in items:
        if item.itemId in map:
            map[item.itemId].winCount += item.winCount
            map[item.itemId].matchCount += item.matchCount
            map[item.itemId].winsAverage = map[item.itemId].winCount / map[item.itemId].matchCount
        else:
            map[item.itemId] = item
    item_list = []
    for (key, value) in map.items():
        item_list.append(value)
    sorted_items = sorted(item_list, reverse=True, key=lambda item: item.winsAverage)
    top_items = sorted_items[:5]
    return await get_item_details(top_items, db)


async def get_item_details(items: List[schemas.ItemStratz], db: Session = Depends(get_db)):
    if not items:
        return []

    item_ids = [item.itemId for item in items]
    item_details = crud.get_items_by_ids(item_ids, db)

    if not item_details:
        return []

    item_details_dict = {item.id: item for item in item_details}

    enriched_items = []
    for item in items:
        item_detail = item_details_dict.get(item.itemId)
        if item_detail:
            enriched_item = schemas.ItemsResponse(
                id=item_detail.id,
                name=item_detail.name,
                dname=item_detail.dname,
                cost=item_detail.cost,
                behavior=item_detail.behavior,
                qual=item_detail.qual,
                img=item_detail.img,
                notes=item_detail.notes,
                lore=item_detail.lore,
                components=item_detail.components,
                abilities=item_detail.abilities,
                attrib=item_detail.attrib,
                cd=item_detail.cd,
                match_count=item.matchCount,
                win_count=item.winCount,
                wins_average=item.winsAverage
            )
            enriched_items.append(enriched_item)
    logger.debug(f"Enriched items: {enriched_items}")
    return enriched_items
