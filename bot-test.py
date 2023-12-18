import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

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

        keyboard = [
            [
                InlineKeyboardButton("Утро", callback_data='empty'),
                InlineKeyboardButton("День", callback_data='empty'),
                InlineKeyboardButton("Вечер", callback_data='empty'),
            ],
            [
                InlineKeyboardButton("8:10", callback_data='morning/8:10'),
                InlineKeyboardButton("13:10", callback_data='morning/13:10'),
                InlineKeyboardButton("18:10", callback_data='morning/18:10'),
            ],
            [
                InlineKeyboardButton("9:10", callback_data='morning/9:10'),
                InlineKeyboardButton("14:10", callback_data='morning/14:10'),
                InlineKeyboardButton("19:10", callback_data='morning/19:10'),
            ],
            [
                InlineKeyboardButton("10:10", callback_data='morning/10:10'),
                InlineKeyboardButton("15:10", callback_data='morning/15:10'),
                InlineKeyboardButton("20:10", callback_data='morning/20:10'),
            ],
            [
                InlineKeyboardButton("11:10", callback_data='morning/11:10'),
                InlineKeyboardButton("16:10", callback_data='morning/16:10'),
                InlineKeyboardButton("21:10", callback_data='morning/21:10'),
            ],
            [
                InlineKeyboardButton("12:10", callback_data='morning/12:10'),
                InlineKeyboardButton("17:10", callback_data='morning/17:10'),
                InlineKeyboardButton("22:10", callback_data='morning/22:10'),
            ],
            [
                InlineKeyboardButton("Подтвердить", callback_data='confirm'),
            ],
        ]
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
