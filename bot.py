import logging
import requests
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import os
from requests_data import (
  user_check,
  user_change_message_mod,
  user_get_message_mod, 
  opt_create,
  opt_set,
  opt_get,
)

from create_btns import (
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
  go_chanel_opt,
  opt_reservation
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

filters_type = ['rating', 'coverage', 'numberSubscribers', 'growthMonth', 'growthWeek', 'new', 'old', 'confirm']
category_type = ['all', 'education', 'finance', 'health', 'news', 'tech', 'entertainment', 'psychology', 'video', 'author', 'other']

class SlonBot():
  def __init__(self, token):
    self.token = token

  def run_bot(self) -> None:
    application = Application.builder().token(self.token).build()
    application.add_handler(CallbackQueryHandler(self.button))
    application.add_handler(CommandHandler("test", self.handler_test))
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
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Создайте профиль и добавьте канал*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
        parse_mode="Markdown")
    else:
      await update.message.reply_text('''\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''',
        parse_mode="Markdown")

  async def handler_new_slon(self, update: Update, _) -> None:
    await update.message.reply_text('вы вызвали команду new_slon')

  async def handler_partners(self, update: Update, _) -> None:
    req = requests.get('http://localhost:3001/user/promocode' + '?id=' + str(update.message.chat.id))
    await update.message.reply_text(req.text)

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
        keyboard = [
          [InlineKeyboardButton("Добавить канал", callback_data='chanelAdd')],
        ]
        reply_markup =  InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('''*Вы пока что не добавили ни одного канала. Чтобы его добавить, введите команду /channel или нажмите кнопку ниже.''', reply_markup=reply_markup, parse_mode="Markdown")
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
        reply_markup = go_into_opt()
        await update.message.reply_text('Зайти в опт', reply_markup=reply_markup)
      return
    elif update.message.text == 'Подборки':
      user_stat = user_check(user_id)
      if user_stat == 'empty':
        await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
      else:
        keyboard = [
          [InlineKeyboardButton("<<Назад", callback_data='testtest'), InlineKeyboardButton("Смотреть предложения", callback_data='watch')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('*Slon Business* «— это инструмент автоматической масштабной закупки рекламы в топовых telegram-каналах по уникальным ценам.', reply_markup=reply_markup, parse_mode="Markdown")
      return
    try:
      if update.message.forward_from_chat:
        idChanel = update.message.forward_from_chat.id
        await context.bot.get_chat_member(user_id=6423584132, chat_id=str(idChanel))
        req = requests.get(
          'http://localhost:3001/chanel/create' +
          '?idUser=' + str(user_id) +
          '&idChanel=' + str(idChanel)
        )
      else:
        await context.bot.get_chat_member(user_id=6423584132, chat_id=update.message.text)
        req = requests.get(
          'http://localhost:3001/chanel/create' +
          '?idUser=' + str(user_id) +
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
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      keyboard = [
        [KeyboardButton("Каталог")],
        [KeyboardButton("Создать опт"), KeyboardButton("Зайти в опт")],
        [KeyboardButton("Подборки"), KeyboardButton("Профиль")],
      ]
      reply_markup = ReplyKeyboardMarkup(keyboard)
      req = requests.get(
        'http://localhost:3001/user/profile' +
        '?idUser=' + str(update.message.chat.id)
      )
      profile = req.json()
      await update.message.reply_text("*Здесь собирается информация, показывающая насколько вы Slon.*\nПодписка " + profile['tariffPlan'] + " действует до: "+ profile['subscriptionEndDate'] +"\nВаши каналы: " + str(profile['channels']) + "\nСоздано оптов: " + str(profile['createdOpt']) + " на сумму " + str(profile['totalSavings']) + "\nКуплено оптов: " + str(profile['byOpt']) + " на сумму " + str(profile['totalEarned']) + "\nВсего сэкономлено:  "+ str(profile['totalEarned']) + "\nПриглашено пользователей: "+ str(profile['totalEarned']) + "\nВсего заработано: "+ str(profile['totalEarned'] )+ "", reply_markup=reply_markup, parse_mode="Markdown")
  
  async def handler_help(self, update: Update, _) -> None:
    await update.message.reply_text('''*Возникли вопросы?*\nМы всегда готовы помочь вам с любые задачи и решение всех интересующих вопросов.\nПросто напишите нам: @slon_feedback''')

  async def handler_channel(self, update: Update, _) -> None:
    user_stat = user_check(update.message.chat.id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
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
  async def button(self, update: Update, _):

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
      categoriesArray = get_categories(query_array[0], start_cut, finish_cut, page)
      try:
        await query.edit_message_text('все каналы', reply_markup=categoriesArray)
      except:
        await query.edit_message_text('нет каналов такой категории')
    #!ФИЛЬТРЫ
    elif query_array[0] == 'filters':
      reply_markup =  set_filters(query_array[1], False)
      await query.edit_message_text('Фильтры', reply_markup=reply_markup)
    elif query_array[0] in filters_type:
      reply_markup =  set_filters(query.data, True)
      await query.edit_message_text('Фильтры', reply_markup=reply_markup)
    elif query_array[0] == 'apply':
      categoriesArray = get_categories(query_array[-1], 1, 10, 0)
      #TODO тут вставить запрос на сохранение фильтров
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
        query.edit_message_text("Упс произошла ошибка")
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
          # print(query_array[3])
          # reply_markup = get_reservation_more_table()
          # await update.message.reply_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)
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
          booking_date_old += '_' + opt_old['booking_date']

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
      data = {'placement_time': query_array[1]}
      opt_set(user_id, data)

    elif query_array[0] == 'watch':
      req = requests.get(
        'http://localhost:3001/user/profile' +
        '?idUser=' + str(user_id)
      )
      profile = req.json()
      if profile['tariffPlan'] == 'base':
        keyboard = [
          [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
          [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
          [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")
      else:
        await query.edit_message_text('''[(Название канала с вшитой ссылкой) (Стоимость рекламного места)тыс.₽]''')
        return
        














  async def handler_test(self, update: Update, _) -> None:
    from datetime import datetime

    current_datetime = datetime.now()
    date = str(current_datetime.month) + '.' + str(current_datetime.day)
    await update.message.reply_text(date)

def main() -> None:
  load_dotenv()
  API_TOKEN = os.getenv('API_TOKEN')
  game_bot = SlonBot(token = API_TOKEN)
  game_bot.run_bot()


if __name__ == "__main__":
  main()
