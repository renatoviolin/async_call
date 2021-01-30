import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from starlette.testclient import TestClient

from app.main import app
from app.db import database
from app.models.weather import Weather, PayloadIn

client = TestClient(app)


def test_server_on():
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}


@pytest.mark.asyncio
async def test_insert_db():
    w = Weather(uid='123', city_id='aaa', temp=1.0, humidity=2.0, ts='12:00:00')
    res = await database.insert(w)
    assert res > 0


@pytest.mark.asyncio
async def test_select_db():
    res = await database.select(uid='123')
    assert res >= 1


@pytest.mark.asyncio
async def test_clean_db():
    _ = await database.clean(uid='123')
    res = await database.select(uid='123')
    assert res == 0


def test_invalid_city():
    payload = {"city_id": [12172797], "uid": "123"}
    res = client.post("/api/weather", json=payload)
    assert res.json()[0].get('city_id', 'none') == ''


def test_valid_city():
    payload = {"city_id": [2172797], "uid": "123"}
    res = client.post("/api/weather", json=payload)
    assert res.json()[0].get('city_id', 'none') == '2172797'
