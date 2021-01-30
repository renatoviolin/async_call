import aiohttp
import asyncio
import fastapi
from app.db.database import select, insert, database, clean
from app.models.weather import PayloadIn, Weather
from datetime import datetime
import os


API_KEY = os.getenv('API_KEY', '')
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '60'))
DELAY_BETWEEN_BATCH_REQUEST = int(os.getenv('DELAY_BETWEEN_BATCH_REQUEST', '60'))

URL = 'https://api.openweathermap.org/data/2.5/weather?id={city}&appid={api_key}'
router = fastapi.APIRouter()


@router.on_event("startup")
async def startup():
    await database.connect()


@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def split_batch(data, split_size=BATCH_SIZE):
    tmp = []
    for i in range(0, len(data), split_size):
        tmp.append(data[i:i + split_size])
    return tmp


def decode_response(data):
    try:
        temp = data.get('main', {}).get('temp', '')
        humidity = data.get('main', {}).get('humidity', '')
        city_id = data.get('id')
        w = Weather(city_id=city_id, temp=temp, humidity=humidity, ts=str(datetime.now()))
    except Exception as ex:
        print(ex)
        w = Weather(city_id='', temp=0.0, humidity=0.0, ts=str(datetime.now()))
    return w


async def get_async(payload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=payload['url']) as response:
                resp = await response.json()
                if resp.get('cod', '') == 401:  # API_KEY INVALID
                    return {
                        'error_code': 401,
                        'error_detail': 'INVALID API KEY',
                        'url': payload['url']
                    }
                w = decode_response(resp)
                w.uid = payload['uid']
                _ = await insert(w)
                return w
    except Exception as e:
        return {
            'error_code': 500,
            'error_detail': str(e),
            'url': payload['url']
        }


@router.post('/api/weather')
async def check_weather(payload: PayloadIn):
    await clean(payload.uid)  # clean temp dataset
    all_results = []
    batches = split_batch(payload.city_id)
    n = len(batches)
    for batch_index, batch in enumerate(batches):
        data = []
        for city in batch:
            params = {}
            params['url'] = URL.format(city=city, api_key=API_KEY)
            params['uid'] = payload.uid
            data.append(params)

        calls = [get_async(d) for d in data]
        batch_result = await asyncio.gather(*calls)
        all_results.extend(batch_result)

        # has more than n queries, wait 60 seconds
        if (batch_index + 1) < n:
            _ = await asyncio.sleep(DELAY_BETWEEN_BATCH_REQUEST)

    return all_results


@router.get("/api/status/{uid}/")
async def status(uid: str):
    n = await select(uid)
    return {'requests done': n}


@router.get('/api/test')
async def test():
    return {'status': 'online'}
