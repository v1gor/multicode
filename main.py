# coding: utf8
# -*- coding: utf-8 -*-
import telebot
import constants
import requests
import json
from pydub import AudioSegment
from time import sleep
import os
import os.path
from ffmpy import FFmpeg
import glob
from collections import Counter

bot = telebot.TeleBot(constants.token)
url = 'https://api.telegram.org/bot476953241:AAGXc_V2lmO0NRvi4-ixaMbw1iCzNo41yh8/getUpdates'
API_ENDPOINT = 'https://api.wit.ai/speech'

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

def read_audio(WAVE_FILENAME):
    # function to read audio(wav) file
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.from_user.id, 'text has come')
      
@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    
    data = requests.get(url, None)
    if data:
        data = data.text
        json_data = json.loads(data)

        if not json_data['result']:
            bot.send_message(message.from_user.id, 'Resend the message please')
            
        else:
            bot.send_message(message.from_user.id, 'Wait please')
            file_idwka = json_data['result'][0]['message']['voice']['file_id']
            file_path_urlq = 'https://api.telegram.org/bot476953241:AAGXc_V2lmO0NRvi4-ixaMbw1iCzNo41yh8/getFile?file_id=' + file_idwka
            data1 = requests.get(file_path_urlq).text
            json_data1 = json.loads(data1)
            file_pathwka = json_data1['result']['file_path']

            print("downloading")
            url_file = 'https://api.telegram.org/file/bot476953241:AAGXc_V2lmO0NRvi4-ixaMbw1iCzNo41yh8/' + file_pathwka
            requests.get(url_file)

            
            g = requests.get(url_file, stream=True)
            voice_filename = "voice.mp3"
            
            with open(voice_filename, "wb") as o:
                  o.write(g.content)

            
            
            #song = AudioSegment.from_mp3("C:/Users/ьоио/Desktop/jaimai/voice.mp3")
            #song.export("out.ogg", format="ogg")  # Is the same as:
            #song.export("out.ogg", format="ogg", codec="libvorbis")
            #AudioSegment.from_ogg("voice.mp3").export("voice.mp3", format="mp3")
            
            AudioSegment.from_file(voice_filename, "ogg").export(voice_filename, format="mp3")
            #resp = client.speech(open(voice_filename, 'rb'), None, {'Content-Type': 'audio/mpeg3'})

            audio = read_audio(voice_filename)
            headers = {'authorization': 'Bearer ' + 'C6RBEQMC3A7BCNCN4BSJCCLNYGMVFL2F','Content-Type': 'audio/mpeg3'}
            resp = requests.post(API_ENDPOINT, headers = headers, data = audio)
            respon = json.loads(resp.content)
            user_output = respon['_text']
            bot.send_message(message.from_user.id, user_output)

            user_words = user_output.split()

            for item in range (0,int(len(user_words))):
                user_words[item] = user_words[item].lower()

            freq_words = []
            
            counter1 = Counter(user_words)
            for key, value in counter1.items():
                if value >=3:
                    freq_words.append(key)
                    
            if freq_words:
                bot.send_message(message.from_user.id, 'Вы слишком часто используете следующие слова :\n')
                for item in freq_words:
                    bot.send_message(message.from_user.id, item)

            #------------------------------------------------#
            with open('przt.txt', 'r') as f:
                parazits = f.readlines()
            arr = []
            prz_detected = []
            for i in range (0,int(len(parazits))):
                arr.append(parazits[i].strip())
            
            for word in user_words:
                for przt in arr:
                    if word == przt:
                       prz_detected.append(word)
            nodup_prz = Counter(prz_detected)
            bot.send_message(message.from_user.id,'Ваши слова паразиты: '+ nodup_prz.keys())
                        
                    
            

            
                
            
            
            



bot.polling(none_stop=True, interval=0)
    

