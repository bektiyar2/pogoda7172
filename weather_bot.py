import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# Замените на свои ключи
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Функция для запроса погоды
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return (f"\U0001F321 Погода в {city.capitalize()}:\n"
                f"{weather_desc}\n"
                f"🌡 Температура: {temp}°C\n"
                f"🌬 Ветер: {wind_speed} м/с\n"
                f"💧 Влажность: {humidity}%\n"
                f"❄ Ощущается как: {feels_like}°C")
    else:
        return "⚠ Город не найден. Попробуйте ещё раз."

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.reply("Привет! Напиши название города, чтобы узнать погоду ☀")

# Обработчик сообщений с названием города
@dp.message_handler()
async def send_weather(message: Message):
    city = message.text.strip()
    weather_info = get_weather(city)
    await message.reply(weather_info)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
