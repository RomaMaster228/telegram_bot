from aiogram import types

ARROW_DOWN = u"\u2193"
SAD_FACE = u"\U0001F614"

photos_menu = types.InlineKeyboardMarkup(row_width=1)
selfie_button = types.InlineKeyboardButton(text='Последнее селфи', callback_data="selfie")
school_button = types.InlineKeyboardButton(text='Фото из старшей школы', callback_data="school")
photos_menu.add(selfie_button, school_button)

voices_menu = types.InlineKeyboardMarkup(row_width=1)
gpt_button = types.InlineKeyboardButton(text='Про GPT для бабушки', callback_data="gpt")
love_button = types.InlineKeyboardButton(text='История первой любви', callback_data="love")
sql_button = types.InlineKeyboardButton(text='Разница между SQL и NoSQL', callback_data="sql")
voices_menu.add(gpt_button, love_button, sql_button)

hobby = "Плавание - это моё главное увлечение, которое приносит мне радость, а также физическую выгоду. Плавание - " \
        "это не только спорт, но и искусство. Каждое движение в воде требует точности и грации, чтобы достичь " \
        "максимальной эффективности. В воде я чувствую себя легким и свободным, забывая о стрессе и напряжении. Это " \
        "время, когда я могу насладиться моментом и полностью отдохнуть."

repo_link = "https://github.com/RomaMaster228/telegram_bot"
