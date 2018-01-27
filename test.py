import telebot
import constants

bot = telebot.TeleBot(constants.token)

#bot.send_message(303852308, "testt")
print(bot.get_me())

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Инструкции и советы', 'Прогресс', 'Настройки')
    bot.send_message(message.from_user.id, 'Добро пожаловать! MultiCode speech bot поможет вам улучшить вашу речь! Избавиться от слов паразитов и многое другое.. Для начало попробуйте сказать несколько предложений зажимая кнопку микрофона в правом нижнем угле.', reply_markup = user_markup )


def log(message, answer):
    from datetime import datetime
    print(datetime.now())
    print("смс от [0] [1]. (id = [2]) \n Текст - [3]".format(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.text) )


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.from_user.id, 'text has come')
      
@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    pass

#bot.polling(none_stop=True, interval=0)

