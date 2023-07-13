import os
import speech_recognition as sr

from aiogram import Bot, Dispatcher, executor, types
from loguru import logger
from pydub import AudioSegment

from constants import ARROW_DOWN, SAD_FACE, photos_menu, voices_menu, hobby, repo_link

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привет!\nЯ бот для тестового задания наставника kids ai.\nПосмотреть команды - "
                        f"/commands\nГолосовые команды - /voice_commands\nФото автора{ARROW_DOWN * 3}",
                        reply_markup=photos_menu)


@dp.message_handler(commands=['commands'])
async def get_commands(message: types.Message):
    await message.answer("/voice - голосовое сообщение\n/hobby - небольшой пост о главном увлечении\n/link - ссылка "
                         "на репозиторий с исходным кодом\n/next_step: your_text - команда по заданию (обратите "
                         "внимание на двоеточие)")


@dp.message_handler(commands=['voice_commands'])
async def get_voice_commands(message: types.Message):
    await message.answer("В голосовом сообщении вы можете сказать любую фразу на английском, содержащую одно из "
                         "ключевых слов:\nvoice - голосовое сообщение\npost - небольшой пост о главном "
                         "увлечении\nlink - ссылка на репозиторий с исходным кодом\nnext step (your_text_in_english) "
                         "- команда по заданию\nselfie - последнее селфи\nschool - фото из старшей школы\nGPT - "
                         "рассказ о GPT для бабушки\ndifference - SQL vs NoSQL\nlove - история первой "
                         "любви.\nЖелательно использовать контекст.")


@dp.callback_query_handler(text="selfie")
async def send_selfie(query: types.CallbackQuery):
    photo = types.InputFile('images/last_selfie.jpg')
    await query.message.answer_photo(photo, reply_markup=photos_menu)


@dp.callback_query_handler(text="school")
async def send_school_photo(query: types.CallbackQuery):
    photo = types.InputFile('images/school_photo.jpg')
    await query.message.answer_photo(photo, reply_markup=photos_menu)


@dp.message_handler(commands=['voice'])
async def send_voice(message: types.Message):
    await message.reply("Выберите тему голосового сообщения:", reply_markup=voices_menu)


@dp.callback_query_handler(text="gpt")
async def send_gpt_voice(query: types.CallbackQuery):
    voice = types.InputFile('voices/gpt.m4a')
    await query.message.reply_voice(voice, caption='Про GPT для бабушки')


@dp.callback_query_handler(text="sql")
async def send_sql_voice(query: types.CallbackQuery):
    voice = types.InputFile('voices/sql_vs_nosql.m4a')
    await query.message.reply_voice(voice, caption="Разница между SQL и NoSQL")


@dp.callback_query_handler(text="love")
async def send_love_voice(query: types.CallbackQuery):
    voice = types.InputFile('voices/first_love.m4a')
    await query.message.reply_voice(voice, caption="История первой любви")


@dp.message_handler(content_types=[types.ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    voice = await message.voice.get_file()
    oga_file = await bot.download_file(file_path=voice.file_path)
    track = AudioSegment.from_file(oga_file, format='ogg')
    file = track.export(format='wav')
    r = sr.Recognizer()
    file = sr.AudioFile(file)
    try:
        with file as source:
            audio = r.record(source)
            command = r.recognize_google(audio)
            if not command:
                return
            command = command.lower()
            if "voice" in command:
                await send_voice(message)
                return
            if "post" in command:
                await send_hobby(message)
                return
            if "next step" in command:
                message.text = command
                await next_step(message)
                return
            if "link" in command:
                await send_link_to_repo(message)
                return
            else:
                q = types.CallbackQuery()
                q.message = message
                if "selfie" in command:
                    await send_selfie(q)
                    return
                if "school" in command:
                    await send_school_photo(q)
                    return
                if "gpt" in command:
                    await send_gpt_voice(q)
                    return
                if "difference" in command:
                    await send_sql_voice(q)
                    return
                if "love" in command:
                    await send_love_voice(q)
                    return
    except Exception as e:
        logger.info(e)
        await message.answer("Попробуйте сказать фразу более чётко. Используйте слово в контексте.")
        return
    await message.answer(f"Такой команды нет{SAD_FACE}. Используйте /voice_commands")


@dp.message_handler(commands=['hobby'])
async def send_hobby(message: types.Message):
    await message.reply(hobby)


@dp.message_handler(commands=['next_step:'])
async def next_step(message: types.Message):
    logger.info(message.text)
    await message.reply("Ваше сообщение успешно доставлено.")


@dp.message_handler(commands=['link'])
async def send_link_to_repo(message: types.Message):
    await message.answer(repo_link)


@dp.message_handler()
async def info(message: types.Message):
    await message.answer(f"Такой команды нет{SAD_FACE}. Используйте /commands")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
