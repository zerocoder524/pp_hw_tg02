import asyncio
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InputFile
from googletrans import Translator
from config import TOKEN0

# Создаем папку для сохранения фото, если она не существует
if not os.path.exists('img'):
    os.makedirs('img')

# Инициализация переводчика
translator = Translator()

# Установим SelectorEventLoop для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN0)
dp = Dispatcher()  # Инициализация Dispatcher без передачи bot

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply(
        "Привет! Я бот, который:\n"
        "1. Сохраняю все твои фото в папку img.\n"
        "2. Отправляю голосовые сообщения.\n"
        "3. Перевожу любой текст на английский.\n\n"
        "Отправь мне фото, текст или команду /voice."
    )

# Сохранение фото
@dp.message(lambda message: message.photo)
async def save_photo(message: types.Message):
    # Получаем фото
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    # Сохраняем фото в папку img
    save_path = f"img/{file_id}.jpg"
    await bot.download_file(file_path, save_path)
    await message.reply(f"Фото сохранено: {save_path}")

# Отправка голосового сообщения
@dp.message(Command("voice"))
async def send_voice(message: types.Message):
    # Отправляем голосовое сообщение
    try:
        voice_file = open('voice.mp3', 'rb')  # Убедитесь, что файл voice.mp3 существует
        await bot.send_voice(chat_id=message.chat.id, voice=InputFile(voice_file))
    except FileNotFoundError:
        await message.reply("Файл voice.mp3 не найден.")
    finally:
        if 'voice_file' in locals() and voice_file:
            voice_file.close()

# Перевод текста на английский
@dp.message()
async def translate_text(message: types.Message):
    text = message.text
    try:
        # Переводим текст
        translated = translator.translate(text, dest='en')
        await message.reply(f"Перевод: {translated.text}")
    except Exception as e:
        await message.reply(f"Произошла ошибка при переводе: {e}")

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())