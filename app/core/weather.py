import requests
import os
from dotenv import load_dotenv
from fastapi import HTTPException

"""Здесь мы инициализируем функции обращения к Accuweather API,
через которые мы будем получать интересующую  нас информацию"""

load_dotenv()

API_KEY = os.getenv("ACCUWEATHER_API_KEY")


def get_location_key(latitude: float, longitude: float) -> str:
    try:
        if not -90 <= float(latitude) <= 90 or not -180 <= float(longitude) <= 180:
            raise ValueError(
                "Некорректные координаты. Широта должна быть между -90 и 90, долгота должна быть между -180 и 180"
            )

        url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_KEY}&q={latitude},{longitude}&language=ru"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Key" not in data:
            raise ValueError("Ключ локации не найден. Проверьте введенные координаты")
        return data["Key"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail="Ошибка подключения к API погоды. Превышено количество запросов в день",
        ) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_current_weather(location_key: str):
    try:
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&language=ru&details=true"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail="Ошибка подключения к API погоды. Превышено количество запросов в день",
        ) from e


def check_bad_weather(temperature: int, wind_speed: int, rain_probability: int) -> bool:
    if temperature < 0 or temperature > 35:
        return True
    if wind_speed > 50:
        return True
    if rain_probability > 70:
        return True
    return False
