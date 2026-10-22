import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Чтение токена из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Пример простой функции-обработчика (замените на вашу логику бота)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Бот работает! Вы написали: {update.message.text}")

def main():
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не найден в переменных окружения!")
        return

    # Инициализация бота
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    print("Бот запущен и ожидает сообщения...")
    # Запуск бота (Long Polling)
    application.run_polling()


# ==========================================
# ВЕБ-СЕРВЕР ДЛЯ RENDER (УДЕРЖАНИЕ ПОРТА)
# ==========================================
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")
        
    def log_message(self, format, *args):
        # Отключаем лишний спам в логах от пингов
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Запускаем веб-сервер в фоновом потоке
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Запускаем основного Telegram-бота
    main()
