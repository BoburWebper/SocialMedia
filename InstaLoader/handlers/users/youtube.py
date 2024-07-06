import os
import pytube
from aiogram import types

from loader import dp, bot

yt = None


async def youtube_download(message, path, call):
    """Download YouTube video by pytube"""

    if call == 'High':
        waiting_message = await bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")
        video_path = path.streams.get_highest_resolution().download()
        video_size = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
        if video_size > 50:
            await bot.send_message(message.chat.id, "Video hajmi juda katta.")
        else:
            video = open(video_path, 'rb')
            await bot.send_video(message.chat.id, video, caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
            if path.streams.filter(only_audio=True):
                audio_path = path.streams.get_highest_resolution().download()
                audio_size = os.path.getsize(audio_path) / (1024 * 1024)  # Size in MB
                if audio_size > 50:
                    await bot.send_message(message.chat.id, "Musiqa hajmi juda katta.")
                else:
                    audio = open(audio_path, 'rb')
                    await bot.send_audio(message.chat.id, audio,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
            else:
                await bot.send_message(message.chat.id, 'Musiqa topilmadi')
        await bot.delete_message(message.chat.id, waiting_message.message_id)
    else:
        waiting_message = await bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")
        video_path = path.streams.first().download()
        video_size = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
        if video_size > 50:
            await bot.send_message(message.chat.id, "Video hajmi juda katta.")
        else:
            video_path_copy = video_path.split('\\')[-1]
            name = video_path_copy.split('.')[0]
            result = name + '.mp4'
            os.rename(video_path, result)
            video = open(result, 'rb')
            await bot.send_video(message.chat.id, video, caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
            if path.streams.filter(only_audio=True):
                audio_path = path.streams.first().download()
                audio_size = os.path.getsize(audio_path) / (1024 * 1024)  # Size in MB
                if audio_size > 50:
                    await bot.send_message(message.chat.id, "Musiqa hajmi juda katta.")
                else:
                    audio = open(audio_path, 'rb')
                    await bot.send_audio(message.chat.id, audio,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
            else:
                await bot.send_message(message.chat.id, 'Musiqa topilmadi')

        await bot.delete_message(message.chat.id, waiting_message.message_id)


async def get_message(message: types.Message):
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
        error_message = "Link orqali video topilmadi"
        await bot.send_message(message.chat.id, error_message)

    keyboard = types.InlineKeyboardMarkup()
    high = types.InlineKeyboardButton('Yuqori', callback_data='Yuqori')
    low = types.InlineKeyboardButton('Past', callback_data='Past')
    keyboard.add(high, low)
    await bot.send_message(message.chat.id, 'Video sifatini tanlang.', reply_markup=keyboard)


@dp.callback_query_handler(text=['Yuqori', 'Past'])
async def download(callback: types.CallbackQuery):
    """Get callback data and call youtube_download"""

    await youtube_download(callback.message, yt, callback.data)
