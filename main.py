import datetime

import requests
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

TOKEN = '6736781787:AAE2WFLSy0Di21l0hC1k0ysQPj9lwOBAKvE'
bot = Bot(TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer(f'Здравствуйте {message.from_user.full_name}. Вас приветствует бот Погода')
    await message.answer('Введите город, в котором хотите узнать погоду')


@dp.message_handler()
async def get_weather(message: Message):
    title = message.text
    params = {
        'appid': '7f72859c08d83f18e4dcfdd744faf091',
        'lang': 'ru',
        'units': 'metric'
    }
    city = title
    params['q'] = city
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params).json()
    try:
        city = data['name']
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        wind = data['wind']['speed']
        timezone = data['timezone']

        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        code_to_smile = {
            'Clear': 'Ясно \U00002600',
            'Clouds': 'Облачно \U00002601',
            'Rain': 'Дождь \U00002614',
            'Thunderstorm': 'Гроза \U000026A1',
            'Snow': 'Снег \U0001F328',
            'Mist': 'Туман \U0001F32B',
        }

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Я не понимаю, что там за погода'

        await message.reply(f'''{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
Погода в городе: {city}
Температура: {temp}°C {wd}
Ветер: {wind} м/с 
Восход солнца: {sunrise}
Закат солнца: {sunset}
Хорошего дня!'''
                        )

    except:
        await message.answer('Я не знаю, что это за город!')

executor.start_polling(dp)
