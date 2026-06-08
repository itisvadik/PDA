import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

TSP_VERSION = "1.1"

SECRET_KEY = "экспедиция"
MESSAGE_DELAY_SECONDS = 15

TSP_MESSAGES = [
    "Здравствуйте, [lghkbq].",
    f"Вы связались с ТСП-А {TSP_VERSION}.",
    "Запрос зарегистрирован.",
    (
        "Техническое средство для экспедиции будет отправлено\n"
        "на ваш личный КПК в течение 30 минут."
    ),
    "Статус: выполняется.",
    "Ожидайте."
]

WRONG_REPLY = (
    f"// ТСП {TSP_VERSION}.\n\n"
    "Ключ доступа не распознан.\n"
    "Проверьте данные и повторите попытку."
)

def normalize(text: str) -> str:
    return text.strip().lower().replace("ё", "е")

async def type_message(bot, chat_id, text, delay=0.08, step=4, parse_mode=None):
    msg = await bot.send_message(chat_id=chat_id, text="█")

    for i in range(0, len(text), step):
        current_text = text[:i + step]
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=current_text + "█",
            parse_mode=parse_mode
        )
        await asyncio.sleep(delay)

    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg.message_id,
        text=text,
        parse_mode=parse_mode
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await type_message(context.bot, update.effective_chat.id,
        f"// ТСП {TSP_VERSION}.\n\n"
        "Канал связи активен.\n"
        "Введите ключ доступа.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = normalize(update.message.text)
    user = update.effective_user

    if user_text == SECRET_KEY:
        for message in TSP_MESSAGES:
            await type_message(
                context.bot,
                update.effective_chat.id,
                message
            )
            await asyncio.sleep(MESSAGE_DELAY_SECONDS)

        if ADMIN_CHAT_ID:
            await context.bot.send_message(
                chat_id=int(ADMIN_CHAT_ID),
                text=(
                    "СИГНАЛ ПОЛУЧЕН.\n\n"
                    "Квест пройден.\n"
                    f"Пользователь: @{user.username if user.username else 'без username'}\n"
                    f"Имя: {user.full_name}\n\n"
                    "Введён ключ «экспедиция».\n"
                    "Можно отправлять Steam Gift в течение 30 минут."
                )
            )
    else:
        await type_message(context.bot, update.effective_chat.id, WRONG_REPLY)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("Не найден BOT_TOKEN. Заполни файл .env")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ТСП запущен.")
    app.run_polling()

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    main()
