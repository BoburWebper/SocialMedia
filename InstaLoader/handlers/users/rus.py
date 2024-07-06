import os

import pytube
from aiogram import types

import requests

from loader import bot, dp

headers = {
    "x-rapidapi-key": "3e98ed8ce1msh1a05c8a7aede75ap1ccdb6jsn2f6f17651931",
    "x-rapidapi-host": "social-media-video-downloader.p.rapidapi.com"
}
Api_url = "https://social-media-video-downloader.p.rapidapi.com/smvd/get/all"


async def insta_download_rus(message, url):
    waiting_message = await bot.send_message(message.chat.id, "⏳ Загрузка...")
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
                                         caption="Скачано через @insta_tik_tokSaverbot 📥")
                except Exception as e:
                    await bot.send_message(message.chat.id, f"Видео не найдено")

            if audio_url:
                try:
                    await bot.send_audio(chat_id=message.chat.id, audio=audio_url,
                                         caption="Скачано через @insta_tik_tokSaverbot 📥")
                except Exception as e:
                    await bot.send_message(message.chat.id, f"Звук не найден")

            await bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

            if not video_url and not audio_url:
                await bot.send_message(chat_id=message.chat.id, text="Извините, ничего не найдено.")
        else:
            await bot.send_message(message.chat.id, f"Произошла ошибка..")
    except requests.exceptions.RequestException as e:
        await bot.send_message(message.chat.id, f"Произошла ошибка..")


# TikTok

RAPID_API_URL = 'https://tiktok-video-no-watermark2.p.rapidapi.com/'
RAPID_API_KEY = '3e98ed8ce1msh1a05c8a7aede75ap1ccdb6jsn2f6f17651931'
HEADERS = {
    'Content-Type': 'application/json',
    'x-rapidapi-host': 'tiktok-video-no-watermark2.p.rapidapi.com',
    'x-rapidapi-key': RAPID_API_KEY
}


# Function to get TikTok video URL using Rapid API
def get_tiktok_video_url_rapid_api_rus(url):
    try:
        response = requests.post(RAPID_API_URL, headers=HEADERS, json={"url": url}, timeout=50)
        response.raise_for_status()

        data = response.json()
        if 'data' in data and 'play' in data['data']:
            return data['data']['play']
        else:
            print(f"Unexpected response structure: {data}")
            return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return None
    except ValueError as e:
        print(f"Value error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# Telegram bot handler to handle TikTok video
async def handle_tiktok_video_rus(message, url):
    try:
        waiting_message = await bot.send_message(message.chat.id, "⏳ Загрузка...")

        # Get the TikTok video URL using Rapid API
        video_url = get_tiktok_video_url_rapid_api_rus(url)

        if video_url:
            # Send the video directly by URL
            await message.reply_video(video_url, caption="Скачано через @insta_tik_tokSaverbot 📥")
            await bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

        else:
            await message.reply("Произошла ошибка..")
    except Exception as e:
        print(f"Error handling TikTok video: {e}")
        await message.reply(f"Произошла ошибка..")


# Youtube
yt = None


async def youtube_download_rus(message, path, call):
    """Download YouTube video by pytube"""

    if call == 'High':
        waiting_message = await bot.send_message(message.chat.id, "⏳ Загрузка...")
        video_path = path.streams.get_highest_resolution().download()
        video_size = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
        if video_size > 50:
            await bot.send_message(message.chat.id, "Размер видео слишком большой.")
        else:
            video = open(video_path, 'rb')
            await bot.send_video(message.chat.id, video, caption="Скачано через @insta_tik_tokSaverbot 📥")
            if path.streams.filter(only_audio=True):
                audio_path = path.streams.get_highest_resolution().download()
                audio_size = os.path.getsize(audio_path) / (1024 * 1024)  # Size in MB
                if audio_size > 50:
                    await bot.send_message(message.chat.id, "Размер аудио слишком большой.")
                else:
                    audio = open(audio_path, 'rb')
                    await bot.send_audio(message.chat.id, audio, caption="Скачано через @insta_tik_tokSaverbot 📥")
            else:
                await bot.send_message(message.chat.id, 'Звук не найден')

        await bot.delete_message(message.chat.id, waiting_message.message_id)
    else:
        waiting_message = await bot.send_message(message.chat.id, "⏳ Загрузка...")
        video_path = path.streams.first().download()
        video_size = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
        if video_size > 50:
            await bot.send_message(message.chat.id, "Размер видео слишком большой.")
        else:
            video_path_copy = video_path.split('\\')[-1]
            name = video_path_copy.split('.')[0]
            result = name + '.mp4'
            os.rename(video_path, result)
            video = open(result, 'rb')
            await bot.send_video(message.chat.id, video, caption="Скачано через @insta_tik_tokSaverbot 📥")
            if path.streams.filter(only_audio=True):
                audio_path = path.streams.first().download()
                audio_size = os.path.getsize(audio_path) / (1024 * 1024)  # Size in MB
                if audio_size > 50:
                    await bot.send_message(message.chat.id, "Размер аудио слишком большой.")
                else:
                    audio = open(audio_path, 'rb')
                    await bot.send_audio(message.chat.id, audio, caption="Скачано через @insta_tik_tokSaverbot 📥")
            else:
                await bot.send_message(message.chat.id, 'Звук не найден')

        await bot.delete_message(message.chat.id, waiting_message.message_id)


async def get_message_rus(message: types.Message):
    """Get link from YouTube"""

    # Remove all .mp4 files
    files = os.listdir()

    for item in files:
        if item.endswith(".mp4"):
            os.remove(item)
    for audio in files:
        if audio.endswith('.mp3'):
            os.remove(audio)

    try:
        global yt
        yt = pytube.YouTube(message.text)

    except pytube.exceptions.RegexMatchError:
        error_message = "Видео по ссылке не найдено"
        await bot.send_message(message.chat.id, error_message)

    keyboard = types.InlineKeyboardMarkup()
    high = types.InlineKeyboardButton('Отличный', callback_data='Отличный')
    low = types.InlineKeyboardButton('Низкий', callback_data='Низкий')
    keyboard.add(high, low)
    await bot.send_message(message.chat.id, 'Выберите качество видео.', reply_markup=keyboard)


@dp.callback_query_handler(text=['Отличный', 'Низкий'])
async def download(callback: types.CallbackQuery):
    """Get callback data and call youtube_download"""

    await youtube_download_rus(callback.message, yt, callback.data)
