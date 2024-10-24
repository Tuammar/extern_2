from fastapi import APIRouter
from app.core.weather import get_location_key, get_current_weather, check_bad_weather

check_weather_router = APIRouter()
# в этом файле лежит рутер для проверки качества погоды (задание 2)
@check_weather_router.get("/check_weather")
def check_weather_by_coordinates(latitude: float, longitude: float):
    try:
        location_key = get_location_key(latitude, longitude)
        weather_data = get_current_weather(location_key)[0]

        temperature = weather_data['Temperature']['Metric']['Value']
        humidity = weather_data['RelativeHumidity']
        wind_speed = weather_data['Wind']['Speed']['Metric']['Value']
        precipitation = weather_data['HasPrecipitation']
        rain_probability = 80 if precipitation else 20

        bad_weather = check_bad_weather(temperature, wind_speed, rain_probability)

        return {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rain_probability": rain_probability,
            "bad_weather": bad_weather
        }

    except Exception as e:
        return {"error": str(e)}
