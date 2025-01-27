import os

from dotenv import load_dotenv
from fastapi import HTTPException
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from schemas import TalentResponseStratz

# load environment variables
load_dotenv()


async def get_stratz_full_purchase(hero_id: int):
    # Http Transport
    transport = RequestsHTTPTransport(
        url="https://api.stratz.com/graphql",  # Replace with the actual GraphQL endpoint
        headers={
            "User-Agent": "STRATZ_API",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['STRATZ_TOKEN']}"
        },
        use_json=True
    )

    # Init Client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
    query($hero_id: Short!){
    heroStats {
    early_game: itemFullPurchase(heroId: $hero_id,minTime:1 maxTime:15){
      matchCount
      winCount
      winsAverage
     itemId
    }
    mid_game: itemFullPurchase(heroId: $hero_id, minTime:16, maxTime: 30){
      matchCount
      winCount
      winsAverage
     itemId
    }
    late_game: itemFullPurchase(heroId: $hero_id, minTime:31){
      matchCount
      winCount
      winsAverage
     itemId
    }
  }
  }
    """)

    # headers dynamic variables
    variables = {"hero_id": hero_id}

    try:
        # await the response
        response = client.execute(query, variable_values=variables)
        # Check if the response contains the expected data
        if 'heroStats' not in response:
            raise HTTPException(status_code=500, detail="GraphQL query failed to return valid data")
        return response['heroStats']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling GraphQL API: {str(e)}")


async def get_stratz_talent(hero_id: int) -> TalentResponseStratz:
    # Http Transport
    transport = RequestsHTTPTransport(
        url="https://api.stratz.com/graphql",  # Replace with the actual GraphQL endpoint
        headers={
            "User-Agent": "STRATZ_API",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['STRATZ_TOKEN']}"
        },
        use_json=True
    )

    # Init Client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
       query ($hero_id: Short!){
       heroStats {
        talent(heroId:$hero_id) {
          matchCount
          winCount
          abilityId
        }
       }
     }
       """)

    # headers dynamic variables
    variables = {"hero_id": hero_id}

    try:
        # await the response
        response = client.execute(query, variable_values=variables)
        # Check if the response contains the expected data
        if 'heroStats' not in response:
            raise HTTPException(status_code=500, detail="GraphQL query failed to return valid data")
        return response['heroStats']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling GraphQL API: {str(e)}")


async def get_stratz_abilities():
    # Http Transport
    transport = RequestsHTTPTransport(
        url="https://api.stratz.com/graphql",  # Replace with the actual GraphQL endpoint
        headers={
            "User-Agent": "STRATZ_API",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['STRATZ_TOKEN']}"
        },
        use_json=True
    )

    # Init Client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
query{
  constants{
    abilities{
      id
      name
	  isTalent
      uri
      language {
        displayName
        lore
        aghanimDescription
        shardDescription
      }
	}
  }
} """)

    try:
        # await the response
        response = client.execute(query)
        # Check if the response contains the expected data
        if 'constants' not in response:
            raise HTTPException(status_code=500, detail="GraphQL query failed to return valid data")
        return response['constants']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling GraphQL API: {str(e)}")
