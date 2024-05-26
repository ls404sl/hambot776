import telebot
import schedule
import time
import threading
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bad_words import bad_words
from admin_names import admin_names

API_TOKEN = '6308303017:AAH0-qKoXmCM__TxzJsEXP5Nt1nGeGBOFzU'
bot = telebot.TeleBot(API_TOKEN, parse_mode='Markdown')

bad_words_responses = [
    "Без мата пожалуйста!"
]

# приветствия новых участников
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    for new_member in message.new_chat_members:
        if new_member.username == "Miraline_M":
            sent_message = bot.send_message(message.chat.id, f"Поздоровайтесь с лапочкой ❤️ - @{new_member.username}!")
        else:
            # разметка с кнопками
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("Советы новичку", url="https://t.me/c/2052489262/1176"),
                InlineKeyboardButton("Зачем нужно Братство", url="https://t.me/c/2052489262/1223"),
                InlineKeyboardButton("Почему листингу быть", url="https://t.me/c/2052489262/1565"),
                InlineKeyboardButton("Дорожная карта", url="https://t.me/c/2052489262/1515"),
                InlineKeyboardButton("Продвижение в соц сетях", url="https://t.me/c/2052489262/1651"),
                InlineKeyboardButton("Гайд по рефералам", url="https://t.me/c/2052489262/4283"),
                InlineKeyboardButton("‼️ Правила общения в чате ‼️", url="https://t.me/c/2052489262/7761")
            )

            # сообщение с приветствием и кнопками
            sent_message = bot.send_message(message.chat.id, f"{new_member.first_name} | "
                                                             f"Добро пожаловать в Братство Хомяков 🤝\n\n",
                                            reply_markup=markup)

        # Удаление приветственного сообщения через 10 минут
        threading.Timer(600, lambda: bot.delete_message(sent_message.chat.id, sent_message.message_id)).start()


# удаления сообщений с матами
@bot.message_handler(func=lambda message: any(bad_word in message.text.lower() for bad_word in bad_words))
def delete_bad_words(message):
    bot.delete_message(message.chat.id, message.message_id)
    response_message = f"{message.from_user.first_name}, {random.choice(bad_words_responses)}"
    sent_message = bot.send_message(message.chat.id, response_message)
    # удаление предупреждающего сообщения через 4 секунды
    threading.Timer(4, lambda: bot.delete_message(sent_message.chat.id, sent_message.message_id)).start()


# удаления сообщений с упоминанием админов
@bot.message_handler(func=lambda message: any(admin_name.lower() in message.text.lower() for admin_name in admin_names))
def delete_admin_mentions(message):
    bot.delete_message(message.chat.id, message.message_id)
    response_message = f"{message.from_user.first_name}, упоминание админов запрещено."
    sent_message = bot.send_message(message.chat.id, response_message)
    # удаление предупреждающего сообщения через 4 секунды
    threading.Timer(4, lambda: bot.delete_message(sent_message.chat.id, sent_message.message_id)).start()


# утренее приветствие
def send_morning_greeting():
    for chat_id in subscribed_chats:
        bot.send_message(chat_id, "Всем доброго утра! Желаю всем хорошего дня, и отличного настроения!")


# планирование утреннего приветствия
def schedule_morning_greeting():
    schedule.every().day.at("06:00").do(send_morning_greeting)

    while True:
        schedule.run_pending()
        time.sleep(1)


bot.remove_webhook()
# запуск планировщика утреннего приветствия в отдельном потоке
threading.Thread(target=schedule_morning_greeting).start()
subscribed_chats = [-1002052489262]

bot.polling(none_stop=True)
