import asyncio
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi import Depends, FastAPI, HTTPException

from src.api.redis_local import write_match_data_to_redis
from src.db.crud import get_match_stats_by_id
from src.db.connection import Connection

app = FastAPI()


@app.get("/stats/{match_id}")
async def get_stats(match_id: int):
    async with Connection.getConnection() as session:
            odds = get_match_stats_by_id(session, match_id)
    if not odds:
        raise HTTPException(status_code=404, detail="Stats not found")
    return odds

@app.post("/set_limits/")
async def set_limits(
    match_id: int,
    first_odd: tuple(float, float),
    second_odd: tuple(float, float),
    draw_odd: tuple(float, float),
    first_handicap: tuple(float, float),
    second_handicap: tuple(float, float),
):
    match_data = {
        "first_odd": {"minn": first_odd[0], "maxx": first_odd[1]},
        "second_odd": {"minn": second_odd[0], "maxx": second_odd[1]},
        "draw_odd": {"minn": draw_odd[0], "maxx": draw_odd[1]},
        "first_handicap": {"minn": first_handicap[0], "maxx": first_handicap[1]},
        "second_handicap": {"minn": second_handicap[0], "maxx": second_handicap[1]}
    }
    status = write_match_data_to_redis(
         match_id=match_id,
         match_data=match_data,
         expiry_seconds=10
    )
    return status
