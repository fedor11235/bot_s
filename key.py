import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from requests_data import (
  user_check,
  get_profile,
  user_get_message_mod,
  # go_into_opt_user,
  user_change_message_mod
)
from create_btns import (
  btns_recommendations_get,
  get_user_chanels,
  go_into_opt_user
)

text_key = ['Создать опт', 'Зайти в опт', 'Slon Business✨', 'Профиль']

# кнопки на клавиатуре
async def handler_btn_keyboard(update: Update, _) -> None:
  text = update.message.text
  user_id = update.message.chat.id

  if text in text_key:
    user_change_message_mod(user_id, 'standart')

  if text == 'Создать опт':
    user_stat = user_check(user_id)
    if user_stat == 'empty':
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
          '?idUser=' + str(user_id)
          )
        chanels = req.json()
        reply_markup = get_user_chanels(chanels)
        await update.message.reply_text('Выберите канал в котором хотите собрать опт:', reply_markup=reply_markup)
    return
  elif text == 'Зайти в опт':
    user_stat = user_check(user_id)
    if user_stat == 'empty':
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
        reply_markup = go_into_opt_user()
        await update.message.reply_text('Зайти в опт', reply_markup=reply_markup)
    return
  elif text == 'Slon Business✨':
    user_stat = user_check(user_id)
    if user_stat == 'empty':
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
        # keyboard = [
        #   [InlineKeyboardButton("<<Назад", callback_data='testtest'), InlineKeyboardButton("Смотреть предложения", callback_data='watch_see')]
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        # await update.message.reply_text('*Подборки* — это инструмент автоматической масштабной закупки рекламы в топовых telegram-каналах по уникальным ценам.', reply_markup=reply_markup, parse_mode="Markdown")
        profile = get_profile(user_id)
        if profile['tariffPlan'] == 'base' or profile['tariffPlan'] == 'lite'  or profile['tariffPlan'] == 'pro':
          keyboard = [
            [InlineKeyboardButton("Lite — 290₽/мес.", callback_data='pay_lite')],
            [InlineKeyboardButton("Pro — 890₽/мес.", callback_data='pay_pro')],
            [InlineKeyboardButton("Business — 3890₽/мес.", callback_data='pay_business')],
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          await update.message.reply_text('''*Lite*\n• доступ к полному функционалу каталога\n• подключение до 2 каналов к боту\n• создание до 2 оптов в месяц\n• до 10 мест в каждом созданном опте\n• покупка до 10 оптов в месяц\n• статус подтвержденного канала в каталоге\n\n*Pro*\n• доступ к полному функционалу каталога\n• безлимит на подключение каналов\n• безлимит на создание оптов\n• до 20 мест в каждом созданном опте\n• безлимит на покупку оптов\n• статус подтвержденного канала в каталоге\n\n*Business*\n• все вышеперечисленные функции\n• до 30 мест в каждом созданном опте\n• доступ к уникальным подборкам в крупнейших и авторских каналах от команды Slon''', reply_markup=reply_markup, parse_mode="Markdown")
        else:
          reply_markup = btns_recommendations_get()
          await update.message.reply_text('''Каталог доступных предложений:''', reply_markup=reply_markup, parse_mode="Markdown")
    return
  elif text == 'Профиль':
    user_stat = user_check(user_id)
    if user_stat == 'empty':
      await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
    else:
      keyboard = [
        [InlineKeyboardButton("Мои опты", callback_data='my-opt')],
        [InlineKeyboardButton("Опты в которых я участвую", callback_data='my-opt-into')],
        [InlineKeyboardButton("Мои каналы", callback_data='my-chanel')],
        [InlineKeyboardButton("График выходов", callback_data='release-schedule')],
        # [InlineKeyboardButton("Подборки в которых я участвую", callback_data='my-opt-into')],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      profile = get_profile(user_id)
      await update.message.reply_text("*Здесь собирается информация, показывающая насколько вы Slon.*\n\n*Подписка " + profile['tariffPlan'] + "* действует до: "+ profile['subscriptionEndDate'] +"\n*Ваши каналы:* " + str(profile['userNumber']) + "\n*Создано оптов:* " + str(profile['optNumber']) + " на сумму " + str(profile['totalSavings']) + "\n*Куплено оптов:* " + str(profile['byOpt']) + " на сумму " + str(profile['totalEarned']) + "\n*Всего сэкономлено:*  "+ str(profile['totalEarned']) + "\n*Приглашено пользователей:* "+ str(profile['totalEarned']) + "\n*Всего заработано:* "+ str(profile['totalEarned'] )+ "", reply_markup=reply_markup, parse_mode="Markdown")
      return