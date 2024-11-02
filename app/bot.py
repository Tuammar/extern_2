import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from app.core.weather import get_location_key, get_current_weather
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Логирование
logging.basicConfig(level=logging.INFO)


# Определяем состояния для FSM
class WeatherStates(StatesGroup):
    start_coordinates = State()
    end_coordinates = State()
    forecast_interval = State()


# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот прогноза погоды. Используйте команду /weather для прогноза."
    )


# Команда /help
@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Доступные команды: /start, /help, /weather")


# Команда /weather для запуска алгоритма
@dp.message(Command("weather"))
async def weather(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите начальные координаты в формате 'широта,долгота' (например, 55.7558,37.6173):"
    )
    await state.set_state(WeatherStates.start_coordinates)


# Обработка начальных координат
@dp.message(WeatherStates.start_coordinates)
async def get_start_coordinates(message: types.Message, state: FSMContext):
    try:
        start_lat, start_lon = map(str.strip, message.text.split(","))
        await state.update_data(start_coordinates=(start_lat, start_lon))
        await message.answer(
            "Введите конечные координаты в формате 'широта,долгота' (например, 59.9343,30.3351):"
        )
        await state.set_state(WeatherStates.end_coordinates)
    except ValueError:
        await message.answer("Некорректный формат координат. Попробуйте еще раз.")


# Обработка конечных координат
@dp.message(WeatherStates.end_coordinates)
async def get_end_coordinates(message: types.Message, state: FSMContext):
    try:
        end_lat, end_lon = map(str.strip, message.text.split(","))
        await state.update_data(end_coordinates=(end_lat, end_lon))

        # Показать опции временного интервала прогноза
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Прогноз на 3 дня", callback_data="forecast_3"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Прогноз на 7 дней", callback_data="forecast_7"
                    )
                ],
            ]
        )
        await message.answer(
            "Выберите временной интервал прогноза:", reply_markup=keyboard
        )
        await state.set_state(WeatherStates.forecast_interval)
    except ValueError:
        await message.answer("Некорректный формат координат. Попробуйте еще раз.")


@dp.callback_query(WeatherStates.forecast_interval)
async def send_forecast(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    start_lat, start_lon = data["start_coordinates"]
    end_lat, end_lon = data["end_coordinates"]
    interval = callback_query.data.split("_")[1]

    coordinates = [(start_lat, start_lon), (end_lat, end_lon)]
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
    logging.info(f"{weather_data}")
    forecast = (
        f"Прогноз погоды для маршрута ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})\n"
        f"Начальная точка:\n"
        f"Температура: {weather_data[0]['temperature']}°C\n"
        f"Скорость ветра: {weather_data[0]['wind_speed']} км/ч\n"
        f"Вероятность дождя: {weather_data[0]['rain_probability']}%\n\n"
        f"Конечная точка:\n"
        f"Температура: {weather_data[1]['temperature']}°C\n"
        f"Скорость ветра: {weather_data[1]['wind_speed']} км/ч\n"
        f"Вероятность дождя: {weather_data[1]['rain_probability']}%"
    )

    await bot.send_message(callback_query.from_user.id, forecast)
    await callback_query.answer()

    # Завершить FSM
    await state.clear()


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
