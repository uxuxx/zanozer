import logging
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8592333952:AAEmHjjLn5OK6kwE2Kf8Oa-7VsJqC2v0u1U"

user_states = {}

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("Отправка", callback_data="send_report")],
        [InlineKeyboardButton("Подписка", callback_data="subscription")],
        [InlineKeyboardButton("Поддержка", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_subscription_menu():
    keyboard = [
        [InlineKeyboardButton("1$ – 1 день", callback_data="sub_1")],
        [InlineKeyboardButton("3.5$ – 5 дней", callback_data="sub_3_5")],
        [InlineKeyboardButton("5$ – навсегда 30% скидка", callback_data="sub_5")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"Привет, {user.first_name}! Спасибо что зашел в бота!\n\n"
        "Бот очень классный\n\n"
        "Используйте кнопки ниже:"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu()
    )

async def simulate_sending(update: Update, context: ContextTypes.DEFAULT_TYPE, link: str):
    message = await update.message.reply_text(
        f"Ссылка: {link}\n\n"
        "Началась отправка с сессий..."
    )
    
    total = 170
    for i in range(1, total + 1):
        await asyncio.sleep(2)
        
        progress_text = (
            f"Ссылка: {link}\n\n"
            f"Началась отправка с сессий...\n"
            f"Выполнено {i}/{total}"
        )
        
        try:
            await message.edit_text(progress_text)
        except:
            pass
        
        if i == total:
            await message.reply_text(
                "Отправка завершена",
                reply_markup=get_main_menu()
            )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "send_report":
        # Проверяем есть ли подписка
        if user_states.get(user_id, {}).get("has_subscription", False):
            await query.edit_message_text(
                text="Введите ссылку:",
                reply_markup=get_main_menu()
            )
            user_states[user_id] = {"awaiting_link": True, "has_subscription": True}
        else:
            await query.edit_message_text(
                text="Нельзя нажать на отправку до отправки",
                reply_markup=get_main_menu()
            )
    
    elif query.data == "subscription":
        await query.edit_message_text(
            text="Стоимость подписки:",
            reply_markup=get_subscription_menu()
        )
    
    elif query.data == "support":
        await query.edit_message_text(
            text="Ожидайте ответа",
            reply_markup=get_main_menu()
        )
    
    elif query.data == "sub_1":
        # Активируем подписку
        user_states[user_id] = {"has_subscription": True}
        await query.edit_message_text(
            text="Оплата 1$",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Перейти", url="http://t.me/send?start=IVOQfcfSzO0m")
            ]])
        )
    
    elif query.data == "sub_3_5":
        # Активируем подписку
        user_states[user_id] = {"has_subscription": True}
        await query.edit_message_text(
            text="Оплата 3.5$",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Перейти", url="http://t.me/send?start=IVU5kkOz3wS0")
            ]])
        )
    
    elif query.data == "sub_5":
        # Активируем подписку
        user_states[user_id] = {"has_subscription": True}
        await query.edit_message_text(
            text="Оплата 5$",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Перейти", url="http://t.me/send?start=IVDfueJJp8ZW")
            ]])
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_states.get(user_id, {}).get("awaiting_link", False):
        link = update.message.text
        user_states[user_id] = {"awaiting_link": False, "has_subscription": True}
        
        await simulate_sending(update, context, link)
    else:
        await update.message.reply_text(
            "Используйте кнопки",
            reply_markup=get_main_menu()
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
