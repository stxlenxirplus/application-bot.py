import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from colorama import init, Fore

TOKEN = "ваш токен"
ADMIN_ID = "админ айди"

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Отправьте мне свою ссылку на лолз, и я отправлю его админу на одобрение.")

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_text = update.message.text

    approval_buttons = [
        [
            InlineKeyboardButton("Одобрить", callback_data=f"approve:{user_id}"),
            InlineKeyboardButton("Отклонить", callback_data=f"reject:{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(approval_buttons)

    context.bot.send_message(ADMIN_ID, f"Заявка от {user_id}: {user_text}", reply_markup=reply_markup)

def handle_approval(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    action, user_id = query.data.split(":")

    if action == "approve":
        context.bot.send_message(user_id, "Ваша заявка была одобрена администратором. Вот ссылка на группу: ТУТ ССЫЛКА")
        query.edit_message_text("Заявка одобрена.")
    elif action == "reject":
        context.bot.send_message(user_id, "Ваша заявка была отклонена администратором.")
        query.edit_message_text("Заявка отклонена.")
    else:
        query.edit_message_text("Произошла ошибка. Попробуйте еще раз.")

init()
def main():
    name = "Dev: Mayrs"
    for _ in range(5):
        print(Fore.LIGHTMAGENTA_EX + name + Fore.RESET)


    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(handle_approval))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
