import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram import types
import requests
from asgiref.sync import sync_to_async

from handlers.users.eng import insta_download_eng, handle_tiktok_video_eng, get_message_eng
from handlers.users.rus import insta_download_rus, handle_tiktok_video_rus, get_message_rus
from handlers.users.tiktok import handle_tiktok_video
from handlers.users.youtube import get_message
from keyboards.inline.add_group import get_inline_keyboard
from loader import bot, dp
from telesave.models import Users

# Ensure directories exist
os.makedirs('instagram', exist_ok=True)
os.makedirs('youtube', exist_ok=True)
os.makedirs('tiktok', exist_ok=True)

keyboard = get_inline_keyboard()

headers = {
    "x-rapidapi-key": "3e98ed8ce1msh1a05c8a7aede75ap1ccdb6jsn2f6f17651931",
    "x-rapidapi-host": "social-media-video-downloader.p.rapidapi.com"
}
Api_url = "https://social-media-video-downloader.p.rapidapi.com/smvd/get/all"


# Handler for handling Instagram post URLs
@dp.message_handler(Text(startswith=['https://']))
async def handle_url(message: types.Message):
    user_id = message.from_user.id
    user = await sync_to_async(Users.objects.get)(telegram_id=user_id)
    url = message.text
    if "instagram.com" in url:
        if user.language == 'uzb':
            await insta_download(message, url)
        elif user.language == 'eng':
            await insta_download_eng(message, url)
        elif user.language == 'rus':
            await insta_download_rus(message, url)
    elif "tiktok.com" in url:
        if user.language == 'uzb':
            await handle_tiktok_video(message, url)
        elif user.language == 'eng':
            await handle_tiktok_video_eng(message, url)
        elif user.language == 'rus':
            await handle_tiktok_video_rus(message, url)
    elif 'youtube.com' in url or 'youtu.be' in url:
        if user.language == 'uzb':
            await get_message(message)
        elif user.language == 'eng':
            await get_message_eng(message)
        elif user.language == 'rus':
            await get_message_rus(message)
        # await state.set_state(YoutubeState.send_image)
        # Implement YouTube content download handling
        pass
    else:
        await message.reply("Video linki topilmadi")


async def insta_download(message, url):
    waiting_message = await bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")
    try:
        response = requests.get(Api_url, headers=headers, params={"url": url})

        if response.status_code == 200:

            data = response.json()

            video_url = None
            audio_url = None

            for link in data['links']:
                if 'video' in link['quality']:
                    video_url = link['link']
                elif 'audio' in link['quality']:
                    audio_url = link['link']

            if video_url:
                try:
                    await bot.send_video(chat_id=message.chat.id, video=video_url,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
                except Exception as e:
                    await bot.send_message(message.chat.id, f"Video topilmadi:")

            if audio_url:
                try:
                    await bot.send_audio(chat_id=message.chat.id, audio=audio_url,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
                except Exception as e:
                    await bot.send_message(message.chat.id, f"Audio tapilmadi")

            await bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

            if not video_url and not audio_url:
                await bot.send_message(chat_id=message.chat.id, text="Kechirasiz, hech narsa topilmadi.")
        else:
            await bot.send_message(message.chat.id, f"Xatolik yuz berdi: API javob kodlari {response.status_code}.")
    except requests.exceptions.RequestException as e:
        await bot.send_message(message.chat.id, f"Xatolik yuz berdi: HTTP talabi muvaffaqiyatsiz {e}")
