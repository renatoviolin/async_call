import sqlalchemy
import databases
from app.models.weather import Weather
import os

DATABASE_URL = "sqlite:///./temp_db.db"

try:
    database = databases.Database(DATABASE_URL)
    metadata = sqlalchemy.MetaData()
    engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    db_weather = sqlalchemy.Table(
        "weather",
        metadata,
        sqlalchemy.Column("uid", sqlalchemy.String),
        sqlalchemy.Column("city_id", sqlalchemy.String),
        sqlalchemy.Column("temp", sqlalchemy.Float),
        sqlalchemy.Column("humidity", sqlalchemy.Float),
        sqlalchemy.Column("ts", sqlalchemy.String),
    )
    metadata.create_all(engine)
except:
    print('Database already created... skiping')


async def insert(weather: Weather):
    query = db_weather.insert().values(uid=weather.uid, city_id=weather.city_id, temp=weather.temp, humidity=weather.humidity)
    last_record_id = await database.execute(query)
    return last_record_id


async def select(uid: str):
    query = db_weather.select().where(uid == db_weather.c.uid)
    return len(await database.fetch_all(query))


async def clean(uid: str):
    query = db_weather.delete().where(uid == db_weather.c.uid)
    return await database.execute(query)
