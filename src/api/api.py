from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from src.db.connection import Connection
from src.db.crud import get_match_statistics_by_match_id

app = FastAPI()

# TODO: сделать модели pydantic
# GET запрос для получения записей с заданным match_id из таблицы Odd
@app.get("/stats/{match_id}")
async def get_stats(
     match_id: int
):
    async with Connection.getConnection() as session:
            stats = get_match_statistics_by_match_id(
                session=session, 
                match_id=match_id
                )
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    return stats


# POST запрос для создания новых записей в таблице Odd
@app.post("/odd_limits/")
async def post_odd_limits(
    match_id: int,
    first_odd: float, 
    second_odd: float, 
    draw_odd: float,
    first_handicap: str, 
    second_handicap: str
):

    return new_odd
