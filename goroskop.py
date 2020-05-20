import random
import telebot
import random
import requests
from lxml import etree
import lxml.html
from telebot import types

# Место для API токена телеграм бота
TOKEN = ""
bot = telebot.TeleBot(TOKEN)

# Выполняется при старте 
@bot.message_handler(commands=['start'])
def welcome(message):
	# Отслеживание того, кто включил бот
	name = message.from_user.username
	fir = message.from_user.first_name
	id = message.from_user.id
	# Вывод этих данных в консоль 
	print("\nSTART\n\n" + "User ID: " + str(id) + "\nFirst name: " + fir + "\nUsername: " + str(name) + "\n")

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Создаём клавиатуру
	btn = types.KeyboardButton("🔮 Получить гороскоп 🔮") # Создаем кнопку
	markup.add(btn) # Добавляем кнопку в клавиатуру
	# Приветствие
	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!".format(message.from_user, bot.get_me()),
	    parse_mode='html', reply_markup=markup)
 


@bot.message_handler(content_types=['text'])
def Inline_keyboard(message): 
	if message.chat.type == 'private':
		if message.text == '🔮 Получить гороскоп 🔮': 
			markup = types.InlineKeyboardMarkup(row_width=1) # Создаём инлайн клавиатуру
			# Создаём кнопки для инлайн клавиатуры 
			item1 = types.InlineKeyboardButton("Овен ♈", callback_data='aries')
			item2 = types.InlineKeyboardButton("Телец ♉", callback_data='taurus')
			item3 = types.InlineKeyboardButton("Близнецы ♊", callback_data='gemini')
			item4 = types.InlineKeyboardButton("Рак ♋", callback_data='cancer')
			item5 = types.InlineKeyboardButton("Лев ♌", callback_data='lion')
			item6 = types.InlineKeyboardButton("Дева ♍", callback_data='virgo')
			item7 = types.InlineKeyboardButton("Весы ♎", callback_data='libra')
			item8 = types.InlineKeyboardButton("Скорпион ♏", callback_data='scorpio')
			item9 = types.InlineKeyboardButton("Стрелец ♐", callback_data='sagittarius')
			item10 = types.InlineKeyboardButton("Козерог ♑", callback_data='capricorn')
			item11 = types.InlineKeyboardButton("Водолей ♒", callback_data='aquarius')
			item12 = types.InlineKeyboardButton("Рыбы ♓", callback_data='pisces')
			# Наполняем клавиатуру кнопками
			markup.add(item1, item2, item3,item4,item5,item6,item7,item8,item9,item10,item11,item12)
			# Передаём инлайн клавиатуру в это сообщение
			bot.send_message(message.chat.id, 'Кто вы по гороскопу?', reply_markup=markup)

		else:
			bot.send_message(message.chat.id, 'Пожалуйста, используйте только кнопки')


@bot.callback_query_handler(func=lambda call: True)
def goroskop(call):	
	try:
		if call.message:
			# Отслеживание выбраного знака зодиака
			# И в зависимости от выбора даётся нужная ссылка на страничку сайта с нужным знаком зодиака
			if call.data == "aries":
				url = "https://orakul.com/horoscope/astrologic/general/aries/today.html"
			elif call.data == "taurus":
				url = "https://orakul.com/horoscope/astrologic/general/taurus/today.html"
			elif call.data == "gemini":
				url = "https://orakul.com/horoscope/astrologic/general/gemini/today.html"
			elif call.data == "cancer":
				url = "https://orakul.com/horoscope/astrologic/general/cancer/today.html"
			elif call.data == "lion":
				url = "https://orakul.com/horoscope/astrologic/general/lion/today.html"
			elif call.data == "virgo":
				url = "https://orakul.com/horoscope/astrologic/general/virgo/today.html"
			elif call.data == "libra":
				url = "https://orakul.com/horoscope/astrologic/general/libra/today.html"
			elif call.data == "scorpio":
				url = "https://orakul.com/horoscope/astrologic/general/scorpio/today.html"
			elif call.data == "sagittarius":
				url = "https://orakul.com/horoscope/astrologic/general/sagittarius/today.html"
			elif call.data == "capricorn":
				url = "https://orakul.com/horoscope/astrologic/general/capricorn/today.html"
			elif call.data == "aquarius":
				url = "https://orakul.com/horoscope/astrologic/general/aquarius/today.html"
			elif call.data == "pisces":
				url = "https://orakul.com/horoscope/astrologic/general/pisces/today.html"

			api = requests.get(url) # Переход по ссылке
			tree = lxml.html.document_fromstring(api.text) # Забыл что это делает, но без него не работает
			text = tree.xpath('///*[@id="content"]/div[1]/div[1]/div[1]/div[2]/div[4]/p[1]/text()') # Берём текст из этого элемента
			text = str(text[0]) # Превращаем список в строку. Это текст гороскопа
			bot.send_message(call.message.chat.id, text) # Печатаем текст гороскопа юзверю
			print(text) # Ну и себе выводим. Ведь нужно же следить за тем, кто что делает
			# P.S. Можно было бы сделать так, что бы в терминале выводило не только, что кому-то пришло, а ещё и юзверя, которому это пришло
			# Но будет выводить данные бота, а не юзверя. Может это Я что-то не так сделал
			
	# Отслеживаем ошибки
	except Exception as e:
	    print(repr(e))


# Запуск
bot.polling(none_stop=True)
