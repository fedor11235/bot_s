import logging
import requests
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
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
    # application.add_handler(CallbackQueryHandler(self.button))
    application.add_handler(CommandHandler("start", self.start_button))
    application.add_handler(CommandHandler("partners", self.handler_partners))
    application.add_handler(CommandHandler("profile", self.handler_profile))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.response_from__message))
    application.run_polling()


  async def start_button(self, update: Update, _) -> None:
    req = requests.get(
      'http://localhost:3001/check' +
      '?idUser=' + str(update.message.chat.id)
    )
    if req.text == 'exist':
      await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nТеперь заведите профиль в боте, для этого отправьте команду /profile\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
        parse_mode="Markdown")
    else:
      await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
        parse_mode="Markdown")

  async def handler_new_slon(self, update: Update, _) -> None:
    await update.message.reply_text('вы вызвали команду new_slon')

  async def handler_partners(self, update: Update, _) -> None:
    req = requests.get('http://localhost:3001/promocode' + '?id=' + str(update.message.chat.id))
    await update.message.reply_text(req.text)

  async def response_from__message(self, update: Update, context) -> None:
    if update.message.text == 'Каталог':
      await update.message.reply_text('Каталог')
      return
    elif update.message.text == 'Создать опт':
      await update.message.reply_text('Создать опт')
      return
    elif update.message.text == 'Зайти в опт':
      await update.message.reply_text('Зайти в опт')
      return
    elif update.message.text == 'Подборки':
      await update.message.reply_text('Подборки')
      return

    try:
      await context.bot.get_chat_member(user_id=6423584132, chat_id=update.message.text)
      req = requests.get(
        'http://localhost:3001/create-chanel' +
        '?idUser=' + str(update.message.chat.id) +
        '&idChanel=' + update.message.text
      )
      if req.text == 'exist':
        await update.message.reply_text('Ваш канал уже зарегистрирован')
      elif req.text == 'created':
        await update.message.reply_text('Ваш канал успешно зарегистрирован')
        await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nТеперь заведите профиль в боте, для этого отправьте команду /profile\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
        parse_mode="Markdown")
    except:
      await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')

  async def handler_profile(self, update: Update, _) -> None:
    keyboard = [
      [KeyboardButton("Каталог")],
      [KeyboardButton("Создать опт"), KeyboardButton("Зайти в опт")],
      [KeyboardButton("Подборки"), KeyboardButton("Профиль")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('''Вы зашли в профиль''', reply_markup=reply_markup)

  # async def button(update, _):
  #   query = update.callback_query
  #   variant = query.data
  #   await query.answer()
  #   await query.edit_message_text(text=f"Выбранный вариант: {variant}")

def main() -> None:
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  game_bot = MoneyBot(token = API_TOKEN)
  game_bot.run_bot()


if __name__ == "__main__":
  main()
