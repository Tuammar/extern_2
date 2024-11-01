from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.weather import get_location_key, get_current_weather, check_bad_weather
from app.routers.dash_app import init_dash_app
from app import app

"""Здесь лежит рутер для задания 3. Пользователь вводит координаты начальной и конечной точки маршрута и получает ответ"""

templates = Jinja2Templates(directory="app/templates")

form_router = APIRouter()


@form_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@form_router.post("/", response_class=HTMLResponse)
async def submit_weather(
        request: Request,
        start_latitude: str = Form(...),
        start_longitude: str = Form(...),
        end_latitude: str = Form(...),
        end_longitude: str = Form(...),
):
    try:
        if (
                not start_latitude
                or not start_longitude
                or not end_latitude
                or not end_longitude
        ):
            raise ValueError("Все координаты обязательны для ввода")

        # Получаем погоду для начальной точки
        start_location_key = get_location_key(start_latitude, start_longitude)
        start_weather_data = get_current_weather(start_location_key)[0]

        # Получаем погоду для конечной точки
        end_location_key = get_location_key(end_latitude, end_longitude)
        end_weather_data = get_current_weather(end_location_key)[0]

        # Обрабатываем данные для начальной точки
        start_temperature = start_weather_data["Temperature"]["Metric"]["Value"]
        start_wind_speed = start_weather_data["Wind"]["Speed"]["Metric"]["Value"]
        start_precipitation = start_weather_data["HasPrecipitation"]
        start_rain_probability = 80 if start_precipitation else 20

        # Обрабатываем данные для конечной точки
        end_temperature = end_weather_data["Temperature"]["Metric"]["Value"]
        end_wind_speed = end_weather_data["Wind"]["Speed"]["Metric"]["Value"]
        end_precipitation = end_weather_data["HasPrecipitation"]
        end_rain_probability = 80 if end_precipitation else 20
        init_dash_app(
            app,
            start_temperature,
            start_wind_speed,
            start_rain_probability,
            end_temperature,
            end_wind_speed,
            end_rain_probability,
        )
        # Проверяем условия для начальной и конечной точки
        if check_bad_weather(
                start_temperature, start_wind_speed, start_rain_probability
        ) or check_bad_weather(end_temperature, end_wind_speed, end_rain_probability):
            result = "Ой-ой, погода плохая!"
        else:
            result = "Погода супер!"

        return templates.TemplateResponse(
            "form.html", {"request": request, "result": result}
        )

    except ValueError as e:
        return templates.TemplateResponse(
            "form.html", {"request": request, "result": f"Ошибка: {str(e)}"}
        )
    except HTTPException as e:
        return templates.TemplateResponse(
            "form.html", {"request": request, "result": f"Ошибка: {e.detail}"}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "form.html",
            {"request": request, "result": f"Непредвиденная ошибка: {str(e)}"},
        )
