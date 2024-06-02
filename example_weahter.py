import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("#")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Введите город:")


@bot.message_handler(func=lambda message: True)
def get_city(message):
    city = message.text
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    button_today = types.KeyboardButton(text="Сегодня")
    button_tomorrow = types.KeyboardButton(text="Завтра")
    button_week = types.KeyboardButton(text="Неделя")
    keyboard.add(button_today, button_tomorrow, button_week)

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_weather, city)


def get_weather(message, city):
    option = message.text.lower()
    if option == "сегодня":
        weather_data = parse_weather(city, "сегодня")
    elif option == "завтра":
        weather_data = parse_weather(city, "завтра")
    elif option == "неделя":
        weather_data = parse_weather(city, "неделя")
    else:
        bot.send_message(message.chat.id, "Неправильная команда. Попробуйте снова.")
        return

    bot.reply_to(message, weather_data)


def parse_weather(city, day):
    print(day)
    url = f"https://meteolabs.org/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_{city}/{day}/"

    # Используем библиотеку Requests и bs4
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if day == 'сегодня' or day == 'завтра':
        try:
            obbr = soup.find('p', class_='icon-calendar heading_date').text
        except:
            return 'Введите название города...'
        name = soup.find('h1', class_='h1').text
        temp = soup.find_all('div', class_='wthSBlock wthSBlock_list')
        try:
            all_par = obbr + '\n' + name + '\n' + temp[0].text.strip() + '\n' + temp[1].text.strip()
            return all_par
        except:
            return 'Введите название города...'
    else:
        head = soup.find('h1', class_='h1').text.strip()
        opy = soup.find('div', class_='block block_margin').find_all('p')
        total = head + '\n' + opy[0].text.strip() + '\n' + opy[1].text.strip() + '\n' + opy[2].text.strip() + '\n' + opy[
            3].text.strip() + '\n' + opy[4].text.strip() + '\n' + opy[5].text.strip() + '\n' + opy[
                    6].text.strip()
        return total


bot.polling(none_stop=True)
