import telebot
import requests
import json

bot = telebot.TeleBot('#')
API = '#'


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, я бот погоды! Напиши название города...')


@bot.message_handler(content_types=['text'])
def get_weahter(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru')
    # print(res.json())
    data = (res.json())
    oblachnost = data['weather'][0]['description']
    temp = data['main']['temp']
    davleniye = data['main']['pressure']
    veter = data['wind']['speed']
    city_name = data['name']
    bot.reply_to(message, f'Сейчас в {city_name}:  {oblachnost}\n Температура:  {temp}\n Давление:  {davleniye} мм/рт.ст\n Скорость ветра:  {veter} м/с')


bot.polling(none_stop=True)
