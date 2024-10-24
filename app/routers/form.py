
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.weather import get_location_key, get_current_weather, check_bad_weather

templates = Jinja2Templates(directory="app/templates")

form_router = APIRouter()
# в этом файле лежат рутер для проверки качества погоды (задание 2)

@form_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@form_router.post("/", response_class=HTMLResponse)
async def submit_weather(request: Request, latitude: str = Form(...), longitude: str = Form(...)):
    try:
        if not latitude or not longitude:
            raise ValueError("Широта и долгота обязательны для ввода")

        location_key = get_location_key(latitude, longitude)
        weather_data = get_current_weather(location_key)[0]

        temperature = weather_data['Temperature']['Metric']['Value']
        wind_speed = weather_data['Wind']['Speed']['Metric']['Value']
        precipitation = weather_data['HasPrecipitation']
        rain_probability = 80 if precipitation else 20

        if check_bad_weather(temperature, wind_speed, rain_probability):
            result = "Ой-ой, погода плохая!"
        else:
            result = "Погода супер!"

        return templates.TemplateResponse("form.html", {"request": request, "result": result})

    except ValueError as e:
        return templates.TemplateResponse("form.html", {"request": request, "result": f"Ошибка: {str(e)}"})
    except HTTPException as e:
        return templates.TemplateResponse("form.html", {"request": request, "result": f"Ошибка: {e.detail}"})
    except Exception as e:
        return templates.TemplateResponse("form.html", {"request": request, "result": f"Ошибка: {str(e)}"})
