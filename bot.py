import logging
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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
    application.add_handler(CallbackQueryHandler(self.button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.response_from__message))
    application.run_polling()


  async def start_button(self, update: Update, _) -> None:
    keyboard = [
      [InlineKeyboardButton("⚡ Погнали ⚡", callback_data='1')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нужно подать заявку. Ты готовы?", reply_markup=reply_markup)

  async def button(self, update: Update, _):
    query = update.callback_query
    self.variant = query.data
    await query.answer()
    await query.edit_message_text(text=registration_steps[self.variant])

  async def response_from__message(self, update: Update, _) -> None:
    variant_temp = int(self.variant) + 1
    self.variant = str(variant_temp)
    await update.message.reply_text(registration_steps[self.variant])

def main() -> None:
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  game_bot = MoneyBot(token = API_TOKEN)
  game_bot.run_bot()


if __name__ == "__main__":
  main()