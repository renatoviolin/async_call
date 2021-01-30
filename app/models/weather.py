from pydantic import BaseModel


class PayloadIn(BaseModel):
    city_id: list
    uid: str


class Weather(BaseModel):
    uid: str = ''
    city_id: str
    temp: float
    humidity: float
    ts: str
