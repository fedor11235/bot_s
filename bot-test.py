import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from keyboards import day_time_choice_keyboard

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class SlonBot():
    def __init__(self, token):
        self.token = token

    def run_bot(self) -> None:
        application = Application.builder().token(self.token).build()
        application.add_handler(CommandHandler("start", self.handler_start))
        application.add_handler(CallbackQueryHandler(self.handler_callback))
        application.run_polling()

    async def handler_start(self, update: Update, _) -> None:
        # тут сделай таблицу
        keyboard = day_time_choice_keyboard()

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '*Выберите допустимое время размещений:',
            reply_markup=reply_markup)

    # all education health news tech entertainment psychology author other
    async def handler_callback(self, update: Update, context):
        query = update.callback_query
        query_array = query.data.split('_')
        value = query_array[0]

        await query.edit_message_text(
            f'*Выбрано: {value}')

        # креативы подборок
        # if query_array[0] == 'callbackdata1':
        #     print('Button Утро')
        #     await query.edit_message_text(
        #         '*Выбрано: Утро')
        #     return
        # elif query_array[0] == 'callbackdata2':
        #     await query.edit_message_text(
        #         '*Выбрано: День')
        #     return

def main() -> None:
    game_bot = SlonBot(token=API_TOKEN)
    game_bot.run_bot()


if __name__ == "__main__":
    main()
