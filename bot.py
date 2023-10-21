from datetime import datetime
from collections import Counter
# import re
from functools import reduce
import logging
import requests
from telegram import Update, LabeledPrice
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, PreCheckoutQueryHandler
from dotenv import load_dotenv
import os

from parse import get_text_for_post

from key import handler_btn_keyboard
from opt_creative import opt_creative
from recommendation_creative import recommendation_creative
from creation_opts import creation_opts

from requests_data import (
  opt_set_check,
  recommendation_set_check,
  opt_requisites,
  recommendation_requisites,
  user_opt,
  user_recommendation_into,
  user_opt_into,
  set_any_profile,
  set_opt_recommendation_into,
  upload_promocode,
  get_opt_into,
  set_opt_into,
  parse_view_date,
  set_tariff_profile,
  user_get_stat_opt,
  user_check,
  user_change_message_mod,
  user_get_message_mod, 
  opt_create,
  opt_set,
  opt_get,
  parse_filter,
  create_chanel,
  get_profile,
  recommendations_get,
  recommendations_ind_get,
  set_channel
)

from create_btns import (
  get_reservation_req_table,
  get_btns_categories,
  get_reservation_into_table,
  btns_recommendations_get,
  set_filters_opt,
  get_categories,
  set_catalog,
  set_filters,
  get_btns_pay,
  get_user_chanels,
  get_reservation_table,
  get_reservation_more_table,
  get_reservation_time_table,
  get_opt_create,
  go_into_opt,
  go_into_opt_user,
  go_chanel_opt,
  go_chanel_opt_into,
  opt_reservation,
  user_get_btns_into
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# filters_type = ['rating', 'coverage', 'numberSubscribers', 'growthMonth', 'growthWeek', 'new', 'old', 'confirm']
filters_type = ['repost', 'numberSubscribers', 'coveragePub', 'coverageDay', 'indexSay']
# category_type = ['all', 'education', 'finance', 'health', 'news', 'tech', 'entertainment', 'psychology', 'video', 'author', 'other']
# categories = ['all', 'Образ', 'Финансы', 'Здоровье', 'Новости', 'IT', 'Досуг', 'Психология', 'Видосики', 'Авторские', 'Другое']
categoriesBd = ['all', 'Education', 'Finance', 'Health', 'News', 'IT', 'Entertainment', 'Psychology', 'Videos', 'Copyright', 'Other']

class SlonBot():
  def __init__(self, token):
    self.token = token

  def run_bot(self) -> None:
    application = Application.builder().token(self.token).build()
    application.add_handler(CommandHandler("test", self.handler_test))
    application.add_handler(CommandHandler("test_secret_profile_base", self.handler_secret_profile_base))
    application.add_handler(CommandHandler("test_secret_profile_lite", self.handler_secret_profile_lite))
    application.add_handler(CommandHandler("test_secret_profile_pro", self.handler_secret_profile_pro))
    application.add_handler(CommandHandler("test_secret_profile_business", self.handler_secret_profile_business))
    application.add_handler(CommandHandler("get_profile_business", self.handler_get_profile_business))
    application.add_handler(PreCheckoutQueryHandler(self.handler_checkout))
    application.add_handler(CallbackQueryHandler(self.handler_callback))
    application.add_handler(CommandHandler("start", self.handler_start))
    application.add_handler(CommandHandler("partners", self.handler_partners))
    application.add_handler(CommandHandler("profile", self.handler_profile))
    application.add_handler(CommandHandler("help", self.handler_help))
    application.add_handler(CommandHandler("channel", self.handler_channel))
    application.add_handler(CommandHandler("newopt", self.handler_newopt))
    application.add_handler(CommandHandler("getopt", self.handler_getopt))
    application.add_handler(CommandHandler("business", self.handler_business))
    application.add_handler(CommandHandler("pay", self.handler_pay))
    # application.add_handler(ImageHandler("getopt", self.image_handler))
    # application.add_handler(CommandHandler("catalog", self.handler_catalog))
    application.add_handler(MessageHandler(filters.ANIMATION | filters.VIDEO | filters.PHOTO | filters.TEXT & ~filters.COMMAND, self.response_from__message))
    # application.add_handler(MessageHandler(filters.PHOTO, self.handler_photo))
    application.run_polling()

  async def handler_start(self, update: Update, _) -> None:
    user_id = update.message.chat.id
    user_stat = user_check(user_id)
    keyboard = [
      # [KeyboardButton("Каталог")],
      [KeyboardButton("Создать опт"), KeyboardButton("Зайти в опт")],
      [KeyboardButton("Подборки"), KeyboardButton("Профиль")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    if user_stat == 'empty':
      await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
        reply_markup=reply_markup, parse_mode="Markdown")
    else:
      user_change_message_mod(user_id, 'standart')
      await update.message.reply_text('''\nВоспользуйтесь кнопками ниже или основным меню для работы с ботом:''', 
        reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_new_slon(self, update: Update, _) -> None:
    await update.message.reply_text('вы вызвали команду new_slon')

  async def handler_partners(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      req = requests.get('http://localhost:3001/user/promocode' + '?idUser=' + str(update.message.chat.id))
      res = req.json()
      # if res == 'no':
      #   await update.message.reply_text('Вы исчерпали лимит генерации промокодов')
      # else:
      await update.message.reply_text('Ваш промокод: ' + req.json())

  async def handler_business(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      keyboard = [
        [InlineKeyboardButton("<<Назад", callback_data='testtest'), InlineKeyboardButton("Смотреть предложения", callback_data='watch_see')]
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      await update.message.reply_text('*Подборки* — это инструмент автоматической масштабной закупки рекламы в топовых telegram-каналах по уникальным ценам.', reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_newopt(self, update: Update, _) -> None:
    user_id = update.message.chat.id
    user_stat = user_check(user_id)
    if user_stat == 'empty':
      keyboard = [
        [InlineKeyboardButton("Добавить канал", callback_data='chanelAdd')],
      ]
      reply_markup =  InlineKeyboardMarkup(keyboard)
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      user = get_profile(user_id)
      tariff_plan = user['tariffPlan']
      if tariff_plan == 'base':
          keyboard = [
            [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
            [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
            [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          await update.message.reply_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")
      else:
        req = requests.get(
          'http://localhost:3001/chanel/user' +
          '?idUser=' + str(update.message.chat.id)
          )
        chanels = req.json()
        reply_markup = get_user_chanels(chanels)
        await update.message.reply_text('Выберите канал в котором хотите собрать опт:', reply_markup=reply_markup)
    return

  async def handler_getopt(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      reply_markup = go_into_opt_user()
      await update.message.reply_text('Зайти в опт', reply_markup=reply_markup)

  async def response_from__message(self, update: Update, context) -> None:
    user_id = update.message.chat.id
    mode = user_get_message_mod(user_id)
    username = '@' + update.message.from_user.username

    # функция для работы кнопок клавиатуры
    await handler_btn_keyboard(update, context)

    # ввод креативов опта
    await opt_creative(update, context)
  
    # ввод креативов подборок
    await recommendation_creative(update, context)

    await creation_opts(update, context)

    # отправка чеков владельцу опта и подборок
    if mode == 'recommendation-check':
      user_id = update.message.chat.id
      mode = user_get_message_mod(user_id)
      file_id = update.message.photo[-1].file_id
      profile = get_profile(user_id)

      file_info = await context.bot.get_file(file_id)
      file_path = file_info.file_path
      recommendation_set_check(user_id, profile['rec_into_temp'], file_id, file_path)
      await update.message.reply_text('Чек придет владельцу опта')
      user_change_message_mod(user_id, 'standart')
    elif mode == 'opt-check':
      user_id = update.message.chat.id
      mode = user_get_message_mod(user_id)
      file_id = update.message.photo[-1].file_id
      profile = get_profile(user_id)

      file_info = await context.bot.get_file(file_id)
      file_path = file_info.file_path
      opt_set_check(user_id, profile['rec_into_temp'], file_id, file_path)
  
      await update.message.reply_text('Чек придет владельцу опта')
      user_change_message_mod(user_id, 'standart')


      try:
        requisites = update.message.text
        data = {'requisites': requisites}
        opt = opt_set(user_id, data)
        reply_markup = get_opt_create(opt['chanel'])
        booking_date = opt['booking_date'].split('_')
        booking_date_parse = parse_view_date(booking_date)
        current_datetime = datetime.now()
        month_now = current_datetime.month
        day_now = current_datetime.day
        date = str(day_now) + '.' + str(month_now)
        first_name = update.message.chat.first_name
        username = update.message.chat.username
        await update.message.reply_text('''
Опт от '''+ date +''' в канале ['''+opt['title']+'''](https://t.me/'''+opt['chanel'][1:]+''')\n
*Розничная цена:* '''+ str(opt['retail_price']) + ''' \n
*Оптовая цена:* '''+ str(opt['wholesale_cost']) + '''\n
*Минимум постов:* '''+ str(opt['min_places']) + '''\n
*Максимум постов:* '''+ str(opt['max_places']) + '''\n
*Список дат:* \n'''+ booking_date_parse + '''\n
*Дедлайн:* '''+ opt['deadline_date'] + '''\n
*Реквизиты:* '''+ opt['requisites'] + '''\n
*Владелец:* ['''+first_name+'''](https://t.me/'''+username+''')'''
        ,
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=None
      )
      except:
        await update.message.reply_text("Упс произошла ошибка")
      return
    #ввод промокода
    elif mode == 'promocode':
      promocode = update.message.text
      user_change_message_mod(update.message.chat.id, 'standart')
      res = upload_promocode(user_id, promocode)
      profile = get_profile(user_id)
      reply_markup = get_btns_pay(profile['tariffPlan_temp'], profile['discount'], user_id)
      if res == 'not-exist':
        await update.message.reply_text(text='Такого промокода не существует')
      elif res == 'expired':
        await update.message.reply_text(text='Просроченный промокод')
      elif res == 'owner':
        await update.message.reply_text(text='Вы являетесь владельцем промокода')
      await update.message.reply_text(text='Выберите срок на который хотите продлить подписку *' + profile['tariffPlan_temp'].title() + '*:\n',  reply_markup=reply_markup, parse_mode="Markdown")
      return
    #добавление канала
    elif mode == 'chanel':
      status = ''
      try:
        if update.message.forward_from_chat:
          idChanel = update.message.forward_from_chat.id
          await context.bot.get_chat_member(user_id=6569483795, chat_id=str(idChanel))
          chat_info = await context.bot.get_chat(chat_id=idChanel)
          
          status = create_chanel(user_id, idChanel, chat_info.title)

          if status == 'exist':
            await update.message.reply_text('Такой канал уже добавлен')
            return
          elif status == 'created':
            reply_markup = get_btns_categories()
            await update.message.reply_text('Введите категорию канала: ', reply_markup=reply_markup)
            # user_change_message_mod(update.message.chat.id, 'type-chanel')
            return
        else:
          text = update.message.text
          if 'https' in text:
            username = '@' + text.split('/')[-1]
            try:
              await context.bot.get_chat_member(user_id=6569483795, chat_id=username)
              chat_info = await context.bot.get_chat(chat_id=username)
              
              status = create_chanel(user_id, username, chat_info.title)
        
            except:
              await update.message.reply_text('Бот не принимает ссылки на частные каналы и чаты. Отправьте @username или ID канала, или просто перешлите любое сообщение из него прямо сюда.')
              user_change_message_mod(update.message.chat.id, 'standart')
              return
          else:
            await context.bot.get_chat_member(user_id=6569483795, chat_id=text)
            chat_info = await context.bot.get_chat(chat_id=text)
            status = create_chanel(user_id, text, chat_info.title)

        
        if status == 'exist':
          await update.message.reply_text('Такой канал уже добавлен')
          user_change_message_mod(update.message.chat.id, 'standart')
          return
        elif status == 'created':
          reply_markup = get_btns_categories()
          await update.message.reply_text('Введите категорию канала: ', reply_markup=reply_markup)
          # user_change_message_mod(update.message.chat.id, 'type-chanel')
          return
        user_change_message_mod(update.message.chat.id, 'standart')

      except:
        user_change_message_mod(update.message.chat.id, 'standart')
        await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')
        return

    user_stat = user_check(user_id)
    if user_stat == 'empty':
      status = ''
      try:
        if update.message.forward_from_chat:
          idChanel = update.message.forward_from_chat.id
          await context.bot.get_chat_member(user_id=6569483795, chat_id=str(idChanel))

          chat_info = await context.bot.get_chat(chat_id=idChanel)
          status = create_chanel(user_id, idChanel, chat_info.title, update.message.from_user.username)
          # user_change_message_mod(update.message.chat.id, 'type-chanel')
        else:
          if 'https' in update.message.text:
            username = '@' + update.message.text.split('/')[-1]

            try: 
              await context.bot.get_chat_member(user_id=6569483795, chat_id=username)
              chat_info = await context.bot.get_chat(chat_id=username)
              status = create_chanel(user_id, username, chat_info.title, update.message.from_user.username)
        
            except:
              await update.message.reply_text('Бот не принимает ссылки на частные каналы и чаты. Отправьте @username или ID канала, или просто перешлите любое сообщение из него прямо сюда.')
              user_change_message_mod(update.message.chat.id, 'standart')
              return
          else:
            await context.bot.get_chat_member(user_id=6569483795, chat_id=update.message.text)
            chat_info = await context.bot.get_chat(chat_id=update.message.text)
            status = create_chanel(user_id, update.message.text, chat_info.title, update.message.from_user.username)
            # user_change_message_mod(update.message.chat.id, 'type-chanel')
        if status == "created":
          reply_markup = get_btns_categories()
          await update.message.reply_text('Введите категорию канала: ', reply_markup=reply_markup)
          # user_change_message_mod(update.message.chat.id, 'type-chanel')
          # await update.message.reply_text('Ваш канал успешно зарегистрирован')
        else:
          await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')
      except:
        await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')
        return

  async def handler_profile(self, update: Update, _) -> None:
    user_id = update.message.chat.id
    user_stat = user_check(user_id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', reply_markup=reply_markup, parse_mode="Markdown")
    else:
      keyboard = [
        [InlineKeyboardButton("Мои опты", callback_data='my-opt')],
        [InlineKeyboardButton("Опты в которых я участвую", callback_data='my-req')],
        [InlineKeyboardButton("Подборки в которых я участвую", callback_data='my-opt-into')],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      profile = get_profile(user_id)
      await update.message.reply_text("*Здесь собирается информация, показывающая насколько вы Slon.*\n\n*Подписка " + profile['tariffPlan'] + "* действует до: "+ profile['subscriptionEndDate'] +"\n*Ваши каналы:* " + str(profile['userNumber']) + "\n*Создано оптов:* " + str(profile['optNumber']) + " на сумму " + str(profile['totalSavings']) + "\n*Куплено оптов:* " + str(profile['byOpt']) + " на сумму " + str(profile['totalEarned']) + "\n*Всего сэкономлено:*  "+ str(profile['totalEarned']) + "\n*Приглашено пользователей:* "+ str(profile['totalEarned']) + "\n*Всего заработано:* "+ str(profile['totalEarned'] )+ "", reply_markup=reply_markup, parse_mode="Markdown")
  
  async def handler_help(self, update: Update, _) -> None:
    await update.message.reply_text('''Возникли вопросы?\n\nМы всегда готовы помочь вам с решением любых задач и ответить на все интересующие вопросы. Просто напишите нам: @slon_feedback''')

  async def handler_channel(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      user_change_message_mod(update.message.chat.id, 'chanel')
      await update.message.reply_text('''Чтобы добавить канал, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n''')

  async def handler_pay(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      keyboard = [
        [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
        [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
        [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      await update.message.reply_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_catalog(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      reply_markup = set_catalog()
      await update.message.reply_text('Выберите тематику:',reply_markup=reply_markup)
  
  # all education health news tech entertainment psychology author other
  async def handler_callback(self, update: Update, context):

    query = update.callback_query
    query_array = query.data.split('_')
    user_id = query.message.chat.id

    # креативы подборок
    if query_array[0] == 'recommendation-creative-two':
      user_change_message_mod(user_id, 'recommendation-creative-three')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return
    if query_array[0] == 'recommendation-creative-three':
      user_change_message_mod(user_id, 'recommendation-creative-four')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return
    if query_array[0] == 'recommendation-creative-four':
      user_change_message_mod(user_id, 'recommendation-creative-five')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return
    if query_array[0] == 'recommendation-creative-five':
      user_change_message_mod(user_id, 'standart')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return

    # креативы опта
    if query_array[0] == 'opt-creative-two':
      user_change_message_mod(user_id, 'opt-creative-three')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return
    if query_array[0] == 'opt-creative-three':
      user_change_message_mod(user_id, 'opt-creative-four')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return
    if query_array[0] == 'opt-creative-four':
      user_change_message_mod(user_id, 'opt-creative-five')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return
    if query_array[0] == 'opt-creative-five':
      user_change_message_mod(user_id, 'standart')
      await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
      return
    
    # одобрение креативов
    elif query_array[0] == 'recommendation-creative-accept':
      profile = get_profile(user_id)
      rec_old = recommendation_requisites(profile['rec_into_temp'])
      user_change_message_mod(user_id, 'recommendation-check')
      await query.edit_message_text('Креативы переданы владельцу канала. Вам придет уведомление когда он ответит.\n Оплатитите присланные реквизиты и пришлите скрин оплаты:\n' + str(rec_old))
      return
    
    elif query_array[0] == 'opt-creative-accept':
      profile = get_profile(user_id)
      opt_old = opt_requisites(profile['opt_into_temp'])
      user_change_message_mod(user_id, 'opt-check')
      await query.edit_message_text('Креативы переданы владельцу канала. Вам придет уведомление когда он ответит.\n Оплатитите присланные реквизиты и пришлите скрин оплаты\n' + str(opt_old))
      return

    #!Подписчки
    if query_array[0] == 'pay':
      profile = get_profile(user_id)
      await query.answer()
      if query_array[1] == 'lite':
        reply_markup = get_btns_pay('lite', profile['discount'], user_id)
        await query.edit_message_text(text='Выберите срок на который хотите продлить подписку *Lite*:\n',  reply_markup=reply_markup, parse_mode="Markdown")
        return
      elif query_array[1] == 'pro':
        reply_markup = get_btns_pay('pro', profile['discount'], user_id)
        await query.edit_message_text(text='Выберите срок на который хотите продлить подписку *Pro*:\n',  reply_markup=reply_markup, parse_mode="Markdown")
        return
      elif query_array[1] == 'business':
        reply_markup = get_btns_pay('business', profile['discount'], user_id)
        await query.edit_message_text(text='Выберите срок на который хотите продлить подписку *Business*:\n',  reply_markup=reply_markup, parse_mode="Markdown")
        return
      elif query_array[1] == 'check':
        label = ''
        sub = ''
        day = ''
        price = int(query_array[4] + '00')
        value = query_array[4] + '.00'
        if query_array[2] == 'lite':
          sub = 'lite'
          if query_array[3] == 'litle':
            label = 'Lite — '+query_array[4]+'₽/мес.'
            day = '30'
          elif query_array[3] == 'middle':
            label = 'Lite — '+query_array[4]+'₽/3мес.'
            day = '90'
          elif query_array[3] == 'big':
            label = 'Lite — '+query_array[4]+'₽/год.'
            day = '365'
            
        elif query_array[2] == 'pro':
          sub = 'pro'
          if query_array[3] == 'litle':
            label = 'Pro — '+query_array[4]+'₽/мес.'
            day = '30'
          elif query_array[3] == 'middle':
            label = 'Pro — '+query_array[4]+'₽/3мес.'
            price = 240300
            day = '90'
          elif query_array[3] == 'big':
            label = 'Pro — '+query_array[4]+'₽/год.'
            day = '365'
          
        elif query_array[2] == 'business':
          sub = 'business'
          if query_array[3] == 'litle':
            label = 'Business — '+query_array[4]+'₽/мес.'
            day = '30'
          elif query_array[3] == 'middle':
            label = 'Business — '+query_array[4]+'₽/3мес.'
            day = '90'
          elif query_array[3] == 'big':
            label = 'Business — '+query_array[4]+'₽/год.'
            day = '365'
        set_tariff_profile(user_id, sub, day)
        await context.bot.send_invoice(chat_id=query.message.chat_id, title="Оплата подписки", description="Для того чтобы оплатить нажмите кнопку ниже:", payload="payload",
          provider_data = {"receipt": {"items": [{"description": "Название товара", "quantity": 1, "amount": {"value": value, "currency": "RUB"}, "vat_code": 1}], "customer": {"email": "mail@mail.ru"}}},                     
          provider_token="390540012:LIVE:40517", start_parameter="", currency="RUB",
          prices=[
            LabeledPrice(label, price),
        ])
        return
    #!КАТЕГОРИИ
    elif query_array[0] == 'set-category':
      category = query_array[1]
      set_channel(user_id, category)
      await query.message.reply_text('Ваш канал успешно загрегестрирован')
      user_change_message_mod(query.message.chat.id, 'standart')
    elif query_array[0] in categoriesBd:
      start_cut = 1
      finish_cut = 10
      page = int(query_array[2])
      if query_array[1] == 'static':
        page += 1
      if query_array[1] == 'next':
        start_cut = (page * 10) + 1
        finish_cut = (page + 1) * 10
        page = page + 1
      elif query_array[1] == 'back':
        start_cut = ((page - 2) * 10) + 1
        finish_cut = (page - 1) * 10
        page = page - 1
      categoriesArray = get_categories(query_array[0], start_cut, finish_cut, page, user_id)
      try:
        await query.edit_message_text('все каналы', reply_markup=categoriesArray)
      except:
        await query.answer()
    #!ФИЛЬТРЫ
    elif query_array[0] == 'filters':
      user = get_profile(user_id)
      filter = parse_filter(user['filter'])
      reply_markup =  set_filters(query_array[1], filter)
      await query.edit_message_text('Фильтры', reply_markup=reply_markup)
    elif query_array[0] in filters_type:
      reply_markup =  set_filters(query_array[1], query_array[0])
      await query.edit_message_text('Фильтры', reply_markup=reply_markup)
    elif query_array[0] == 'apply':
      profile = get_profile(user_id)
      categoriesArray = go_chanel_opt_into(query_array[1], 1, 10, 1, profile['filter_opt'], user_id)
      await query.edit_message_text('все каналы', reply_markup=categoriesArray)
    #!Каналы
    elif '@' in query_array[0]:
      try:

        req = requests.get(
          'http://localhost:3001/chanel/get' +
          '?username=' + query_array[0]
          )
        
        chanel =  req.json()

        keyboard = [
          [InlineKeyboardButton("<<Назад", callback_data=query_array[1] + '_static_0')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = query_array[0] + '\nПодписчиков: ' + str(chanel['participants_count']) + '\nОхват: ' + str(chanel['avg_post_reach']) + '\nЦена рекламы:' + '?' + '\nРекомендаций: ' + '?' + '\nКонтакт для связи: ' + '?'

        await query.edit_message_text(reply_text, reply_markup=reply_markup)
      except:
        await query.edit_message_text("Упс произошла ошибка")
    #!Опт
    elif query_array[0] == 'opt':
      if query_array[1] == 'confirm':
        reply_markup = get_reservation_table()
        opt = opt_set(user_id, {})
        booking_date = opt['booking_date'].split('_')
        booking_date_parse = parse_view_date(booking_date)
        await query.message.reply_text('Хотите выбрать следующие даты:?\n' + booking_date_parse, reply_markup=reply_markup)
        return
      elif query_array[1] == "change":
        opt = opt_set(user_id, {})

        bookeds = []
        if opt != None:
          if isinstance(opt['booking_date'], str):
            bookeds = opt['booking_date'].split('_')
          
        reply_markup = get_reservation_more_table(bookeds)
        await query.message.reply_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)

      elif query_array[1] == 'save':
        user_change_message_mod(user_id, 'deadline-wholesale-formation')
        await query.message.reply_text('Укажите крайнюю дату формирования опта в формате 31.12. По наступлении этой даты, если опт не будет собран, он будет отменен.')
        return
      elif query_array[1] == 'time':
        user_change_message_mod(user_id, 'opt-send-details')
        await query.message.reply_text('Пришлите реквизиты для оплаты одним сообщением:')
        return
      elif query_array[1] == 'create':
        data = {'status': 'confirmed'}
        opt_set(user_id, data)
        user_change_message_mod(user_id, 'standart')
        await query.message.reply_text('Поздравляем! Опт успешно создан и добавлен в каталог.')
        return
      elif query_array[1] in categoriesBd:
        start_cut = 1
        finish_cut = 10
        page = 1
        reply_markup = go_chanel_opt(query_array[1], start_cut, finish_cut, page)

        await query.message.reply_text('Выберите категорию', reply_markup=reply_markup)
        return
      elif '@' in query_array[1]:
        try:
          req = requests.get(
          'http://localhost:3001/chanel/get' +
          '?username=' + query_array[1]
          )

          chanel =  req.json()
          keyboard = [
            [InlineKeyboardButton("<<Назад", callback_data='opt_' + query_array[2] + '_static_0')],
            [InlineKeyboardButton("Записаться", callback_data='opt_' + 'sign-up_' +query_array[2])]
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          reply_text = query_array[1] + '\nОсталось мест: [х/у]' + '\nПодписчиков: ' + str(chanel['participants_count']) + '\nОхват: ' + str(chanel['avg_post_reach']) + '\nЦена рекламы:' + '?' + '\nРекомендаций: ' + '?' + '\nКонтакт для связи: ' + '?'

          await query.edit_message_text(reply_text, reply_markup=reply_markup)
        except:
          await query.edit_message_text("Упс произошла ошибка")
        return
      elif query_array[1] == 'sign-up':
        reply_markup = opt_reservation()
        await query.edit_message_text('Выберите дату: ', reply_markup=reply_markup)
        return
      elif query_array[1] == 'reservation':
        if query_array[2] == 'confirm':
          keyboard = [
            [InlineKeyboardButton("Вернуться в каталог", callback_data='test')]
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          await query.edit_message_text('Креативы переданы владельцу канала. Вам придет уведомление когда он ответит.')
          return
        elif query_array[2] == 'paid':
          keyboard = [
            [InlineKeyboardButton("Подтвердить", callback_data='opt_reservation_confirm')]
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          await query.edit_message_text('Поздравляем! Выбранные места успешно забронированы. Пришлите рекламные креативы сюда или напрямую владельцу [юзер владельца].')
          return
        # elif query_array[1] == 'morning' or query_array[2] == 'day' or query_array[2] == 'evening':
        #   return
        keyboard = [
          [InlineKeyboardButton("<<Назад", callback_data='opt_reservation_back')],
          [InlineKeyboardButton("Оплатил ✅", callback_data='opt_reservation_paid')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('*Чтобы забронировать выбранные даты, оплатите [сумма] на реквизиты владельца канала, затем нажмите кнопку ниже:*', reply_markup=reply_markup, parse_mode="Markdown")
        return
      elif query_array[1] == 'init':
        opt_create(user_id, str(query_array[2]))

        user_change_message_mod(user_id, 'opt-retail-price')

        await query.message.reply_text('Создаем опт для канала '+ str(query_array[2]) +'. Напишите стандартную(розничную) стоимость размещения: ')
      elif query_array[1] == 'into':
        if query_array[2] in categoriesBd:
          if query_array[3] == 'back':
            reply_markup = go_into_opt_user()
            await query.edit_message_text('Зайти в опт', reply_markup=reply_markup)
          if query_array[3] == 'data':
            # username = query.from_user.username
            
            opt_old = set_opt_into(user_id, query_array[4],  {}, 'enabled')

            bookeds = []
            booked_send = ''

            if opt_old != None:
              # if isinstance(opt_old['booking_date'], str):
              booked_send = opt_old['booking_date']
              bookeds = booked_send.split('_')

            repeated_elements = [item for item, count in Counter(bookeds).items() if count > 1]

            c = list(set(bookeds) ^ set(repeated_elements))
            c = [s for s in c if s]

            str_booked = '_'.join(c)
            
            opt = set_opt_into(user_id, query_array[4],  {'booking_date': str_booked}, 'none')

            allowed_dates = opt['allowed_dates'].split('_')

            reply_markup = get_reservation_into_table(bookeds=c, offset = 0, channel=query_array[4], allowed_dates=allowed_dates)
            await query.edit_message_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)
            return
          elif query_array[3] == 'next':
            old = int(query_array[4])
            start_cut = old * 10
            finish_cut = (old + 1) * 10
            page = old + 1
            profile = get_profile(user_id)
            reply_markup = go_chanel_opt_into(query_array[2], start_cut, finish_cut, page, profile['filter_opt'], user_id)
            await query.edit_message_text('Выберите опт', reply_markup=reply_markup)
            return
          elif query_array[3] == 'filters':
            user = get_profile(user_id)
            filter = parse_filter(user['filter_opt'])
            if not filter:
              filter = ''
            reply_markup =  set_filters_opt(query_array[2], filter)
            await query.message.reply_text('Фильтры:', reply_markup=reply_markup)
          elif query_array[3] == 'old':
            opt = user_get_stat_opt(query_array[4])
            reply_markup = user_get_btns_into(query_array[2], opt['chanel'] )
            booking_date = opt['booking_date'].split('_')
            booking_date_parse = parse_view_date(booking_date)
            profile = get_profile(opt['user_id'])
            await query.edit_message_text('''
*Опт в канале:* ['''+ str(opt['title']) +'''](https://t.me/'''+opt['chanel'][1:]+''')\n                            
*Розничная цена:* '''+ str(opt['retail_price']) +'''\n
*Оптовая цена:* '''+ str(opt['wholesale_cost']) +'''\n
*Минимум постов:* '''+ str(opt['min_places']) +'''\n
*Максимум постов:* '''+ str(opt['max_places']) +'''\n
*Список дат:* \n'''+ booking_date_parse +'''\n
*Дедлайн:* '''+ str(opt['deadline_date']) +'''\n
*Реквизиты:* '''+ str(opt['requisites']) +'''\n
*Владелец:* @'''+ str(profile['username']) +'''\n
''', reply_markup=reply_markup, parse_mode="Markdown")
          elif query_array[3] == 'init':
            start_cut = 1
            finish_cut = 10
            page = 1
            profile = get_profile(user_id)
            reply_markup = go_chanel_opt_into(query_array[2], start_cut, finish_cut, page, profile['filter_opt'], user_id)
            await query.edit_message_text('Выберите опт', reply_markup=reply_markup)
        return

    elif query_array[0] == 'reservation':
      booking_date_old = ''
      opt_old = opt_get(user_id)
      offset = 0
      if query_array[1] == 'more':
        offset_old = int(query_array[2])
        if offset_old < 20:
          offset = offset_old + 10
        else:
          await query.answer()
          return
          # offset = offset_old
        if opt_old != None:
          if isinstance(opt_old['booking_date'], str):
            booking_date_old += opt_old['booking_date']
          booking_date = booking_date_old
          array_booking_date = booking_date.split('_')

          repeated_elements = [item for item, count in Counter(array_booking_date).items() if count > 1]

          c = list(set(array_booking_date) ^ set(repeated_elements))
          c = [s for s in c if s]

          final = reduce(lambda x, y: x + '_' + y, c)

          data = {'booking_date': final}
          opt = opt_set(user_id, data)

          bookeds = []
          if opt != None:
            if isinstance(opt['booking_date'], str):
              bookeds = opt['booking_date'].split('_')
          
          reply_markup = get_reservation_more_table(bookeds, offset)
          await query.edit_message_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)
      else:
        offset = query_array[2]
        if opt_old != None:
          if isinstance(opt_old['booking_date'], str):
            booking_date_old += opt_old['booking_date']
          booking_date = booking_date_old + '_' + query_array[1]
          array_booking_date = booking_date.split('_')

          repeated_elements = [item for item, count in Counter(array_booking_date).items() if count > 1]

          c = list(set(array_booking_date) ^ set(repeated_elements))
          c = [s for s in c if s]

          final = reduce(lambda x, y: x + '_' + y, c)

          data = {'booking_date': final}
          opt = opt_set(user_id, data)

          bookeds = []
          if opt != None:
            if isinstance(opt['booking_date'], str):
              bookeds = opt['booking_date'].split('_')
          
          reply_markup = get_reservation_more_table(bookeds, offset)
          await query.edit_message_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)

      return
    elif query_array[0] == 'time':
      placement_time_old = ""
      opt_old = opt_get(user_id)
      if opt_old != None:
        if isinstance(opt_old['placement_time'], str):
          placement_time_old += opt_old['placement_time']

      booking_date = placement_time_old + '_' + query_array[1]
      array_booking_date = booking_date.split('_')

      repeated_elements = [item for item, count in Counter(array_booking_date).items() if count > 1]

      c = list(set(array_booking_date) ^ set(repeated_elements))
      c = [s for s in c if s]

      final = reduce(lambda x, y: x + '_' + y, c)

      data = {'placement_time': final}
      opt = opt_set(user_id, data)

      bookeds = opt['placement_time'].split('_')

      reply_markup = get_reservation_time_table(bookeds)
      await query.edit_message_text('Выберите допустимое время размещений:', reply_markup=reply_markup)

    elif query_array[0] == 'watch':
      delete = 'enabled'
      if query_array[1] == 'opt-into':
        username = ''
        username_array = query_array[2:-1]
        if len(username_array) > 0:
          username = '_'.join(username_array)
        else:
          username = query_array[0]

        new_booket = ''
        # username = query_array[1]
        offset= 0
        try:
          offset = query_array[-1]
        except:
          offset= 0

        if query_array[-2] == 'more':
          username_array = query_array[2:-2]
          if len(username_array) > 0:
            username = '_'.join(username_array)
          else:
            username = query_array[0]
          delete = 'none'
          offset_old = int(query_array[-1])
          if offset_old < 20:
            offset = offset_old + 10
          else:
            offset = offset_old
        elif query_array[-1] == 'confirm':
          username_array = query_array[2:-1]
          if len(username_array) > 0:
            username = '_'.join(username_array)
          else:
            username = query_array[0]
          set_any_profile(user_id, {'rec_into_temp': username})
          user_change_message_mod(user_id, 'recommendation-creative-one')
          opt_old = set_opt_recommendation_into(user_id, query_array[2],  {'status': 'confirm'}, 'none')
          await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
          return
        elif  'morning' in query_array[-2] or 'day' in query_array[-2] or 'evening' in query_array[-2]:
          new_booket = query_array[-2]
          delete = 'none'
          username = ''
          username_array = query_array[2:-2]
          if len(username_array) > 0:
            username = '_'.join(username_array)
          else:
            username = query_array[0]

        opt_old = set_opt_recommendation_into(user_id, username,  {}, delete)

        print('рекомендации')
        allowed_dates = opt_old['allowed_dates'].split('_')
        bookeds = []
        booked_send = ''
        if opt_old != None:
          # if isinstance(opt_old['booking_date'], str):
          booked_send = opt_old['booking_date'] + '_' + new_booket
          bookeds = booked_send.split('_')

        repeated_elements = [item for item, count in Counter(bookeds).items() if count > 1]

        c = list(set(bookeds) ^ set(repeated_elements))
        c = [s for s in c if s]

        str_booked = '_'.join(c)

        opt = set_opt_recommendation_into(user_id, username,  {'booking_date': str_booked}, delete)

        reply_markup = get_reservation_req_table(bookeds=c, offset = offset, channel=username, allowed_dates=allowed_dates)
        await query.edit_message_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)


      elif query_array[1] == 'see':
        profile = get_profile(user_id)
        if profile['tariffPlan'] == 'base' or profile['tariffPlan'] == 'lite'  or profile['tariffPlan'] == 'pro':
          keyboard = [
            [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
            [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
            [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          await query.edit_message_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")
        else:
          reply_markup = btns_recommendations_get()
          await query.edit_message_text('''Каталог доступных предложений:''', reply_markup=reply_markup, parse_mode="Markdown")
          return
      elif query_array[1] == 'chanel':
        recommendation = recommendations_ind_get(query_array[2])
        keyboard = [
          [InlineKeyboardButton("Назад", callback_data='watch_see')],
          [InlineKeyboardButton("Выбрать даты", callback_data='watch_opt-into_' + recommendation['username'] + '_0')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        booking_date = recommendation['data_list'].split('_')
        booking_date_parse = parse_view_date(booking_date)
        await query.edit_message_text('''
*Подписчиков:* '''+ str(recommendation['subscribers']) +'''\n
*Охват:* '''+ str(recommendation['coverage']) +'''\n
*Стандартная цена:* '''+ str(recommendation['price_standart']) +'''\n
*Текущая цена:* '''+ str(recommendation['price_now']) +'''\n
*Формат:* '''+ recommendation['format'] +'''\n
*Число постов:* '''+ str(recommendation['number_posts']) +'''\n
*Места длля брони:* '''+ booking_date_parse +'''\n
*Ревизиты:* '''+ recommendation['requisites'] +'''\n
*Дедлайн формирования опта:* '''+ recommendation['deadline'] +'''\n
*Юзернейм:* ['''+ recommendation['username'] +''']\n
*Информация:* '''+ recommendation['info'] +'''\n
*Контакт для связи*: [@slon_feedback]''', reply_markup=reply_markup, parse_mode="Markdown")
      elif query_array[1] == 'back':
        offset = int(query_array[2]) - 10
        if offset < 0:
          offset = 0
        reply_markup = btns_recommendations_get(offset)
        await query.edit_message_text('''Каталог доступных предложений:''', reply_markup=reply_markup, parse_mode="Markdown")
      elif query_array[1] == 'next':
        offset = int(query_array[2]) + 10
        rec = recommendations_get()
        rec_len = len(rec)
        if rec_len > offset:
          reply_markup = btns_recommendations_get(offset)
          await query.edit_message_text('''Каталог доступных предложений:''', reply_markup=reply_markup, parse_mode="Markdown")
        else:
          reply_markup = btns_recommendations_get(offset - 10)
          await query.edit_message_text('''Каталог доступных предложений:''', reply_markup=reply_markup, parse_mode="Markdown")
        reply_markup = btns_recommendations_get(offset)
        await query.edit_message_text('''Каталог доступных предложений:''', reply_markup=reply_markup, parse_mode="Markdown")

    elif query_array[0] == 'lol':
      await query.edit_message_text('''В разработке''')

    elif query_array[0] == 'promocode':
      if query_array[1] == 'enter':
        await query.edit_message_text('''Вводите промокод: ''',  parse_mode="Markdown")
        user_change_message_mod(user_id, 'promocode')

    elif query_array[0] == 'empty':
      await query.answer()

    elif query_array[0] == 'opt-into':
      delete = 'enabled'
      new_booket = ''
      # username = query_array[1]
      offset= 0
      try:
        offset = query_array[3]
      except:
        offset= 0

      if query_array[2] == 'more':
        offset_old = int(query_array[3])
        if offset_old < 20:
          offset = offset_old + 10
        else:
          offset = offset_old
      elif query_array[2] == 'confirm':
        opt_old = set_opt_into(user_id, query_array[1],  {'status': 'confirm'}, 'none')
        set_any_profile(user_id, {'opt_into_temp': query_array[1]})
        user_change_message_mod(user_id, 'opt-creative-one')
        await query.edit_message_text('Отправьте креативы, кнопки присылайте отдельным креативом: ')
        return
      elif  'morning' in query_array[2] or 'day' in query_array[2] or 'evening' in query_array[2]:
        new_booket = query_array[2]
        delete = 'none'

      opt_old = set_opt_into(user_id, query_array[1],  {}, delete)
      print('опт')
      allowed_dates = opt_old['allowed_dates'].split('_')
      bookeds = []
      booked_send = ''
      if opt_old != None:
        # if isinstance(opt_old['booking_date'], str):
        booked_send = opt_old['booking_date'] + '_' + new_booket
        bookeds = booked_send.split('_')

      repeated_elements = [item for item, count in Counter(bookeds).items() if count > 1]

      c = list(set(bookeds) ^ set(repeated_elements))
      c = [s for s in c if s]

      str_booked = '_'.join(c)

      opt = set_opt_into(user_id, query_array[1],  {'booking_date': str_booked}, delete)

      reply_markup = get_reservation_into_table(bookeds=c, offset = offset, channel=query_array[1], allowed_dates=allowed_dates)
      await query.edit_message_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)

    elif query_array[0] == 'my-opt':
      opts = user_opt(user_id)
      opts_str = ''
      keyboard = []

      for opt in opts:
        keyboard.append([InlineKeyboardButton(opt['chanel'], callback_data='my-opt-chenel_' + opt['chanel'])])
        
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text('Мои опты:\n', reply_markup=reply_markup)

    elif query_array[0] == 'my-opt-chenel':
      await query.answer()
      channel = ''
      query_array.pop(0)
      if(len(query_array) > 1):
        channel = query_array.join('_')
      else:
        channel = query_array[0]
      opts = user_opt(user_id)
      keyboard = []
      for opt in opts:
        if opt['chanel'] == channel:

          for user in opt['users']:
            keyboard.append([InlineKeyboardButton(user['user']['username'], callback_data='empty'), InlineKeyboardButton('Чек', callback_data='my-opt-check_' + str(user['id']) +'_' + channel), InlineKeyboardButton('Посты', callback_data='my-opt-post_' + str(user['id']) +'_' + channel)])

      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-opt')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.message.reply_text('Ник/Чек/Посты\n', reply_markup=reply_markup)

    elif query_array[0] == 'my-opt-check':
      await query.answer()
      into_id = int(query_array[1])
      channel = ''
      query_array.pop(0)
      query_array.pop(0)
      if(len(query_array) > 1):
        channel = query_array.join('_')
      else:
        channel = query_array[0]

      opts = user_opt(user_id)
      keyboard = []
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-opt-chenel_' + channel)])
      reply_markup = InlineKeyboardMarkup(keyboard)
      for opt in opts:
        if opt['chanel'] == channel:
          for user in opt['users']:
            if user['id'] == into_id:
              if user['check'] != None:
                await context.bot.send_photo(user_id, user['check'], reply_markup=reply_markup)
              else:
                await query.message.reply_text('У пользователя нету чеков\n', reply_markup=reply_markup)
              return
              
      await query.message.reply_text('У пользователя нету чеков\n', reply_markup=reply_markup)


    elif query_array[0] == 'my-opt-post':
      await query.answer()
      into_id = int(query_array[1])
      channel = ''
      query_array.pop(0)
      query_array.pop(0)
      if(len(query_array) > 1):
        channel = query_array.join('_')
      else:
        channel = query_array[0]

      opts = user_opt(user_id)
      keyboard = []
      for opt in opts:
        if opt['chanel'] == channel:
          for user in opt['users']:
            if user['id'] == into_id:
              creatives =  user['creatives'].split('///')
              for i, v in enumerate(creatives):
                if i == 0:
                  continue
                keyboard.append([InlineKeyboardButton("Пост №"+str(i), callback_data='my-opt-post-number_' + str(i) + '_' + str(user['id']) +'_' + channel)])

      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-opt-chenel_' + channel)])
      reply_markup = InlineKeyboardMarkup(keyboard)
                
      await query.message.reply_text('У пользователя нету чеков\n', reply_markup=reply_markup)


    elif query_array[0] == 'my-opt-post-number':
      await query.answer()
      post_id = int(query_array[1])
      into_id = int(query_array[2])
      channel = ''
      query_array.pop(0)
      query_array.pop(0)
      query_array.pop(0)
      if(len(query_array) > 1):
        channel = query_array.join('_')
      else:
        channel = query_array[0]

      opts = user_opt(user_id)
      keyboard = []
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-opt-chenel_' + channel)])
      reply_markup = InlineKeyboardMarkup(keyboard)
      for opt in opts:
        if opt['chanel'] == channel:
          for user in opt['users']:
            if user['id'] == into_id:
              creatives =  user['creatives'].split('///')
              for i, v in enumerate(creatives):
                if i == post_id:
                  textArray = v.split('*')
                  if len(textArray) == 1:
                    await query.message.reply_text(v, reply_markup=reply_markup, parse_mode="HTML")
                  else:
                    text = textArray[0]
                    file_id, file_type = textArray[1].split('%')
                    if file_type == 'photo':
                      await context.bot.send_photo(caption=text, chat_id=query.message.chat.id, photo=file_id, reply_markup=reply_markup, parse_mode="HTML")
                    elif file_type == 'video':
                      await context.bot.send_video(caption=text, chat_id=query.message.chat.id, video=file_id, reply_markup=reply_markup, parse_mode="HTML")
                    elif file_type == 'animation':
                      await context.bot.send_animation(caption=text, chat_id=query.message.chat.id, animation=file_id, reply_markup=reply_markup, parse_mode="HTML")
                  return
                
      await query.message.reply_text('Упс :( какая-то ошибка\n', reply_markup=reply_markup)

    # в подборках в которых учатсвешь
    elif query_array[0] == 'my-opt-into':
      opts = user_recommendation_into(user_id)
      opts_str = ''
      keyboard = []
      for opt in opts:
        keyboard.append([
          InlineKeyboardButton(opt['chanel'], callback_data='empty'),
          InlineKeyboardButton('Посты', callback_data='my-opt-into-post_' + opt['chanel']),
          InlineKeyboardButton('Чек', callback_data='my-opt-into-check_' + opt['chanel']),
          InlineKeyboardButton('Даты брони', callback_data='my-opt-into-date_' + opt['chanel'])
        ])
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text('В подборках в которых учавствуешь\n' + opts_str, reply_markup=reply_markup)

    elif query_array[0] == 'my-opt-into-date':
      user_array = query_array[1:]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[1]
      keyboard = [[InlineKeyboardButton("Назад", callback_data='my-profile')]]
      reply_markup = InlineKeyboardMarkup(keyboard)
      opts = user_recommendation_into(user_id)
      for opt in opts:
        if opt['chanel'] == chanel:
          booking_date =  parse_view_date(opt['booking_date'].split('_'))
          await query.edit_message_text(booking_date, reply_markup=reply_markup)
          return
      await query.edit_message_text('Упс :( что-то пошло не так')

    elif query_array[0] == 'my-opt-into-check':
      user_array = query_array[1:]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[1]
      keyboard = []
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      opts = user_recommendation_into(user_id)
      for opt in opts:
        if opt['chanel'] == chanel:
          check =  opt['check']
          await query.answer()
          await context.bot.send_photo(caption="Ваш чек: ", chat_id=query.message.chat.id, photo=check, reply_markup=reply_markup)
          return
      await query.edit_message_text('Упс :( что-то пошло не так')

    elif query_array[0] == 'my-opt-into-post':
      print('посты подборок')
      user_array = query_array[1:]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[1]
      opts = user_recommendation_into(user_id)
      keyboard = []
      for opt in opts:
        if opt['chanel'] == chanel:
          creatives =  opt['creatives'].split('///')
          for i, v in enumerate(creatives):
            if i == 0:
              continue
            keyboard.append([InlineKeyboardButton("Пост № " + str(i), callback_data='my-opt-into-post-number_' + str(i) + '_' + chanel)])
          
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text('Посты:', reply_markup=reply_markup)

    elif query_array[0] == 'my-opt-into-post-number':
      print(query_array)
      user_array = query_array[2:]
      post_number = query_array[1]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[2]
      opts = user_recommendation_into(user_id)
      keyboard = [[InlineKeyboardButton("Назад", callback_data='my-profile')]]
      reply_markup = InlineKeyboardMarkup(keyboard)
      for opt in opts:
        if opt['chanel'] == chanel:
          creatives =  opt['creatives'].split('///')
          for i, v in enumerate(creatives):
            if i == int(post_number):
              print(v)
              textArray = v.split('*')
              await query.answer()
              if len(textArray) == 1:
                await query.message.reply_text(v, reply_markup=reply_markup, parse_mode="HTML")
              else:
                text = textArray[0]
                file_id, file_type = textArray[1].split('%')
                if file_type == 'photo':
                  await context.bot.send_photo(caption=text, chat_id=query.message.chat.id, photo=file_id, reply_markup=reply_markup, parse_mode="HTML")
                elif file_type == 'video':
                  await context.bot.send_video(caption=text, chat_id=query.message.chat.id, video=file_id, reply_markup=reply_markup, parse_mode="HTML")
                elif file_type == 'animation':
                  await context.bot.send_animation(caption=text, chat_id=query.message.chat.id, animation=file_id, reply_markup=reply_markup, parse_mode="HTML")
              return
          
      await query.edit_message_text('Упс какая-то ошибка :(', reply_markup=reply_markup)

    # в оптах в которых учатсвешь
    elif query_array[0] == 'my-req':
      opts = user_opt_into(user_id)

      opts_str = ''
      keyboard = []
      for opt in opts:
        keyboard.append([
          InlineKeyboardButton(opt['chanel'], callback_data='empty'),
          InlineKeyboardButton("Посты", callback_data='my-req-post_' + opt['chanel']),
          InlineKeyboardButton("Чек", callback_data='my-req-check_' + opt['chanel']),
          InlineKeyboardButton("Даты брони", callback_data='my-req-date_' + opt['chanel']),
        ])
        
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])

      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text('Опты в которых я участвую:', reply_markup=reply_markup)

    elif query_array[0] == 'my-req-post':
      user_array = query_array[1:]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[1]
      opts = user_opt_into(user_id)
      keyboard = []
      for opt in opts:
        if opt['chanel'] == chanel:
          creatives =  opt['creatives'].split('///')
          for i, v in enumerate(creatives):
            if i == 0:
              continue
            keyboard.append([InlineKeyboardButton("Пост № " + str(i), callback_data='my-req-post-number_' + str(i) + '_' + chanel)])
          
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text('Посты:', reply_markup=reply_markup)

    elif query_array[0] == 'my-req-post-number':
      user_array = query_array[2:]
      post_number = query_array[1]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[2]
      opts = user_opt_into(user_id)
      keyboard = [[InlineKeyboardButton("Назад", callback_data='my-profile')]]
      reply_markup = InlineKeyboardMarkup(keyboard)
      for opt in opts:
        if opt['chanel'] == chanel:
          creatives =  opt['creatives'].split('///')
          for i, v in enumerate(creatives):
            if i == int(post_number):
              textArray = v.split('*')
              await query.answer()
              if len(textArray) == 1:
                await query.message.reply_text(v, reply_markup=reply_markup, parse_mode="HTML")
              else:
                text = textArray[0]
                file_id, file_type = textArray[1].split('%')
                if file_type == 'photo':
                  await context.bot.send_photo(caption=text, chat_id=query.message.chat.id, photo=file_id, reply_markup=reply_markup, parse_mode="HTML")
                elif file_type == 'video':
                  await context.bot.send_video(caption=text, chat_id=query.message.chat.id, video=file_id, reply_markup=reply_markup, parse_mode="HTML")
                elif file_type == 'animation':
                  await context.bot.send_animation(caption=text, chat_id=query.message.chat.id, animation=file_id, reply_markup=reply_markup, parse_mode="HTML")
              return
          
      await query.edit_message_text('Упс какая-то ошибка :(', reply_markup=reply_markup)

    elif query_array[0] == 'my-req-check':
      user_array = query_array[1:]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[1]
      keyboard = []
      keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
      reply_markup = InlineKeyboardMarkup(keyboard)
      opts = user_opt_into(user_id)
      for opt in opts:
        if opt['chanel'] == chanel:
          check =  opt['check']
          await query.answer()
          await context.bot.send_photo(caption="Ваш чек: ", chat_id=query.message.chat.id, photo=check, reply_markup=reply_markup)
          return
      await query.edit_message_text('Упс :( что-то пошло не так')

    elif query_array[0] == 'my-req-date':
      user_array = query_array[1:]
      chanel = ''
      if len(user_array) > 1:
        chanel = '_'.join(user_array)
      else:
        chanel = query_array[1]
      keyboard = [[InlineKeyboardButton("Назад", callback_data='my-profile')]]
      reply_markup = InlineKeyboardMarkup(keyboard)
      opts = user_opt_into(user_id)
      for opt in opts:
        if opt['chanel'] == chanel:
          booking_date =  parse_view_date(opt['booking_date'].split('_'))
          await query.edit_message_text(booking_date, reply_markup=reply_markup)
          return
      await query.edit_message_text('Упс :( что-то пошло не так')

    elif query_array[0] == 'my-profile':
      user_id = query.message.chat.id
      keyboard = [
        [InlineKeyboardButton("Мои опты", callback_data='my-opt')],
        [InlineKeyboardButton("Опты в которых я участвую", callback_data='my-req')],
        [InlineKeyboardButton("Подборки в которых я участвую", callback_data='my-opt-into')],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      profile = get_profile(user_id)
      await query.answer()
      await query.message.reply_text("*Здесь собирается информация, показывающая насколько вы Slon.*\n\n*Подписка " + profile['tariffPlan'] + "* действует до: "+ profile['subscriptionEndDate'] +"\n*Ваши каналы:* " + str(profile['userNumber']) + "\n*Создано оптов:* " + str(profile['optNumber']) + " на сумму " + str(profile['totalSavings']) + "\n*Куплено оптов:* " + str(profile['byOpt']) + " на сумму " + str(profile['totalEarned']) + "\n*Всего сэкономлено:*  "+ str(profile['totalEarned']) + "\n*Приглашено пользователей:* "+ str(profile['totalEarned']) + "\n*Всего заработано:* "+ str(profile['totalEarned'] )+ "", reply_markup=reply_markup, parse_mode="Markdown")




  async def handler_checkout(self, update: Update, context) -> None:
    total_amount = update.pre_checkout_query.total_amount
    user_id = update.message.chat.id
    id = update.pre_checkout_query.id
    await update.pre_checkout_query.answer(ok=True)
    # await context.bot.answer_pre_checkout_query(id, ok=True)
    # user = get_profile(user_id)
    # tariff_plan = user['tariffPlan']
    # subscription_end_date = user['subscriptionEndDate']

    # await update.message.reply_text('Получилось! Теперь у вас подписка *' + tariff_plan + '*, действующая до ' + subscription_end_date, parse_mode="Markdown")
    return


  async def handler_test(self, update: Update, context) -> None:
    text = '@aaaaaaaaawd'
    test = await context.bot.get_chat(chat_id=text)
    # test = self.ug.get_user(first_name="Test", last_name="The Bot")
    # test = await update.get_user(text='')

  async def handler_secret_profile_base(self, update: Update, context) -> None:
    id = update.message.chat.id
    set_tariff_profile(id, 'base', 'never')
    await update.message.reply_text('У вас подписка base')

  async def handler_secret_profile_lite(self, update: Update, context) -> None:
    id = update.message.chat.id
    set_tariff_profile(id, 'lite', 30)
    await update.message.reply_text('У вас подписка lite')
  async def handler_secret_profile_pro(self, update: Update, context) -> None:
    id = update.message.chat.id
    set_tariff_profile(id, 'pro', 30)
    await update.message.reply_text('У вас подписка pro')
  async def handler_secret_profile_business(self, update: Update, context) -> None:
    id = update.message.chat.id
    set_tariff_profile(id, 'business', 30)
    await update.message.reply_text('У вас подписка business')
  async def handler_get_profile_business(self, update: Update, context) -> None:
    id = update.message.chat.id
    res = set_tariff_profile(id, 'business', 30, 'enabled')
    if res == 'no':
      await update.message.reply_text('Вы уже один раз импользовали секретную команду :(')
    else:
      await update.message.reply_text('У вас подписка business')

def main() -> None:
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  game_bot = SlonBot(token = API_TOKEN)
  game_bot.run_bot()


if __name__ == "__main__":
  main()
