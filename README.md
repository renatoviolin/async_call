# Async API Call on OpenWeatherMap

This repository implements a simple API to retrieve temperature and humidity from the [OpenWeatherMap](https://openweathermap.org) service.

Before you start this container, you need to get your own API_KEY from OpenWeatherMap. You can get it [here](https://home.openweathermap.org/users/sign_in).


# Services available
| Endpoint | Method | Description
| --- | --- | --- |
| /api/weather | POST | Retrieve the temperature and humidity given the city_id
| /api/status  | GET  | Retrieve the status (# of requests processed)
| /api/test    | GET  | Check if the server is online


# Project Details
This project uses the following packages/frameworks:
- [fastapi](https://fastapi.tiangolo.com): high performance python framework for building APIs.
- [aiohttp](https://docs.aiohttp.org/en/stable/): Asynchronous HTTP Client/Server for asyncio and Python. 
- [sqlalchemy](https://www.sqlalchemy.org): Python SQL toolkit and Object Relational Mapper, used to retrieve/store temporary status of the requests.
- [pytest](https://docs.pytest.org/en/stable/): A framework to help write small tests and perform Test Driven Development (TDD)


### POST: /api/weather
Input

```
{
    "city_id": [2172797, 3442585],
    "uid": "ren123"
}
``` 

Output: 
```
[
  {
    "uid": "ren123",
    "city_id": "2172797",
    "temp": 295.48,
    "humidity": 88.0,
    "ts": "2021-01-30 19:45:28.389619"
  },
  {
    "uid": "ren123",
    "city_id": "3442585",
    "temp": 292.7,
    "humidity": 90.0,
    "ts": "2021-01-30 19:45:32.690209"
  }
]
```

Sample using CURL
```
curl -X POST "http://localhost/api/weather" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"city_id\":[2172797,3442585],\"uid\":\"ren123\"}"
```

### GET: /api/status/\<uid\>
Input
```
uid
``` 

Output: 
```
{
    "requests done": 2
}
```

Sample using CURL
``` 
curl -X GET "http://localhost/api/status/ren123/"
``` 

### GET: /api/test/
Input
``` 
None
```
Output:
```
{
  "status": "online"
}
```


# Install instructions
1. Clone this repository
```
git clone https://github.com/renatoviolin/async_call.git
cd async_call
```

2. Install [docker](https://www.docker.com/get-started). If you already have, create the container with the command:
``` 
docker build -t image01 .
```

3. Run the container with your API_KEY
``` 
docker run -d -e API_KEY="YOUR_API_KEY" --name container01 -p 80:80 image01
```

4. Run the inital test
```
docker exec -it container01 pytest test/test_main.py
```

5. Perform some requests using the integrated Swagger UI.
```
http://localhost/docs
```
<img src=img/img1.jpg>

After the request, the result must be.
<img src=img/img2.jpg>


## Advanced options
- BATCH_SIZE (default=60): indicates how many requests to perform in a given time interval.
- DELAY_BETWEEN_BATCH_REQUEST (default=60): indicates how much time (in seconds) to wait between batch requests.

With default values, if you want to perform 100 requests, you'll have two batchs with 60 and 40 requests, and a delay of 60 seconds between the first batch and the second batch.

Those default values are set avoid get blocked by the free account of OpenWeatherMap.

If you have a payed account, you can set DELAY_BETWEEN_BATCH_REQUEST = 1

The following example start the container setting the batch size = 10 and a delay between batchs of 2 seconds.

```
docker run -d -e API_KEY="YOU_API_KEY" -e BATCH_SIZE="10" -e DELAY_BETWEEN_BATCH_REQUEST="2" --name container01 -p 80:80 image01
``` 
