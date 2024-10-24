from fastapi import FastAPI
from app.routers.weather import weather_router
from app.routers.check_weather import check_weather_router
from app.routers.form import form_router


app = FastAPI()

# подключаем рутеры (они же ручки)
app.include_router(weather_router)
app.include_router(check_weather_router)
app.include_router(form_router)
