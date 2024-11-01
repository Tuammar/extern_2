from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.weather import get_location_key, get_current_weather, check_bad_weather
from app.routers.dash_app import init_dash_app
from app import app

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    waypoint_latitude: list[str] = Form([]),
    waypoint_longitude: list[str] = Form([]),
):
    form_data = await request.form()
    waypoint_latitudes = []
    waypoint_longitudes = []

    # Ищем все ключи, начинающиеся с waypoint_latitude_ и waypoint_longitude_
    for key, value in form_data.items():
        if key.startswith("waypoint_latitude_"):
            waypoint_latitudes.append(value)
        elif key.startswith("waypoint_longitude_"):
            waypoint_longitudes.append(value)
    try:
        coordinates = [(start_latitude, start_longitude)]
        coordinates.extend(zip(waypoint_latitudes, waypoint_longitudes))
        coordinates.append((end_latitude, end_longitude))
        # logging.info(coordinates)
        weather_data = []
        for lat, lon in coordinates:
            location_key = get_location_key(lat, lon)
            weather_info = get_current_weather(location_key)[0]

            temperature = weather_info["Temperature"]["Metric"]["Value"]
            wind_speed = weather_info["Wind"]["Speed"]["Metric"]["Value"]
            precipitation = weather_info["HasPrecipitation"]
            rain_probability = 80 if precipitation else 20

            weather_data.append(
                {
                    "temperature": temperature,
                    "wind_speed": wind_speed,
                    "rain_probability": rain_probability,
                }
            )
        logging.info(weather_data)
        init_dash_app(app, weather_data)

        bad_weather_found = any(
            check_bad_weather(
                point["temperature"], point["wind_speed"], point["rain_probability"]
            )
            for point in weather_data
        )
        result = "Ой-ой, погода плохая!" if bad_weather_found else "Погода супер!"

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
