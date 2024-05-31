import telebot
import speech_recognition as sr
from pydub import AudioSegment
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

recognizer = sr.Recognizer()

ffmpeg_path = "C:\ffmpeg-7.0.1-essentials_build\ffmpeg-7.0.1-essentials_build\bin\ffmpeg.exe"


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:

        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        with open('voice.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)

        audio = AudioSegment.from_ogg('voice.ogg')
        audio.export('voice.wav', format='wav')

        with sr.AudioFile('voice.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ru-RU')

        bot.reply_to(message, text)

        os.remove('voice.ogg')
        os.remove('voice.wav')

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")


bot.polling()
