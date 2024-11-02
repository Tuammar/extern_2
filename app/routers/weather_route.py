from pydantic import BaseModel
from app import app


class WeatherRequest(BaseModel):
    start_latitude: str
    start_longitude: str
    end_latitude: str
    end_longitude: str
    interval: int


@app.post("/weather_route")
async def weather_route(request: WeatherRequest):
    start_latitude = request.start_latitude
    start_longitude = request.start_longitude
    end_latitude = request.end_latitude
    end_longitude = request.end_longitude
    interval = request.interval

    weather_info = f"Погода от ({start_latitude}, {start_longitude}) до ({end_latitude}, {end_longitude}) на {interval} дней."

    return {"weather_info": weather_info}
