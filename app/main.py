from fastapi import FastAPI, Query
from app.routers.weather import weather_router
from app.routers.check_weather import check_weather_router
from app.routers.form import form_router
from app.routers.dash_app import init_dash_app
from app import app

# подключаем рутеры (они же ручки)
app.include_router(weather_router)
app.include_router(check_weather_router)
app.include_router(form_router)
