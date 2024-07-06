import os

import django
from aiogram import types
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
django.setup()
from telesave.models import Users

from keyboards.inline.lang import lang
from loader import dp


@dp.message_handler(commands=['lang'])
async def language(message: types.Message):
    await message.answer("Tilni tanlang", reply_markup=lang)


@dp.callback_query_handler(text=['eng', 'uzb', 'rus'])
async def eng_callback(query: types.CallbackQuery):
    user_id = str(query.from_user.id)

    # Wrap the database call with sync_to_async
    try:
        user = await sync_to_async(Users.objects.get)(telegram_id=user_id)

        user.language = query.data
        await sync_to_async(user.save)()

        if query.data == 'eng':
            await query.message.answer("Update your language")
            await query.message.answer("""
            Hi I am Tele Save Bot

✅ Get to know my features:

📥 From Instagram - Download video and music

📥 From TikTok - Download video and music 

📥 From YouTube - Download videos and music

Send me the video link""")

        elif query.data == 'uzb':
            await query.message.answer("Til ozgartirildi")
            await query.message.answer("""
            Salom Men Tele Save Bot

✅ Mening xususiyatlarim bilan tanishing:

📥 Instagramdan - Video va audio yuklash

📥 TikTokdan - Video va audio yuklash

📥 YouTubedan - Video va audio yuklash

Video linkini yuboring""")

        elif query.data == 'rus':
            await query.message.answer("Обновил ваш язык")
            await query.message.answer("""
            Привет, Я Tele Save Bot

✅ Познакомьтесь с моими возможностями:

📥 Из Instagram - Скачать видео и музыку

📥 Из TikTok - Скачать видео и музыку

📥 Из YouTube – скачивайте видео и музыку

Отправьте мне ссылку на видео""")

    except Users.DoesNotExist:
        # Handle case where user is not found
        await query.message.answer("User not found.")
