import telebot
import constants
from wit import Wit
client = Wit('C6RBEQMC3A7BCNCN4BSJCCLNYGMVFL2F')
from pydub import AudioSegment
bot = telebot.TeleBot(constants.token)

# -*- coding: utf-8 -*-


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Инструкции и советы', 'Прогресс', 'Настройки')
    bot.send_message(message.from_user.id, 'Добро пожаловать! MultiCode speech bot поможет вам улучшить вашу речь! Избавиться от слов паразитов и многое другое.. Для начало попробуйте сказать несколько предложений зажимая кнопку микрофона в правом нижнем угле.', reply_markup = user_markup )


def log(message, answer):
    from datetime import datetime
    print(datetime.now())
    print("смс от [0] [1]. (id = [2]) \n Текст - [3]".format(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.text) )

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.reply_to(message, "Yes voice")
    AudioSegment.from_ogg("voice.ogg").export("voice.mp3", format="mp3")

'''    with open('test.wav', 'rb') as f:
      resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
    print('Yay, got Wit.ai response: ' + str(resp))
    client.speech(f, None, {'Content-Type': 'audio/mpeg3'})
    AudioSegment.from_ogg("voice.ogg").export("voice.mp3", format="mp3")
    '''


@bot.message_handler(content_types=["text"])
def handle_text(message):
    answer = "Выберите команду"
    if message.text == "Инструкции":
        instruction = u"1) Нажимите и зажимайте кнопку микрофона в правом нижнем краю и произнесите свою речь. После \n 2) В смайликах будут укзазаны слова паразиты над которыми следует паработать и маты в случае присутствие. Помните маты очень сильно занижают вашу оценку и плохо влияет на общую статистику. \n 3) Итого вы получите: \n 1. ваш текст \n2. Рекомендуемый текст \n3. Синонимы для слов паразитов"
        log(message, instruction)
        bot.send_message(message.chat.id, instruction)
    else:
        bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)
