import logging
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

registration_steps = {
}

class MoneyBot():
  def __init__(self, token):
    self.token = token

  def run_bot(self) -> None:
    application = Application.builder().token(self.token).build()
    application.add_handler(CommandHandler("start", self.start_button))
    application.add_handler(CommandHandler("newslon", self.handler_new_slon))
    application.add_handler(CommandHandler("newslon", self.handler_new_slon))
    application.add_handler(CallbackQueryHandler(self.button))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.response_from__message))
    application.run_polling()


  async def start_button(self, update: Update, _) -> None:
    keyboard = [
      [InlineKeyboardButton("Создать нового бота", callback_data='new_slon')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('''*Создайте своего персонального бота*\nЧтобы начать использовать бота отправьте команду /newslon или нажмите на кнопку внизу сообщения\n*Другие полезные команды:*\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
      reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_new_slon(self, update: Update, _) -> None:
    await update.message.reply_text('вы вызвали команду new_slon')

  async def button(self, update: Update, _):
    print('button')
    query = update.callback_query
    if query.data == 'new_slon':
      await query.message.reply_text('вы вызвали команду new_slon')


def main() -> None:
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  game_bot = MoneyBot(token = API_TOKEN)
  game_bot.run_bot()


if __name__ == "__main__":
  main()