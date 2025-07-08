import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS", "").split(",")]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def notify_admins(text, content_callable=None):
    for admin_id in ADMIN_IDS:
        await bot.send_message(chat_id=admin_id, text=text)
        if content_callable:
            await content_callable(admin_id)


@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    user = message.from_user
    caption = message.caption or "Без подписи"
    photo = message.photo[-1]

    text = (
        f"📬 Новое фото от:\n"
        f"👤 {user.full_name} (@{user.username or 'нет username'})\n"
        f"🆔 ID: {user.id}\n\n"
        f"📝 Подпись: {caption}"
    )

    await notify_admins(text, lambda admin_id: bot.send_photo(admin_id, photo.file_id, caption=caption))
    await message.reply("Спасибо! Фото отправлено на модерацию 😊")


@dp.message_handler(content_types=['document'])
async def handle_document(message: types.Message):
    user = message.from_user
    doc = message.document

    text = (
        f"📬 Новый документ от:\n"
        f"👤 {user.full_name} (@{user.username or 'нет username'})\n"
        f"🆔 ID: {user.id}\n\n"
        f"📄 Имя файла: {doc.file_name}\n"
        f"📦 Размер: {doc.file_size} байт"
    )

    await notify_admins(text, lambda admin_id: bot.send_document(admin_id, document=doc.file_id))
    await message.reply("Спасибо! Документ отправлен на модерацию 😊")


@dp.message_handler(content_types=['video'])
async def handle_video(message: types.Message):
    user = message.from_user
    caption = message.caption or "Без подписи"
    video = message.video

    text = (
        f"📬 Новое видео от:\n"
        f"👤 {user.full_name} (@{user.username or 'нет username'})\n"
        f"🆔 ID: {user.id}\n\n"
        f"📝 Подпись: {caption}\n"
        f"📹 Длительность: {video.duration} сек\n"
        f"🎞 Размер: {video.file_size} байт"
    )

    await notify_admins(text, lambda admin_id: bot.send_video(admin_id, video=video.file_id, caption=caption))
    await message.reply("Спасибо! Видео отправлено на модерацию 😊")


@dp.message_handler()
async def fallback(message: types.Message):
    await message.reply("Пожалуйста, отправьте фотографию или видео для публикации.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
