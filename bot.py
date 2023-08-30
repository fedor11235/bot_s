import logging
import requests
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, BotCommand, BotCommandScopeDefault, BotCommandScopeAllGroupChats
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import os

def set_catalog():
  keyboard = [
    [InlineKeyboardButton("Все тематики", callback_data='2')],
    [InlineKeyboardButton("Образование", callback_data='2')],
    [InlineKeyboardButton("Финансы", callback_data='2')],
    [InlineKeyboardButton("Здоровье", callback_data='2')],
    [InlineKeyboardButton("Новости", callback_data='2')],
    [InlineKeyboardButton("IT", callback_data='2')],
    [InlineKeyboardButton("Развлечения", callback_data='2')],
    [InlineKeyboardButton("Психология", callback_data='2')],
    [InlineKeyboardButton("Видосники", callback_data='2')],
    [InlineKeyboardButton("Юмор", callback_data='2')],
    [InlineKeyboardButton("Авторские", callback_data='2')],
    [InlineKeyboardButton("Другое", callback_data='2')],
  ]
  return InlineKeyboardMarkup(keyboard)

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
    application.add_handler(CallbackQueryHandler(self.button))
    application.add_handler(CommandHandler("start", self.start_button))
    application.add_handler(CommandHandler("partners", self.handler_partners))
    application.add_handler(CommandHandler("profile", self.handler_profile))
    application.add_handler(CommandHandler("help", self.handler_help))
    application.add_handler(CommandHandler("channel", self.handler_channel))
    application.add_handler(CommandHandler("pay", self.handler_pay))
    application.add_handler(CommandHandler("catalog", self.handler_catalog))
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
      reply_markup = set_catalog()
      await update.message.reply_text('Каталог', reply_markup=reply_markup)
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
        await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nТеперь зайдите в профиль, для этого отправьте команду /profile\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
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
    await update.message.reply_text('''*Вы зашли в профиль*\n/channel - добавить канал\n/help - поддержка\n/pay - оплата подписки\n/catalog - каталог\n/newopt - создать опт\n/getopt - войти в опт\n/busines - подборки\n/profile - мой профиль''', reply_markup=reply_markup, parse_mode="Markdown")
  
  async def handler_help(self, update: Update, _) -> None:
    await update.message.reply_text('''*Возникли вопросы?*\nМы всегда готовы помочь вам с любые задачи и решение всех интересующих вопросов.\nПросто напишите нам: @slon_feedback''')

  async def handler_channel(self, update: Update, _) -> None:
    await update.message.reply_text('''Чтобы добавить канал введите в поле ниже\n''')

  async def handler_pay(self, update: Update, _) -> None:
    keyboard = [
      [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
      [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
      [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_catalog(self, update: Update, _) -> None:
    reply_markup = set_catalog()
    await update.message.reply_text('Выберите тематику:',reply_markup=reply_markup)
  
  async def button(self, update: Update, _):
    keyboard = [
      [InlineKeyboardButton("Ввести промокод", callback_data='promocode_enter')],
      [InlineKeyboardButton("30 дней за 0", callback_data='pay_fo_30')],
      [InlineKeyboardButton("90 дней за 0", callback_data='pay_fo_90')],
      [InlineKeyboardButton("365 дней за 0", callback_data='pay_fo_365')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    if query.data == 'pay_lite':
      await query.answer()
      await query.edit_message_text(text='Выберите срокна который хотите продлить подписку Lite\nВаша скидка: 0%',  reply_markup=reply_markup)
    if query.data == 'pay_pro':
      await query.answer()
      await query.edit_message_text(text='Выберите срокна который хотите продлить подписку Pro\nВаша скидка: 0%',  reply_markup=reply_markup)
    if query.data == 'pay_business':
      await query.answer()
      await query.edit_message_text(text='Выберите срокна который хотите продлить подписку Business\nВаша скидка: 0%',  reply_markup=reply_markup)

def main() -> None:
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  game_bot = MoneyBot(token = API_TOKEN)
  game_bot.run_bot()


if __name__ == "__main__":
  main()
