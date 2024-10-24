
from fastapi import APIRouter
from app.core.weather import get_location_key, get_current_weather

weather_router = APIRouter()
# в этом файле лежит рутер для получения информации о текущей погоде (задание 1)

@weather_router.get("/weather")
def weather_by_coordinates(latitude: float, longitude: float):
    try:
        location_key = get_location_key(latitude, longitude)
        weather_data = get_current_weather(location_key)[0]

        temperature = weather_data['Temperature']['Metric']['Value']
        humidity = weather_data['RelativeHumidity']
        wind_speed = weather_data['Wind']['Speed']['Metric']['Value']
        precipitation = weather_data['HasPrecipitation']
        rain_probability = "Есть осадки" if precipitation else "Без осадков"

        return {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rain_probability": rain_probability
        }

    except Exception as e:
        return {"error": str(e)}
