#Импорт библиотек
import telebot
from currency import Currency

#Токен бота
token = 'YOUR TOKEN'
 
#Инициализируем бота
bot = telebot.TeleBot(token)
#Инициализируем объект класса Currency
currency = Currency('YOUR API KEY')

#Функция для обработки взаимодействий с пользователем
@bot.message_handler(content_types=['text'])
def handle_text(message):
    #Разбиваем сообщение на слова
    word_list = message.text.split()
    #При вводе определенных команд возвращаем нужное сообщение
    if word_list[0] == '/start' or word_list[0] == '/help':
        answer = f'Для справочной информации используйте команду /help.\n\nПривет! Я бот, который подскажет тебе курс рубля к указанной валюте, чтобы получить курс введи команду:\n\n/rate [названия валюты]\n\nВот список доступных валют:\n {currency.currency_list}'
        bot.send_message(message.from_user.id, answer)
    #Если нужно вывести курс валюты, то делаем это
    elif word_list[0] == '/rate':
        if len(word_list) == 2:
            answer = currency.get_currency_rate(word_list[1])
        else:
            answer = 'Некорректный запрос'
        bot.send_message(message.from_user.id, answer)
            
#Поставим бота в режим постоянной обработки информации, приходящей от серверов telegram.
bot.polling(none_stop=True, interval=0)