import telebot
import wb_parser


#Токен бота
token = 'YOUR TOKEN'
 
#Инициализируем бота
bot = telebot.TeleBot(token)

#Функция для обработки взаимодействий с пользователем
@bot.message_handler(content_types=['text'])
def handle_text(message):
    #Разбиваем сообщение на слова
    word_list = message.text.split()
    #При вводе определенных команд возвращаем нужное сообщение
    if word_list[0] == '/start' or word_list[0] == '/help':
        answer = f'Для справочной информации используйте команду /help.\n\nПривет! Я бот, который найдет где в поиске находится товар на площадке wildberries. Инструкция к применению:\n\nВведите /search [Поисковый запрос] [Артикул]'
        bot.send_message(message.from_user.id, answer)
    #Если нужно найти позицию товара, то делаем это
    elif word_list[0] == '/search':
        if len(word_list) >= 2 and word_list[-1].isdigit():
            query = ' '.join(word_list[1:-1])
            id = int(word_list[-1])
            answer = wb_parser.find_product_position(query, id)
        else:
            answer = 'Некорректный запрос'
        bot.send_message(message.from_user.id, answer)
            
#Поставим бота в режим постоянной обработки информации, приходящей от серверов telegram.
bot.polling(none_stop=True, interval=0)