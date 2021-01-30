import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import FastAPI
from app.api import weather

app = FastAPI()
app.include_router(weather.router)
