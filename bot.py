import os
import logging
import html
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("universal-stealth-bot")

def get_main_keyboard():
    keyboard = [
        ["🛡️ Снять плагиат (Сохранить язык)"],
        ["ℹ️ Как это работает"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔓 <b>Универсальный стелс-бот запущен!</b>\n\n"
        "Отправь мне текст на любом языке (русский, английский, армянский и т.д.), и я сниму плагиат, сохранив оригинальный язык и слова без изменений.",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

def universal_stealth_bypass(text: str) -> str:
    """
    Универсальный обход: добавляет невидимые нулевые пробелы (\u200B) 
    между символами, что ломает хэш систем проверки на любом языке, 
    оставляя текст визуально абсолютно прежним.
    """
    invisible_space = "\u200B"
    result = []
    
    for i, char in enumerate(text):
        result.append(char)
        # Вставляем невидимый символ через каждые 3-4 символа, 
        # чтобы текст оставался читаемым и проходил проверки
        if i % 3 == 0 and char.isalnum():
            result.append(invisible_space)
            
    return "".join(result)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if "Как это работает" in user_text:
        msg = (
            "💡 <b>О принципах работы:</b>\n\n"
            "• Бот автоматически определяет любой язык (English, Русский, Հայերեն и др.).\n"
            "• Слова, буквы и смысл <b>не перекладываются и не переводятся</b>.\n"
            "• Интегрируются микро-символы нулевой ширины, которые обнуляют совпадения в базах данных."
        )
        await update.message.reply_text(msg, parse_mode="HTML")
        return

    if "Снять плагиат" in user_text:
        await update.message.reply_text("Отправь текст на любом языке:")
        return

    if len(user_text) < 5:
        await update.message.reply_text("⚠️ Текст слишком короткий.")
        return

    await update.message.reply_text("⏳ Обрабатываю текст...")

    # Применяем универсальную стелс-модификацию
    processed_text = universal_stealth_bypass(user_text)

    response = (
        "✅ <b>Готово! Язык и текст сохранены, плагиат снят:</b>\n\n"
        f"<code>{html.escape(processed_text)}</code>\n\n"
        "📋 <i>Скопируй результат и вставляй в документ.</i>"
    )

    await update.message.reply_text(response, parse_mode="HTML")

def main():
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не найден в .env")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Универсальный стелс-бот запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()