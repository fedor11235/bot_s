import logging
import requests
from telegram import Update, LabeledPrice
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, PreCheckoutQueryHandler
from dotenv import load_dotenv
import os
from requests_data import (
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
  recommendations_ind_get
)

from create_btns import (
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

filters_type = ['rating', 'coverage', 'numberSubscribers', 'growthMonth', 'growthWeek', 'new', 'old', 'confirm']
filters_type = ['repost', 'numberSubscribers', 'coveragePub', 'coverageDay', 'indexSay']
category_type = ['all', 'education', 'finance', 'health', 'news', 'tech', 'entertainment', 'psychology', 'video', 'author', 'other']

class SlonBot():
  def __init__(self, token):
    self.token = token

  def run_bot(self) -> None:
    application = Application.builder().token(self.token).build()
    application.add_handler(CommandHandler("test", self.handler_test))
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
    application.add_handler(CommandHandler("catalog", self.handler_catalog))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.response_from__message))
    application.run_polling()

  async def handler_start(self, update: Update, _) -> None:
    print('ИИИ ЧЕ')
    user_stat = user_check(update.message.chat.id)
    keyboard = [
      [KeyboardButton("Каталог")],
      [KeyboardButton("Создать опт"), KeyboardButton("Зайти в опт")],
      [KeyboardButton("Подборки"), KeyboardButton("Профиль")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    print('user_stat')
    print(user_stat)
    if user_stat == 'empty':
      user_change_message_mod(update.message.chat.id, 'chanel')
      await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
        reply_markup=reply_markup, parse_mode="Markdown")
    else:
      await update.message.reply_text('''\nВоспользуйтесь кнопками ниже или основным меню для работы с ботом:''', 
        reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_new_slon(self, update: Update, _) -> None:
    await update.message.reply_text('вы вызвали команду new_slon')

  async def handler_partners(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      req = requests.get('http://localhost:3001/user/promocode' + '?idUser=' + str(update.message.chat.id))
      await update.message.reply_text(req.json())

  async def handler_business(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      keyboard = [
        [InlineKeyboardButton("<<Назад", callback_data='testtest'), InlineKeyboardButton("Смотреть предложения", callback_data='watch_see')]
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      await update.message.reply_text('*Slon Business* «— это инструмент автоматической масштабной закупки рекламы в топовых telegram-каналах по уникальным ценам.', reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_newopt(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      keyboard = [
        [InlineKeyboardButton("Добавить канал", callback_data='chanelAdd')],
      ]
      reply_markup =  InlineKeyboardMarkup(keyboard)
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      req = requests.get(
        'http://localhost:3001/chanel/user' +
        '?idUser=' + str(update.message.chat.id)
        )
      chanels = req.json()
      reply_markup = get_user_chanels(chanels)
      await update.message.reply_text('Выберите канал в котором хотите собрать опт:\n', reply_markup=reply_markup)
    return

  async def handler_getopt(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      reply_markup = go_into_opt()
      await update.message.reply_text('Зайти в опт', reply_markup=reply_markup)

  async def response_from__message(self, update: Update, context) -> None:
    user_id = update.message.chat.id
    mode = user_get_message_mod(user_id)

    #создание оптов
    if mode == 'opt-retail-price':
      try:
        retail_price = int(update.message.text)
        data = {'retail_price': retail_price}
        opt_set(user_id, data)
        user_change_message_mod(user_id, 'opt-wholesale-cost')
        await update.message.reply_text("Напишите текущую(оптовую) стоимость размещения. Разница с розничной должна быть не менее 10%:")
      except:
        await update.message.reply_text("вы ввели неверные данные, повторите ввод")
      return
    elif mode == 'opt-wholesale-cost':
      try:
        wholesale_cost = int(update.message.text)
        data = {'wholesale_cost': wholesale_cost}
        opt_set(user_id, data)
        user_change_message_mod(user_id, 'opt-minimum-permissible-value')
        await update.message.reply_text("Введите минимальное количество мест, необходимое для оформления опта(от 3 до 10):")
      except:
        await update.message.reply_text("вы ввели неверные данные, повторите ввод")
      return
    elif mode == 'opt-minimum-permissible-value':
      try:
        opt_minimum = int(update.message.text)
        if opt_minimum > 3 and opt_minimum < 10:
          data = {'min_places': str(opt_minimum)}
          opt_set(user_id, data)
          user_change_message_mod(user_id, 'opt-maximum-permissible-value')
          await update.message.reply_text("Введите максимальное допустимое количество мест в опте(до x):")
        else:
          await update.message.reply_text("вы ввели неверные данные, повторите ввод")
      except:
        await update.message.reply_text("вы ввели неверные данные, повторите ввод")
      return
    elif mode == 'opt-maximum-permissible-value':
      try:
        opt_maximum = int(update.message.text)
        data = {'max_places': str(opt_maximum)}
        opt_set(user_id, data)
        user_change_message_mod(user_id, 'opt-available-reservation')
        reply_markup = get_reservation_more_table()
        await update.message.reply_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)
      except:
        await update.message.reply_text("вы ввели неверные данные, повторите ввод")
      return
    elif mode == 'opt-available-reservation':
      reply_markup = get_reservation_more_table()
      await update.message.reply_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)
      return
    elif mode == 'deadline-wholesale-formation':
      deadline_date = update.message.text
      data = {'deadline_date': deadline_date}
      opt_set(user_id, data)
      reply_markup = get_reservation_time_table()
      await update.message.reply_text('Выберите допустимое время размещений:', reply_markup=reply_markup)
      return
    elif mode == 'opt-send-details':
      try:
        requisites = update.message.text
        data = {'requisites': requisites}
        opt = opt_set(user_id, data)
        reply_markup = get_opt_create()
        await update.message.reply_text('''
Опт от '''+'1.07'+''' в канале *'''+opt['chanel']+'''*
Розничная цена: '''+ str(opt['retail_price']) + ''' \n
Оптовая цена: '''+ str(opt['wholesale_cost']) + '''\n
Минимум постов: '''+ str(opt['min_places']) + '''\n
Максимум постов: '''+ str(opt['max_places']) + '''\n
Список дат: '''+ opt['booking_date'] + '''\n
Дедлайн: '''+ opt['deadline_date'] + '''\n
Реквизиты: '''+ opt['requisites'] + '''\n
Владелец: '''+ str(opt['idUser'])
        ,
        reply_markup=reply_markup
      )
      except:
        await update.message.reply_text("Упс произошла ошибка")
      return
    #кнопки на клавиатуре
    if update.message.text == 'Каталог':
      user_stat = user_check(user_id)
      if user_stat == 'empty':
        await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
      else:
        reply_markup = set_catalog()
        await update.message.reply_text('Каталог', reply_markup=reply_markup)
      return
    elif update.message.text == 'Создать опт':
      user_stat = user_check(user_id)
      if user_stat == 'empty':
        await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
        # keyboard = [
        #   [InlineKeyboardButton("Добавить канал", callback_data='chanelAdd')],
        # ]
        # reply_markup =  InlineKeyboardMarkup(keyboard)
        # await update.message.reply_text("*Вы пока что не добавили ни одного канала.* Чтобы его добавить, введите команду /channel или нажмите кнопку ниже.", reply_markup=reply_markup, parse_mode="Markdown")
      
      else:
        req = requests.get(
          'http://localhost:3001/chanel/user' +
          '?idUser=' + str(user_id)
          )
        chanels = req.json()
        reply_markup = get_user_chanels(chanels)
        await update.message.reply_text('Выберите канал в котором хотите собрать опт:\n', reply_markup=reply_markup)
      return
    elif update.message.text == 'Зайти в опт':
      user_stat = user_check(user_id)
      if user_stat == 'empty':
        await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
      else:
        reply_markup = go_into_opt_user()
        await update.message.reply_text('Зайти в опт', reply_markup=reply_markup)
      return
    elif update.message.text == 'Подборки':
      user_stat = user_check(user_id)
      if user_stat == 'empty':
        await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
      else:
        keyboard = [
          [InlineKeyboardButton("<<Назад", callback_data='testtest'), InlineKeyboardButton("Смотреть предложения", callback_data='watch_see')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('*Slon Business* «— это инструмент автоматической масштабной закупки рекламы в топовых telegram-каналах по уникальным ценам.', reply_markup=reply_markup, parse_mode="Markdown")
      return
    elif update.message.text == "Профиль":
      user_stat = user_check(user_id)
      if user_stat == 'empty':
        await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
      else:
        profile = get_profile(update.message.chat.id)
        await update.message.reply_text("*Здесь собирается информация, показывающая насколько вы Slon.*\nПодписка " + profile['tariffPlan'] + " действует до: "+ profile['subscriptionEndDate'] +"\nВаши каналы: " + str(profile['channels']) + "\nСоздано оптов: " + str(profile['createdOpt']) + " на сумму " + str(profile['totalSavings']) + "\nКуплено оптов: " + str(profile['byOpt']) + " на сумму " + str(profile['totalEarned']) + "\nВсего сэкономлено:  "+ str(profile['totalEarned']) + "\nПриглашено пользователей: "+ str(profile['totalEarned']) + "\nВсего заработано: "+ str(profile['totalEarned'] )+ "", parse_mode="Markdown")    
    #добавление канала
    elif mode == 'chanel':
      try:
        if update.message.forward_from_chat:
          idChanel = update.message.forward_from_chat.id
          await context.bot.get_chat_member(user_id=6423584132, chat_id=str(idChanel))
          status = create_chanel(user_id, idChanel)
          user_change_message_mod(update.message.chat.id, 'standart')
          if status == 'exist':
            await update.message.reply_text('Такой канал уже добавлен')
            return
          elif status == 'created':
            await update.message.reply_text('Ваш канал успешно зарегистрирован')
            return
        else:
          await context.bot.get_chat_member(user_id=6423584132, chat_id=update.message.text)
          status = create_chanel(user_id, update.message.text)
        user_change_message_mod(update.message.chat.id, 'standart')
        if status == 'exist':
          await update.message.reply_text('Такой канал уже добавлен')
          return
        elif status == 'created':
          await update.message.reply_text('Ваш канал успешно зарегистрирован')
          return

      except:
        user_change_message_mod(update.message.chat.id, 'standart')
        await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')
        return









  async def handler_profile(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      profile = get_profile(update.message.chat.id)
      await update.message.reply_text("*Здесь собирается информация, показывающая насколько вы Slon.*\nПодписка " + profile['tariffPlan'] + " действует до: "+ profile['subscriptionEndDate'] +"\nВаши каналы: " + str(profile['channels']) + "\nСоздано оптов: " + str(profile['createdOpt']) + " на сумму " + str(profile['totalSavings']) + "\nКуплено оптов: " + str(profile['byOpt']) + " на сумму " + str(profile['totalEarned']) + "\nВсего сэкономлено:  "+ str(profile['totalEarned']) + "\nПриглашено пользователей: "+ str(profile['totalEarned']) + "\nВсего заработано: "+ str(profile['totalEarned'] )+ "", parse_mode="Markdown")
  
  async def handler_help(self, update: Update, _) -> None:
    await update.message.reply_text('''*Возникли вопросы?*\nМы всегда готовы помочь вам с любые задачи и решение всех интересующих вопросов.\nПросто напишите нам: @slon_feedback''')

  async def handler_channel(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      user_change_message_mod(update.message.chat.id, 'chanel')
      await update.message.reply_text('''Чтобы добавить канал введите в поле ниже\n''')

  async def handler_pay(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      keyboard = [
        [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
        [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
        [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      await update.message.reply_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")

  async def handler_catalog(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      reply_markup = set_catalog()
      await update.message.reply_text('Выберите тематику:',reply_markup=reply_markup)
  
  # all education health news tech entertainment psychology author other
  async def handler_callback(self, update: Update, _):
    print(update.callback_query)

    query = update.callback_query
    query_array = query.data.split('_')
    user_id = query.message.chat.id

    #!Подписчки
    if query_array[0] == 'pay':
      reply_markup = get_btns_pay()
      await query.answer()
      if query_array[1] == 'lite':
        await query.edit_message_text(text='Выберите срокна который хотите продлить подписку Lite\nВаша скидка: 0%',  reply_markup=reply_markup)
      elif query_array[1] == 'pro':
        await query.edit_message_text(text='Выберите срокна который хотите продлить подписку Pro\nВаша скидка: 0%',  reply_markup=reply_markup)
      elif query_array[1] == 'business':
        await query.edit_message_text(text='Выберите срокна который хотите продлить подписку Business\nВаша скидка: 0%',  reply_markup=reply_markup)
    #!КАТЕГОРИИ
    elif query_array[0] in category_type:
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
      categoriesArray = get_categories(query_array[1], 1, 10, 1, user_id, filter=query_array[2])
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
        await query.message.reply_text('Хотите выбрать следующие даты:?', reply_markup=reply_markup)
        return
      elif query_array[1] == 'save':
        user_change_message_mod(user_id, 'deadline-wholesale-formation')
        await query.message.reply_text('Укажите крайнюю дату формирования опта в формате [01.07]. По наступлении этой даты, если опт не будет собран, он будет отменен.')
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
      elif query_array[1] in category_type:
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
        elif query_array[1] == 'morning' or query_array[2] == 'day' or query_array[2] == 'evening':
          return
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
        if query_array[2] in category_type:
          if query_array[3] == 'back':
            reply_markup = go_into_opt_user()
            await query.message.reply_text('Зайти в опт', reply_markup=reply_markup)
          if query_array[3] == 'data':
            print('data')
          elif query_array[3] == 'next':
            print('next')    
          elif query_array[3] == 'filters':
            user = get_profile(user_id)
            filter = parse_filter(user['filter'])
            reply_markup =  set_filters_opt(query_array[1], filter)
            await query.message.reply_text('Фильтры:', reply_markup=reply_markup)
          elif query_array[3] == 'old':
            opt = user_get_stat_opt(query_array[4])
            reply_markup = user_get_btns_into(query_array[2])
            await query.message.reply_text('''
Розничная цена: '''+ str(opt['retail_price']) +'''
Оптовая цена: '''+ str(opt['wholesale_cost']) +'''
Минимум постов: '''+ str(opt['min_places']) +'''
Максимум постов: '''+ str(opt['max_places']) +'''
Список дат: '''+ str(opt['booking_date']) +'''
Дедлайн: '''+ str(opt['deadline_date']) +'''
Реквизиты: '''+ str(opt['requisites']) +'''
Владелец: '''+ str(opt['user_id']) +'''
''', reply_markup=reply_markup)
          elif query_array[3] == 'init':
            print('init')
            start_cut = 1
            finish_cut = 10
            page = 1
            profile = get_profile(user_id)
            reply_markup = go_chanel_opt_into(query_array[2], start_cut, finish_cut, page, profile['filter_opt'], user_id)
            await query.message.reply_text('Выберите опт', reply_markup=reply_markup)
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
          offset = offset_old
      else:
        offset = query_array[2]
      if opt_old != None:
        if isinstance(opt_old['booking_date'], str):
          booking_date_old += opt_old['booking_date']

      data = {'booking_date': booking_date_old + '_' + query_array[1]}
      opt = opt_set(user_id, data)
      # opt = opt_get(user_id)
      bookeds = []
      if opt != None:
        if isinstance(opt['booking_date'], str):
          bookeds = opt['booking_date'].split('_')
      
      reply_markup = get_reservation_more_table(bookeds, offset)
      await query.edit_message_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)

    elif query_array[0] == 'time':
      placement_time_old = ""
      opt_old = opt_get(user_id)
      if opt_old != None:
        if isinstance(opt_old['placement_time'], str):
          placement_time_old += opt_old['placement_time']

      data = {'placement_time': placement_time_old + '_' + query_array[1]}
      opt = opt_set(user_id, data)

      bookeds = opt['placement_time'].split('_')

      reply_markup = get_reservation_time_table(bookeds)
      await query.edit_message_text('Выберите допустимое время размещений:', reply_markup=reply_markup)

    elif query_array[0] == 'watch':
      if query_array[1] == 'see':
        profile = get_profile(user_id)
        if profile['tariffPlan'] == 'base':
          # keyboard = [
          #   [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
          #   [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
          #   [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
          # ]
          # reply_markup = InlineKeyboardMarkup(keyboard)
          reply_markup = btns_recommendations_get()
          # await query.edit_message_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")
          await query.edit_message_text('''Каталог доступных предложений:''', reply_markup=reply_markup, parse_mode="Markdown")
        else:
          await query.edit_message_text('''[(Название канала с вшитой ссылкой) (Стоимость рекламного места)тыс.₽]''')
          return
      elif query_array[1] == 'chanel':
        recommendation = recommendations_ind_get(query_array[2])
        keyboard = [
          [InlineKeyboardButton("Назад", callback_data='watch_see')],
          [InlineKeyboardButton("Выбрать даты", callback_data='lol')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('''
Подписчиков: ??
Охват: ??
Стандартная цена: '''+ recommendation['price_standart'] +'''
Текущая цена: '''+ recommendation['price_now'] +'''
Контакт для связи: @slon_feedback»
''', reply_markup=reply_markup)
        
    elif query_array[0] == 'lol':
      await query.edit_message_text('''Вы разработке''')








  async def handler_checkout(self, update: Update, context) -> None:
    # print(update.callback_query.edit_message_text)
    total_amount = update.pre_checkout_query.total_amount
    # id = update.pre_checkout_query.id
    if total_amount == 29000:
      await update.pre_checkout_query.answer(ok=True)
      # await context.bot.answer_pre_checkout_query(id, ok=True)
      # await update.message.reply_text("User said:")
      # await update.pre_checkout_query.edit_message_text("Вы купили подписку Lite")
    # elif total_amount == 89000:
    #   await update.message.reply_text("Вы купили подписку Pro")
    # elif total_amount == 389000:
    #   await update.message.reply_text("Вы купили подписку Business")
    return


  async def handler_test(self, update: Update, context) -> None:
    # from datetime import datetime

    # current_datetime = datetime.now()
    # date = str(current_datetime.month) + '.' + str(current_datetime.day)
    
    # await context.bot.send_invoice(chat_id=update.message.chat_id, title="title", description="description", payload="payload",
    #   provider_token="390540012:LIVE:40517", start_parameter="", currency="RUB",
    #   prices=[LabeledPrice('тестовая сумма', 20000)])
    await context.bot.send_invoice(chat_id=update.message.chat_id, title="Оплата подписки", description="Для того чтобы оплатить нажмите кнопку ниже:", payload="payload",
      provider_token="381764678:TEST:67635", start_parameter="", currency="RUB",
      prices=[
        LabeledPrice('Lite — 290₽/мес.', 29000),
        # LabeledPrice('Pro — 890₽/мес.', 89000),
        # LabeledPrice('Business — 3890₽/мес.', 389000)
      ])

def main() -> None:
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  game_bot = SlonBot(token = API_TOKEN)
  game_bot.run_bot()


if __name__ == "__main__":
  main()
