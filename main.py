from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests
import datetime
import math

# Вставьте свой токен Telegram и API-ключ OpenWeatherMap
API_TOKEN = '7200818259:AAF5awjKWxsQ3ufyc8wR2zQh10FHFCLat7I'
WEATHER_API_KEY = 'bf06273965b66c9e43cc95c529333ddb'

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который показывает погоду. Введите название города.")

# Обработчик текстовых сообщений
@dp.message_handler()
async def get_weather(message: types.Message):
    city = message.text
    weather_data = fetch_weather(city)
    if weather_data:
        response = format_weather_response(weather_data)
    else:
        response = "Не удалось найти информацию о погоде. Проверьте название города."
    await message.reply(response)

# Функция для получения данных о погоде
def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Функция для форматирования ответа
def format_weather_response(data):
    city = data["name"]
    cur_temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    weather_desc = data['weather'][0]['description']
    # получаем время рассвета и преобразуем его в читабельный формат
    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    # то же самое проделаем со временем заката
    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    # продолжительность дня
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    return (f"Погода в {city}:\n"
            f"Температура: {cur_temp}°C\n"
            f"Описание: {weather_desc}\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {math.ceil(pressure/1.333)} мм.рт.ст.\n"
            f"Скорость ветра: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp}\n"
            f"Закат солнца: {sunset_timestamp}\n"
            f"Продолжительность дня: {length_of_the_day}\n"
            f"Хорошего дня!")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)